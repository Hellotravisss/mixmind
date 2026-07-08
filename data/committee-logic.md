# MixMind — Mix Committee Logic (public; general concrete engineering)

> How the multi-agent "Mix Committee" debates a cost/strength change. General engineering
> reasoning (no confidential plant data). Grounded in Travis's shop-floor intuition + standard
> concrete science. Powers the committee agents' positions.

## Scenario: "Can I use less cement in this paver mix and keep the strength?"

### 配方标准官 · Recipe/Standard  (tools: strength_model + packing_calc)
Proposes the levers that cut cost *without* necessarily losing strength:
- **Swap some fine sand → well-graded coarse aggregate (chips).** Better particle packing =
  denser skeleton + lower water demand → strength can hold or **increase** while cost drops.
  (Cite `packing_calc` / Fuller curve.)
- **Replace ~20% of cement with slag (GGBS).** Cheaper, and see the strength note below.
- Predicts resulting strength with `strength_model`.

### QC 把关官 · Donny  (thresholds / risk — the skeptic)
Pushes back on the real risks:
- **Early strength.** Slag reacts slowly → **48 h / early strength drops**, even though 28-day is
  fine. This matters for **demould, handling, shipping schedule**. Gate: don't ship if predicted
  early strength < demould threshold.
- Less cement overall → confirm 28-day still clears spec with margin.
- Watch the **moisture window / consistency** if the aggregate ratio changes.

### 用量审计官 · Luis  (usage / reconciliation)
- Confirms the new mix's material tonnage vs plan: cement down, slag + chips up.
- Flags if predicted usage vs actual would drift (the reconciliation catch).

### 成本碳排官 · Cost/CO2
- Less cement + more cheap chips + slag = **lower $ AND lower CO2.**
  Cement ≈ **0.9 kg CO2/kg**; slag ≈ **near zero**; aggregate low.
- Quantifies **$ saved per 1000 units** and **kg CO2 saved**. This is the decarbonization headline.

## The tension the committee resolves
Cost/CO2 officers + Standard officer push **for** the change; QC pushes back on **early-strength
risk** (especially with slag). Typical resolution:

> "**~20% slag + partial sand→chips swap:** 28-day strength meets/exceeds spec and cuts cost + CO2.
> **But 48 h strength drops** — so it's fine **if** your demould/cure schedule can absorb the slower
> early gain. If not, reduce slag % or extend cure."

## Why this makes a great demo moment
The **slag early-vs-late strength crossover** is non-obvious: a naive tool (or generic AI) would
reject slag for low 48 h strength. The committee **explains the 30-day crossover + the carbon win** —
showing reasoning a single model spitting one number would miss. That's the value of the debate.

---
*Source intuitions: Travis (operator) — validated against standard concrete science (packing
density; GGBS latent-hydraulic behaviour; embodied-carbon factors). Cleared for public use.*
