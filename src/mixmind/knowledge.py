"""
MixMind plant knowledge base.

Illustrative shop-floor knowledge for a concrete paver plant — the tacit,
plant-specific know-how a generic model does not have. This is the kind of note
the Copilot retrieves and cites. Swap this list per plant; the model does not
memorize these facts (they live here, in retrieval), so the same fine-tuned
model serves any plant by pointing it at that plant's notes.

No company name/address or real recipe quantities appear here — generic tricks
plus invented plant details.
"""
from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class Note:
    id: str
    category: str
    text: str


KNOWLEDGE: list[Note] = [
    Note("KB-03", "Testing",
         "For a valid density reading the product must be fully submerged in the dunk tank. "
         "In hot weather top up the tank before the first test. Clear settled sludge from the "
         "tank floor regularly or it throws the reading high."),
    Note("KB-04", "Quality",
         "If a batch is lighter or darker than the standard swatch, flag QC before running the "
         "pallet; QC nudges the pigment ratio rather than scrapping the batch."),
    Note("KB-05", "Process",
         "A slight curl on one edge straight off the press usually means the base mix is too wet "
         "- lower the water a touch on the next batch."),
    Note("KB-06", "Materials",
         "Low sand moisture: add water at the mixer. High sand moisture (common after rain, sand "
         "is stored outdoors): you cannot pull water back out, so you may have to stop and let it "
         "drain, which is costly. Avoid scooping from puddles when loading the silo."),
    Note("KB-07", "Reliability",
         "If the cement or sand silos stop feeding, a few firm hits near the outlet with a rubber "
         "mallet usually breaks the bridge. If cement still won't drop, open the inspection cover "
         "near the base and clear it. Lock out the feed first."),
    Note("KB-08", "Reliability",
         "If the stone/aggregate gate stops flowing, it's almost always a physical blockage at the "
         "outlet - check and clear it rather than forcing the gate."),
    Note("KB-09", "Quality",
         "Sand and stone that build up on the cement scale platform throw off the batch weight. "
         "Wipe the scale clean whenever you see debris on it."),
    Note("KB-10", "Maintenance",
         "When washing out the mixer, tap along the inlet pipe - leftover cement or pigment hides "
         "there and contaminates the next colour."),
    Note("KB-11", "Safety",
         "Before opening any silo inspection cover or reaching into a hopper, lock out the feed and "
         "confirm the auger is stopped - material can drop or the auger can turn without warning."),
    Note("KB-12", "Reliability",
         "If early strength is low in winter, check the cure area temperature first - cold spots "
         "near the door slow hydration. Rotate racks or extend cure time before touching the mix."),
    Note("KB-13", "Process",
         "If the press sounds like a low rumbling motorcycle during main vibration, the board or "
         "mold is lifting off the vibrating table and compaction suffers. Tune until it is an "
         "almost continuous high-pitched hum - twice the impacts, much better compaction."),
    Note("KB-14", "Process",
         "If tamperhead pressure is too high, the vibrator current (amps) during main vibration "
         "drops below its starting value - visible on the vibrator settings page. Re-tune the "
         "machine by power consumption at every product change."),
    Note("KB-15", "Process",
         "Load pressure set too high stops the table vibrating freely and makes it sway: outside "
         "stones come out more compacted and shorter than the middle. Reduce load pressure, then "
         "take back the angle and correct mold clamping pressure."),
    Note("KB-16", "Process",
         "After a height change: reduce the vibration angle in small steps (only with tamperhead "
         "pressure coming down too), then trim main vibration time in small increments. Always "
         "measure stone height on the product - the display can read high."),
    Note("KB-17", "Reference",
         "Typical press ranges: impact bar gap 0.6-0.7 mm; 2800-3000 rpm up to 80 mm product "
         "(2400-2700 rpm with angle >=120 deg above 100 mm); angle 65-90 deg by height, +20 deg if "
         "the mix runs dry; tamperhead low 15-20 / high 20-40 bar; mold clamping 2-3.5 bar. "
         "Vibration force too high = the product will not compact properly."),
]

BY_ID = {n.id: n for n in KNOWLEDGE}
