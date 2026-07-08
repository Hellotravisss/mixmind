"""
MixMind SFT dataset builder.

Emits `mixmind_sft.jsonl` — instruction data to LoRA-fine-tune Gemma 4 into a
plant-floor assistant. Run:  python build_dataset.py

Design (matches our architecture — RAG for facts, fine-tune for behavior/voice):
  1. GROUNDED  — question + retrieved plant notes -> concise cited answer.
                 Teaches "ground in the given notes, cite [KB-xx]" — NOT to memorize
                 plant facts (those stay in the swappable knowledge base).
  2. REFUSAL   — notes don't cover it -> "I don't have a note on that." (no hallucination)
  3. COMMITTEE — a mix change + computed numbers -> 4-role minutes + verdict.
                 Teaches the concrete cost/strength/CO2 tradeoff reasoning.
  4. DOMAIN    — universal concrete engineering Q&A (parametric knowledge is fine here).
  5. PARSE     — natural-language change + baseline -> structured mix JSON.

Confidentiality: no company name/address/real recipe kg. Plant tricks are the
generic shop-floor kind Travis cleared for public use; mix numbers are illustrative.
"""
import json

SYSTEM = (
    "You are MixMind, a plant-floor assistant for a concrete paver plant. "
    "When plant notes are provided, answer only from them and cite the note id in square brackets like [KB-07]; "
    "if the notes do not cover the question, say you don't have a note on that and never invent plant-specific facts. "
    "For general concrete engineering, answer concisely and correctly. "
    "When reviewing a mix change, reason like a plant committee across 2-day demould strength, 28-day strength, "
    "packing, cost, and CO2, then give a clear verdict."
)

# ---------------------------------------------------------------- 1. GROUNDED
# (question, note_id, note_text, answer)
GROUNDED = [
    ("The cement silo isn't feeding — what do I do?", "KB-07",
     "If the cement or sand silos stop feeding, a few firm hits near the outlet with a rubber mallet usually breaks the bridge. If cement still won't drop, open the inspection cover near the base to clear it. Lock out the feed first.",
     "Give a few firm hits near the outlet with a rubber mallet to break the bridge [KB-07]. If it still won't drop, lock out the feed first, then open the inspection cover near the base and clear it [KB-07]."),
    ("The bricks curl on one edge as they come off the press.", "KB-05",
     "A slight curl on one edge straight off the press usually means the base mix is too wet - lower the water a touch on the next batch.",
     "A curled edge off the press usually means the base mix is too wet — lower the water a touch on the next batch [KB-05]."),
    ("It rained last night and the sand feels soaked. What should I watch for?", "KB-06",
     "Low sand moisture: add water at the mixer. High sand moisture (common after rain, sand stored outdoors): you can't pull water back out, so you may have to stop and let it drain, which is costly. Avoid scooping from puddles when loading the silo.",
     "You can't pull the water back out of soaked sand, so you may have to stop and let it drain — which is costly [KB-06]. When loading the silo, avoid scooping from puddles [KB-06]."),
    ("The stone gate stopped letting aggregate through.", "KB-08",
     "If the stone/aggregate gate stops flowing, it's almost always a physical blockage at the outlet - check and clear it rather than forcing the gate.",
     "That's almost always a physical blockage at the outlet — check and clear the outlet rather than forcing the gate [KB-08]."),
    ("Our density readings have been coming out high.", "KB-03",
     "For a valid density reading the product must be fully submerged in the dunk tank. In hot weather top up the tank before the first test. Clear settled sludge from the tank floor regularly or it throws the reading.",
     "Make sure the product is fully submerged, and clear any settled sludge from the tank floor — buildup throws the reading high [KB-03]. In hot weather, top up the tank before the first test [KB-03]."),
    ("The colour came out darker than the sample board.", "KB-04",
     "If a batch is lighter or darker than the standard swatch, flag QC before running the pallet; QC nudges the pigment ratio rather than scrapping the batch.",
     "Flag QC before you run the pallet — they'll nudge the pigment ratio rather than scrap the batch [KB-04]."),
    ("There's sand and stone piling up on the cement scale.", "KB-09",
     "Sand and stone that build up on the cement scale platform throw off the batch weight. Wipe the scale clean whenever you see debris on it.",
     "That debris throws off the batch weight — wipe the scale clean whenever you see it [KB-09]."),
    ("How do I stop the last colour contaminating the next one after a washout?", "KB-10",
     "When washing out the mixer, tap along the inlet pipe - leftover cement or pigment hides there and contaminates the next colour.",
     "Tap along the inlet pipe during washout — leftover cement or pigment hides there and carries into the next colour [KB-10]."),
    ("Winter batches are coming out weak early on.", "KB-12",
     "If early strength is low in winter, check the cure area temperature first - cold spots near the door slow hydration. Rotate racks or extend cure time before touching the mix.",
     "Check the cure area temperature first — cold spots near the door slow hydration. Rotate racks or extend cure time before you touch the mix [KB-12]."),
    ("Before I open the silo cover to clear a blockage, anything I should do?", "KB-11",
     "Before opening any silo inspection cover or reaching into a hopper, lock out the feed and confirm the auger is stopped - material can drop or the auger can turn without warning.",
     "Lock out the feed and confirm the auger is stopped before you open the cover — material can drop or the auger can turn without warning [KB-11]."),
]

# ---------------------------------------------------------------- 2. REFUSAL
# (question, note_id_shown, note_text_shown) — notes present but do NOT answer it
REFUSAL = [
    ("What is the current market price of grey cement?", "KB-07",
     "If the cement or sand silos stop feeding, a few firm hits near the outlet with a rubber mallet usually breaks the bridge."),
    ("How many pallets did we ship last Tuesday?", "KB-03",
     "For a valid density reading the product must be fully submerged in the dunk tank."),
    ("What's the WiFi password in the break room?", "KB-10",
     "When washing out the mixer, tap along the inlet pipe - leftover cement or pigment hides there."),
]

# ---------------------------------------------------------------- 3. COMMITTEE
# (request, facts_block, minutes_and_verdict)
COMMITTEE = [
    ("Replace about 20% of the cement with slag and swap some sand for chips to cut cost and CO2.",
     "SPEC: 2-day >= 12 MPa (demould), 28-day >= 28 MPa.\n"
     "BASELINE  cement 320, slag 0, sand 780, chips 1000, water 160 | cost $90.4 | CO2 305.8kg | 2-day 15.7 | 28-day 51.8 MPa\n"
     "PROPOSED  cement 256, slag 64, sand 680, chips 1100, water 160 | cost $88.2 | CO2 249.5kg | 2-day 12.7 | 28-day 46.3 MPa",
     "Standard: 28-day 46.3 MPa holds a comfortable margin over the 28.0 floor; slag and the higher chip-to-sand ratio preserve packing, though w/c rises to about 0.63.\n"
     "QC: 2-day is only 12.7 MPa — it clears the 12.0 demould spec but the buffer is slim, and the model is R2=0.91 not 1.0, so a moisture swing could risk demould.\n"
     "Cost: unit cost falls $90.4 -> $88.2.\n"
     "Carbon: CO2 drops 305.8 -> 249.5 kg per batch, about 18%.\n"
     "VERDICT: APPROVED WITH CONDITIONS — run a 1-week pilot and monitor actual 2-day demould success before full-scale."),
    ("Cut cement, add slag, shift some sand to chips, and keep the water/cement ratio steady.",
     "SPEC: 2-day >= 12 MPa (demould), 28-day >= 28 MPa.\n"
     "BASELINE  cement 320, slag 0, sand 780, chips 1000, water 160 | cost $90.4 | CO2 305.8kg | 2-day 15.7 | 28-day 51.8 MPa\n"
     "PROPOSED  cement 260, slag 60, sand 730, chips 1050, water 155 | cost $87.9 | CO2 253.0kg | 2-day 16.1 | 28-day 52.6 MPa",
     "Standard: 28-day rises to 52.6 MPa, above the floor; lower w/c and better packing carry the strength despite less cement.\n"
     "QC: 2-day 16.1 MPa clears the 12.0 demould spec with a healthy margin.\n"
     "Cost: unit cost falls $90.4 -> $87.9.\n"
     "Carbon: CO2 drops 305.8 -> 253.0 kg, about 17%.\n"
     "VERDICT: APPROVED — cheaper, lower carbon, and strength holds or improves on every axis."),
    ("Push it hard — replace 45% of the cement with slag and add water to keep it workable.",
     "SPEC: 2-day >= 12 MPa (demould), 28-day >= 28 MPa.\n"
     "BASELINE  cement 320, slag 0, sand 780, chips 1000, water 160 | cost $90.4 | CO2 305.8kg | 2-day 15.7 | 28-day 51.8 MPa\n"
     "PROPOSED  cement 180, slag 150, sand 730, chips 1050, water 175 | cost $84.8 | CO2 182.8kg | 2-day 8.0 | 28-day 36.0 MPa",
     "Standard: 28-day meets the floor at 36.0 MPa, but w/c jumps to about 0.97 — the high water content risks long-term durability and surface finish.\n"
     "QC: 2-day is 8.0 MPa, critically short of the 12.0 demould spec; this risks mold sticking and line delays. I cannot sign off.\n"
     "Cost: biggest saving on the board, $90.4 -> $84.8.\n"
     "Carbon: deepest cut, 305.8 -> 182.8 kg, about 40%.\n"
     "VERDICT: REJECTED — it is the cheapest and greenest option, but the 2-day strength fails the demould spec. Safety over savings."),
]

# ---------------------------------------------------------------- 4. DOMAIN QA
DOMAIN = [
    ("Why does a lower water-to-cement ratio increase concrete strength?",
     "A lower water-to-cement ratio leaves less excess water in the paste. As the cement hydrates it forms a denser calcium-silicate-hydrate gel with fewer capillary pores, so the hardened matrix is more compact and stronger."),
    ("What does slag do to concrete strength over time?",
     "Slag (ground granulated blast-furnace slag) reacts more slowly than cement, so early strength — say at 1-2 days — is lower. But it keeps reacting, and by 28 days and beyond the strength usually catches up and often exceeds a plain cement mix, with better long-term durability."),
    ("Why replace part of the cement with slag at all?",
     "Two reasons: cost and carbon. Slag is cheaper than cement, and its embodied CO2 is near zero versus roughly 0.9 kg CO2 per kg of cement, so a partial replacement cuts both cost and carbon. The trade-off is slower early strength."),
    ("Why can swapping some fine sand for coarse chips increase strength?",
     "A well-graded coarse aggregate skeleton packs more densely and lowers the water demand of the mix. Better particle packing with less paste needed can hold or even raise strength while using less cement."),
    ("What early strength do pavers usually need, and why does it matter?",
     "Pavers need enough early strength — often around 12 MPa at demould age — to be handled and shipped without cracking or edge chipping. If early strength is too low the units stick in the mold or break during handling, causing scrap and line delays, even if the 28-day strength would have been fine."),
    ("What's the risk of too much water in the mix besides low strength?",
     "Beyond lower strength, excess water raises the water-to-cement ratio, which increases capillary porosity — hurting long-term durability, freeze-thaw resistance, and surface finish. It can also cause bleeding and a curled or weak top edge on freshly pressed units."),
    ("How does cure temperature affect early strength?",
     "Hydration slows in the cold, so cool cure conditions delay early strength gain. Cold spots — like near a kiln door — can leave some units weak while others are fine. Extending cure time or evening out the temperature helps before changing the mix."),
    ("Roughly how much CO2 comes from cement versus slag?",
     "Cement carries roughly 0.9 kg of embodied CO2 per kg, mostly from calcination and kiln fuel. Slag is a blast-furnace byproduct, so its embodied CO2 is close to zero. Aggregate and sand are low as well. That's why cutting cement is the main lever for lowering a mix's carbon."),
]

# ---------------------------------------------------------------- 5. PARSE
# (baseline_json, request, new_mix_json)
PARSE = [
    ('{"cement": 320, "slag": 0, "sand": 780, "chips": 1000, "water": 160}',
     "Replace about 20% of the cement with slag.",
     '{"cement": 256, "slag": 64, "sand": 780, "chips": 1000, "water": 160}'),
    ('{"cement": 320, "slag": 0, "sand": 780, "chips": 1000, "water": 160}',
     "Cut cement by 60 and swap 50 of the sand over to chips.",
     '{"cement": 260, "slag": 0, "sand": 730, "chips": 1050, "water": 160}'),
    ('{"cement": 300, "slag": 0, "sand": 800, "chips": 950, "water": 150}',
     "Replace a third of the cement with slag and drop the water by 5.",
     '{"cement": 200, "slag": 100, "sand": 800, "chips": 950, "water": 145}'),
]


# ---------------------------------------------------------------- EXTRA (expansion)
# Paraphrase variants teach the "ground + cite" behaviour across phrasings.
GROUNDED += [
    ("Nothing is coming out of the grey-cement silo.", "KB-07",
     "If the cement or sand silos stop feeding, a few firm hits near the outlet with a rubber mallet usually breaks the bridge. If cement still won't drop, open the inspection cover near the base to clear it. Lock out the feed first.",
     "Hit near the outlet a few times with a rubber mallet to break the bridge [KB-07]. If it still won't drop, lock out the feed and open the base inspection cover to clear it [KB-07]."),
    ("Fresh pavers are curling up at one edge.", "KB-05",
     "A slight curl on one edge straight off the press usually means the base mix is too wet - lower the water a touch on the next batch.",
     "That curl usually means the base mix is too wet — take the water down a touch next batch [KB-05]."),
    ("The batch weight looks off — what should I check?", "KB-09",
     "Sand and stone that build up on the cement scale platform throw off the batch weight. Wipe the scale clean whenever you see debris on it.",
     "Check the cement scale for sand or stone buildup — that throws the batch weight off. Wipe it clean [KB-09]."),
    ("How do I keep the previous colour out of the next batch?", "KB-10",
     "When washing out the mixer, tap along the inlet pipe - leftover cement or pigment hides there and contaminates the next colour.",
     "During washout, tap along the inlet pipe — leftover pigment hides there and carries into the next colour [KB-10]."),
    ("The density numbers seem too high today.", "KB-03",
     "For a valid density reading the product must be fully submerged in the dunk tank. Clear settled sludge from the tank floor regularly or it throws the reading.",
     "Check the dunk tank — the product must be fully submerged, and settled sludge on the floor throws the reading high. Clear it [KB-03]."),
]
REFUSAL += [
    ("Who is on shift tomorrow morning?", "KB-11",
     "Before opening any silo inspection cover or reaching into a hopper, lock out the feed and confirm the auger is stopped."),
    ("What's our target output for this quarter?", "KB-04",
     "If a batch is lighter or darker than the standard swatch, flag QC before running the pallet."),
]
DOMAIN += [
    ("What is the water-to-cement ratio and why does it matter?",
     "It's the mass of water divided by the mass of cement in the mix. It's the single biggest lever on strength and durability: lower ratios give denser, stronger, more durable concrete; higher ratios add workability but leave more capillary pores and weaken the hardened matrix."),
    ("Does adding coarse aggregate always improve strength?",
     "Not always — it helps up to a point. A well-graded coarse skeleton improves packing and lowers water demand, which can raise strength. But too much coarse aggregate, or poor grading, leaves gaps the paste can't fill and can hurt strength and finish."),
    ("What is embodied carbon in concrete?",
     "The CO2 emitted to produce the materials in the mix. Cement dominates it — roughly 0.9 kg CO2 per kg, from calcination and kiln fuel. Supplementary materials like slag and fly ash are byproducts with near-zero embodied carbon, so replacing cement with them is the main way to lower a mix's footprint."),
    ("Why do pavers use a low-water, dry-cast mix?",
     "Dry-cast (zero-slump) mixes are pressed and vibrated in a machine and demoulded immediately, so they need very little water and enough green strength to hold their shape. That's different from wet-cast concrete, which is poured and flows into forms."),
    ("What does 'demould strength' mean?",
     "The compressive strength the product needs at the age it's removed from the mold and handled — often a day or two old. If it's too low the unit sticks, slumps, or chips during demould and handling, causing scrap, regardless of what the 28-day strength would be."),
    ("Can fly ash be used like slag to cut cement?",
     "Yes — fly ash is another supplementary cementitious material. Like slag it reacts more slowly, trimming early strength but improving long-term strength and durability, and it lowers cost and embodied carbon. The exact effect depends on the ash and dosage."),
]
PARSE += [
    ('{"cement": 320, "slag": 0, "sand": 780, "chips": 1000, "water": 160}',
     "Bump the water down by 10 and add 40 kg of slag.",
     '{"cement": 320, "slag": 40, "sand": 780, "chips": 1000, "water": 150}'),
    ('{"cement": 280, "slag": 40, "sand": 760, "chips": 1020, "water": 158}',
     "Take 30 kg out of the cement and put it into slag.",
     '{"cement": 250, "slag": 70, "sand": 760, "chips": 1020, "water": 158}'),
]


def ex(user, assistant):
    return {"messages": [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": user},
        {"role": "assistant", "content": assistant},
    ]}


def build():
    rows = []
    for q, kid, note, ans in GROUNDED:
        rows.append(ex(f"Plant notes:\n[{kid}] {note}\n\nQuestion: {q}", ans))
    for q, kid, note in REFUSAL:
        rows.append(ex(f"Plant notes:\n[{kid}] {note}\n\nQuestion: {q}",
                       "I don't have a note on that."))
    for req, facts, mins in COMMITTEE:
        rows.append(ex(f"Review this proposed mix change.\nRequest: {req}\n\n{facts}", mins))
    for q, a in DOMAIN:
        rows.append(ex(q, a))
    for base, req, new in PARSE:
        rows.append(ex(f"Baseline mix (kg/m3): {base}\nRequest: {req}\n"
                       "Return only the new mix as JSON with the same keys.", new))
    return rows


if __name__ == "__main__":
    rows = build()
    with open("mixmind_sft.jsonl", "w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    from collections import Counter
    print(f"Wrote {len(rows)} examples to mixmind_sft.jsonl")
    print("Breakdown:",
          dict(Counter(["grounded"]*len(GROUNDED)+["refusal"]*len(REFUSAL)
                       +["committee"]*len(COMMITTEE)+["domain"]*len(DOMAIN)+["parse"]*len(PARSE))))
