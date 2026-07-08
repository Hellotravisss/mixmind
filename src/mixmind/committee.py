"""
Mix Committee — a panel of AI specialists that debates a recipe change.

Each role is grounded in real numbers: strength from the trained model
(R2~=0.91), cost and CO2 from the deterministic tools. The LLM writes the
minutes and the verdict; it does not invent the numbers.

Roles mirror a real plant's quality org:
  - Standard : 28-day strength vs spec, packing
  - QC       : early (2-day) strength vs the demould spec  (the skeptic)
  - Cost     : the $ change
  - Carbon   : the CO2 change
"""
from __future__ import annotations
import json
import re
from dataclasses import dataclass, field

from .llm import LLM
from .strength import StrengthModel
from .tools import Mix, cost, co2, water_cement

SPEC = {"demould_2day": 12.0, "min_28day": 28.0}   # MPa

SYSTEM = (
    "You are the Mix Committee for a concrete paver plant. Strength numbers come from a "
    "gradient-boosting model trained on 1030 real lab tests (R2=0.91). Four experts debate "
    "the change, each grounded in the numbers below. Give short minutes — one paragraph per "
    "role — then a VERDICT line (APPROVED / APPROVED WITH CONDITIONS / REJECTED).\n"
    "- Standard Officer: packing and 28-day strength vs the spec floor.\n"
    "- QC Officer (skeptic): 2-day strength vs the demould spec.\n"
    "- Cost Officer: the $ change.\n"
    "- Carbon Officer: the CO2 change (cement ~0.9, slag ~0.02 kg CO2/kg).\n"
    "Ground every claim in the numbers and the SPEC. Be concise."
)


@dataclass
class Review:
    baseline: Mix
    proposed: Mix
    numbers: dict = field(default_factory=dict)
    minutes: str = ""


class Committee:
    def __init__(self, llm: LLM, strength: StrengthModel) -> None:
        self.llm = llm
        self.strength = strength

    def _card(self, m: Mix) -> dict:
        return {
            "cost": cost(m), "co2": co2(m), "wc": round(water_cement(m), 3),
            "s2": self.strength.predict(m, 2), "s28": self.strength.predict(m, 28),
        }

    def review(self, baseline: Mix, proposed: Mix) -> Review:
        b, p = self._card(baseline), self._card(proposed)
        facts = (
            f"SPEC: demould >= {SPEC['demould_2day']} MPa at 2 days; 28-day floor "
            f"= {SPEC['min_28day']} MPa.\n"
            f"BASELINE {baseline} | cost ${b['cost']} | CO2 {b['co2']}kg | w/c {b['wc']} "
            f"| 2-day {b['s2']} | 28-day {b['s28']} MPa\n"
            f"PROPOSED {proposed} | cost ${p['cost']} | CO2 {p['co2']}kg | w/c {p['wc']} "
            f"| 2-day {p['s2']} | 28-day {p['s28']} MPa"
        )
        minutes = self.llm.generate(
            [{"role": "system", "content": SYSTEM},
             {"role": "user", "content": "Review this proposed mix change.\n\n" + facts}],
            max_new_tokens=520)
        return Review(baseline, proposed, {"baseline": b, "proposed": p}, minutes)

    def parse_request(self, baseline: Mix, request: str) -> Mix:
        """Turn a natural-language change into a concrete mix via the LLM."""
        prompt = (
            f"Baseline paver mix in kg/m3: {json.dumps(baseline)}. The operator asks: "
            f"'{request}'. Return ONLY a JSON object for the new mix using exactly these keys "
            f"(cement, slag, sand, chips, water), numbers only, applying the change. No prose.")
        txt = self.llm.generate([{"role": "user", "content": prompt}], max_new_tokens=120)
        return json.loads(re.search(r"\{[^}]*\}", txt).group(0))
