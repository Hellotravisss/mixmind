"""
MixMind — LoRA fine-tune of Gemma 4 on the plant SFT set.

Runs on the AMD Radeon notebook (ROCm + transformers 5.13, which we proved loads
Gemma 4). Deliberately uses ONLY `peft` as a new dependency + a plain training
loop — no Unsloth / TRL — to avoid version-pin conflicts with transformers 5.

Paste cell-by-cell, or run as a script. Expect the adapter in ./mixmind-gemma4-lora.

NEXT-SESSION CHECKLIST (validate before a long run):
  1. `%pip install -q peft` in the kernel, then RESTART the kernel.
  2. Confirm the dataset path (upload mixmind_sft.jsonl to the notebook).
  3. Do a 2-step smoke run first (set MAX_STEPS=2) to catch any ROCm/peft issue
     before committing GPU time; then set MAX_STEPS back to None for the full run.
  4. Loss should fall over the epochs. Then run the before/after eval cell.
"""
import json, torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import LoraConfig, get_peft_model
from torch.utils.data import DataLoader

MODEL   = "google/gemma-4-12B-it"
DATA    = "mixmind_sft.jsonl"     # upload alongside this script
OUT     = "mixmind-gemma4-lora"
EPOCHS  = 3
LR      = 2e-4
BATCH   = 2
MAXLEN  = 1024
MAX_STEPS = None                  # set to 2 for a smoke test first

tok = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForCausalLM.from_pretrained(MODEL, dtype=torch.bfloat16, device_map="cuda",
                                             attn_implementation="sdpa")
model.gradient_checkpointing_enable()
model.enable_input_require_grads()

lora = LoraConfig(
    r=16, lora_alpha=32, lora_dropout=0.05, bias="none", task_type="CAUSAL_LM",
    target_modules=["q_proj","k_proj","v_proj","o_proj","gate_proj","up_proj","down_proj"],
)
model = get_peft_model(model, lora)
model.print_trainable_parameters()

# ---- build prompt-masked training examples (loss only on the assistant reply) ----
# NOTE: on transformers 5.x, apply_chat_template(tokenize=True) can return tokenizers.Encoding
# objects that torch.tensor can't infer a dtype for. return_dict=True gives plain int lists.
def encode(msgs):
    prompt_ids = tok.apply_chat_template(msgs[:-1], add_generation_prompt=True,
                                         tokenize=True, return_dict=True)["input_ids"]
    full_ids   = tok.apply_chat_template(msgs, tokenize=True, return_dict=True)["input_ids"]
    prompt_ids = list(prompt_ids); full_ids = list(full_ids)
    labels = list(full_ids)
    for i in range(min(len(prompt_ids), len(labels))):
        labels[i] = -100                      # mask the system+user prompt
    return full_ids[:MAXLEN], labels[:MAXLEN]

rows = [json.loads(l) for l in open(DATA)]
data = [encode(r["messages"]) for r in rows]
print(f"{len(data)} training examples")

pad = tok.pad_token_id or 0
def collate(batch):
    m = max(len(x[0]) for x in batch)
    ids, lbl, att = [], [], []
    for inp, lab in batch:
        p = m - len(inp)
        ids.append(inp + [pad]*p)
        lbl.append(lab + [-100]*p)
        att.append([1]*len(inp) + [0]*p)
    t = lambda a: torch.tensor(a, device="cuda")
    return t(ids), t(lbl), t(att)

loader = DataLoader(data, batch_size=BATCH, shuffle=True, collate_fn=collate)
opt = torch.optim.AdamW([p for p in model.parameters() if p.requires_grad], lr=LR)

# ---- train ----
model.train()
step = 0
for ep in range(EPOCHS):
    for ids, lbl, att in loader:
        out = model(input_ids=ids, attention_mask=att, labels=lbl)
        out.loss.backward()
        opt.step(); opt.zero_grad()
        step += 1
        if step % 5 == 0 or step == 1:
            print(f"epoch {ep+1} step {step} loss {out.loss.item():.3f}")
        if MAX_STEPS and step >= MAX_STEPS:
            break
    if MAX_STEPS and step >= MAX_STEPS:
        break

model.save_pretrained(OUT)
tok.save_pretrained(OUT)
print(f"saved LoRA adapter -> {OUT}")

# ---- quick before/after sanity check (run after training) ----
def ask(m, q):
    ids = tok.apply_chat_template([{"role":"user","content":q}], add_generation_prompt=True,
                                  return_tensors="pt", return_dict=True).to("cuda")
    out = m.generate(**ids, max_new_tokens=160)
    return tok.decode(out[0][ids["input_ids"].shape[1]:], skip_special_tokens=True)

model.eval()
print("\nFINE-TUNED:", ask(model, "Why replace part of the cement with slag?"))
# compare against base: model.disable_adapter() context, or reload base separately.
