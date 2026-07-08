# MixMind — demo video script (~2:50)

**Format:** screen recording + on-screen captions. **No camera, no live voice needed.**
Voiceover is optional — either record the caption lines yourself, use an AI voice, or run
caption-only. Nothing is filmed inside a plant; no faces, no company marks.

**What you screen-record:** the web demo `web/index.html` (open it in the browser) and one or
two of the AMD notebook evidence shots (rocm-smi, Gemma answering on the GPU).

**Identity line is text only** — never point a camera at yourself or the plant.

---

| Time | On screen | Caption / voiceover |
|---|---|---|
| 0:00–0:12 | Title card: **MixMind**. Fade in the tagline. | "Concrete is the most-used material on Earth — and about 8% of global CO₂." |
| 0:12–0:22 | Text card, plain. | "The know-how to optimize a mix sits in a few corporate labs. And no plant will send its recipes to a third-party AI." |
| 0:22–0:32 | Text card → the MixMind hero. | "So we built a mix AI that runs on the plant's own AMD GPU. Nothing leaves the building. Built by a machine operator at a North American precast plant." |
| 0:32–1:00 | Screen-record **Floor Copilot**. Click "cement stuck in the silo". Answer appears with **[KB-07]** citation. | "Ask it a real floor question — it answers from the plant's own notes, and cites the source." |
| 1:00–1:12 | Click "current market price of grey cement". Answer: *"I don't have a note on that."* | "And when it doesn't know, it says so. No made-up answers." |
| 1:12–1:20 | Switch to **Mix Committee** tab. | "Now the part that saves cement." |
| 1:20–1:45 | Committee "20% cement → slag" scenario. Show composition bars, strength-vs-spec chart, cost/CO₂ tiles, then the four agent cards, then **APPROVED / CONDITIONS**. | "Four AI specialists debate a recipe change — strength, QC, cost, carbon — each grounded in a real model. Here: cheaper, 18% less CO₂, approved with a pilot condition." |
| 1:45–2:05 | Switch to **Aggressive (45% slag)**. Strength chart 2-day bar drops **below the red line**. Verdict stamps **REJECTED**. | "This one is the cheapest and greenest on the board. And it gets rejected — 2-day strength fails the demould spec. The model learned slag's early-strength penalty from real data. Judgment, not a yes-man." |
| 2:05–2:20 | Hard-numbers card (from the hero / deck): **R² 0.910 · −17% CO₂ · 0 bytes off-site**. | "Strength model: R-squared 0.91 on a thousand real lab tests. The approved mix: 17% less carbon, strength held." |
| 2:20–2:38 | Cut to the **AMD notebook evidence**: rocm-smi showing the Radeon GPU, then Gemma answering a concrete question on it. | "The brain is Gemma 4, fine-tuned and self-hosted on an AMD Radeon GPU. It runs on a few thousand dollars of hardware — not a data-center box. That's what makes private AI affordable for a small plant." |
| 2:38–2:50 | Closing card: MixMind logo + one line. | "Every plant that can't afford a research lab — gets one it can run itself. We predict directions, we don't certify mixes. That's MixMind." |

---

## Recording checklist
- [ ] Open `web/index.html`, resize the window clean (hide bookmarks bar), record at 1080p.
- [ ] Do a slow, deliberate click-through — pause on each answer/verdict so it's readable.
- [ ] Grab the two AMD shots from the notebook (rocm-smi; Gemma answering). Blur nothing sensitive — there is none.
- [ ] Keep it under 3:00. Captions large and high-contrast.
- [ ] Export 1080p MP4. Music optional, low.

## Hard rules (confidentiality)
- No footage inside a real plant, no faces, no company name/logo/address, no real recipe numbers.
- Identity = one text line: "a machine operator at a North American precast plant." Nothing more.
