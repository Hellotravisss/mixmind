# MixMind

**A plant-private concrete-mix AI — the R&D department a plant can't afford to hire, running on its own hardware.**

Concrete is the most-consumed material on Earth and roughly **8% of global CO₂**. Yet mix-design know-how sits inside a handful of corporate labs. MixMind puts a research-grade mix assistant on a plant's **own AMD GPU** — nothing leaves the building — so any producer can cut cement (= cost = carbon) with real engineering judgment.

Built for the **AMD Developer Hackathon: ACT II** (Unicorn / open-innovation track) by a machine operator at a North American precast plant.

---

## What it does

**1 · Floor Copilot** — answers plant-floor questions from the plant's *own* notes, cites the source, and refuses when it doesn't know.

> **Q:** "Material is stuck in the cement silo — what do I do?"
> **A:** "Give a few firm hits near the outlet with a rubber mallet to break the bridge **[KB-07]**. If it still won't drop, lock out the feed first, then open the inspection cover near the base **[KB-07]**."
>
> **Q:** "What is the current market price of grey cement?"
> **A:** "I don't have a note on that." *(no hallucination)*

**2 · Mix Committee** — a panel of four AI specialists debates a recipe change, each grounded in real numbers, and returns minutes plus a verdict:

| Proposed change | 28-day | 2-day (demould ≥ 12) | Cost | CO₂ | Verdict |
|---|---|---|---|---|---|
| Sweet spot | 52.6 MPa | 16.1 ✓ | $87.9 | −17% | **APPROVED** |
| 20% cement → slag | 46.3 MPa | 12.7 ✓ (tight) | $88.2 | −18% | **APPROVED / CONDITIONS** |
| Aggressive 45% slag | 36.0 MPa | **8.0 ✗** | $84.8 | −40% | **REJECTED** |

The system will **reject the cheapest, greenest option** when early strength fails the demould spec — the strength model learned slag's early-strength penalty from real data. Judgment, not a yes-man.

You can also ask in plain English — *"replace about 20% of the cement with slag and swap some sand for chips"* — and the model builds the exact mix, then the committee reviews it.

---

## Why it runs on AMD

The whole thesis is **data sovereignty**: a plant will not send its recipes to a third-party API. So the model must be **self-hosted**.

- **Brain:** Gemma 4 (12B), loaded and run **locally on an AMD Radeon GPU (ROCm)** — fine-tuned on plant knowledge with a LoRA adapter. *(Runs on ~$4k of AMD hardware, not a $200k data-center box — that's what makes "private AI" affordable for a small plant.)*
- **Strength model:** gradient-boosting regressor on the public **UCI Concrete Compressive Strength** dataset (Yeh 1998, 1,030 lab tests). **Held-out R² = 0.910, MAE = 3.46 MPa.**
- Everything the Copilot cites and every number the Committee argues stays on the plant's machine.

## Hard numbers

| Metric | Value |
|---|---|
| Strength model held-out R² | **0.910** (MAE 3.46 MPa) |
| CO₂ cut on the approved mix | **−17.3%**, strength held |
| Recipe data sent off-site | **0 bytes** |

---

## Architecture

```
Operator (plain English)
      │
      ▼
Gemma 4 — fine-tuned, self-hosted on AMD Radeon (ROCm)
      │
      ├── Floor Copilot ──── retrieval over the plant's notes → grounded, cited answer
      │
      └── Mix Committee ──── Standard · QC · Cost · Carbon  (each grounded in a real tool)
                              ├── strength model   (UCI-trained GBM, R²=0.91)
                              └── cost / CO₂        (deterministic arithmetic)
                              → minutes + verdict
```

Facts live in a **swappable knowledge base** (retrieval); fine-tuning teaches **behavior and voice** (ground, cite, refuse, reason). Point the same model at a different plant's notes and it serves that plant.

---

## Quickstart

```bash
pip install -r requirements.txt

# Deterministic parts only — no GPU (strength model + tools + retrieval):
PYTHONPATH=src python -m mixmind.demo --stub

# Full run with the self-hosted Gemma 4 brain (AMD ROCm GPU):
PYTHONPATH=src python -m mixmind.demo
# ...with the fine-tuned adapter:
PYTHONPATH=src python -m mixmind.demo --adapter data/finetune/mixmind-gemma4-lora
```

Fine-tune the brain on the plant SFT set (see [`data/finetune/`](data/finetune/)):

```bash
cd data/finetune && python build_dataset.py   # regenerate the training data
# then run train_lora.py on the AMD notebook (LoRA via PEFT)
```

The interactive web demo is a single self-contained file: [`web/index.html`](web/index.html).

---

## Repo layout

| Path | What |
|---|---|
| `src/mixmind/` | the product — knowledge, retrieval, copilot, strength model, committee, tools |
| `web/index.html` | interactive demo (Floor Copilot + Mix Committee), self-contained |
| `data/finetune/` | SFT dataset builder + LoRA training script (PEFT) |
| `data/*.md` | illustrative knowledge base + committee logic |

## Honest boundary

The strength model is trained on wet-cast lab data; dry-cast pavers differ, so predictions are **directional, not certified**. Every Copilot answer is grounded in the plant's own notes; load-bearing changes always go to a qualified engineer.
**We ground every answer, and we predict directions — we don't certify mixes.**

## Tech

Gemma 4 · PyTorch + ROCm on AMD Radeon · PEFT (LoRA) · scikit-learn · UCI Concrete (Yeh 1998) · Fireworks AI (eval judge).

> Yeh, I-C. (1998). *Modeling of strength of high-performance concrete using artificial neural networks.* Cement and Concrete Research, 28(12), 1797–1808.
