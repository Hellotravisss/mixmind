# MixMind fine-tune (LoRA on Gemma 4)

Ready to run on the AMD Radeon notebook next GPU session.

## Files
- `build_dataset.py` — authors the SFT examples (readable source of truth). Run it to (re)generate the dataset.
- `mixmind_sft.jsonl` — 27 training examples, chat format. Regenerate with `python build_dataset.py`.
- `train_lora.py` — plain PEFT LoRA trainer (no Unsloth/TRL — fewest version conflicts with transformers 5.13 + Gemma 4).

## Dataset (27 examples, expandable)
| Category | n | Teaches |
|---|---|---|
| grounded | 10 | answer from the given plant notes, cite `[KB-xx]` |
| refusal | 3 | say "I don't have a note on that" — no hallucination |
| committee | 3 | reason across 2-day/28-day strength, cost, CO2 → verdict |
| domain | 8 | universal concrete engineering (w/c, slag, packing, cure) |
| parse | 3 | natural-language change → structured mix JSON |

Design: facts stay in the swappable RAG knowledge base; fine-tuning teaches
**behavior and voice** (ground, cite, refuse, reason), not memorized plant facts.

## Run order (next session)
1. Upload `mixmind_sft.jsonl` + `train_lora.py` to the notebook.
2. `%pip install -q peft`, restart kernel.
3. Smoke test: set `MAX_STEPS=2` in `train_lora.py`, run — catch any ROCm/peft issue cheaply.
4. Full run: `MAX_STEPS=None`, watch loss fall over 3 epochs.
5. Eval: compare base vs fine-tuned on the citation set + domain questions (Fireworks as judge for the write-up).

## Confidentiality
No company name/address/real recipe kg. Plant tricks are the generic shop-floor kind
cleared for public use; mix numbers are illustrative.
