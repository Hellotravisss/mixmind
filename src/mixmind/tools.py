"""
Deterministic mix tools — cost and embodied carbon.

Not an LLM: plain arithmetic the committee agents cite so their arguments are
grounded in real numbers rather than generated text.

A mix is a dict of kg/m3 amounts: cement, slag, sand, chips, water.
Prices are illustrative $/kg. CO2 factors are public embodied-carbon values
(cement ~0.9 kg CO2/kg; slag is a blast-furnace byproduct, near zero).
"""
from __future__ import annotations

Mix = dict[str, float]

# Illustrative $/kg (public-market ballpark, not a real plant's costs)
PRICE: dict[str, float] = {
    "cement": 0.14, "slag": 0.09, "sand": 0.02, "chips": 0.03, "water": 0.0,
}

# Embodied CO2, kg per kg of material (public factors)
CO2: dict[str, float] = {
    "cement": 0.90, "slag": 0.02, "sand": 0.01, "chips": 0.01, "water": 0.0,
}


def water_cement(mix: Mix) -> float:
    return mix["water"] / mix["cement"]


def cost(mix: Mix) -> float:
    """Cost per batch, USD."""
    return round(sum(mix.get(k, 0) * p for k, p in PRICE.items()), 2)


def co2(mix: Mix) -> float:
    """Embodied CO2 per batch, kg."""
    return round(sum(mix.get(k, 0) * f for k, f in CO2.items()), 1)
