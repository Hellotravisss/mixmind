"""
MixMind — a plant-private concrete-mix AI.

A fine-tuned open model (Gemma 4), self-hosted on an AMD GPU, that (1) answers a
plant's own floor knowledge with citations and (2) convenes a committee of AI
specialists to review a mix change against a real strength model — cutting
cement, cost, and CO2 without the recipe leaving the building.
"""
from .knowledge import KNOWLEDGE, Note
from .retrieval import Retriever
from .llm import LLM, GemmaLLM, StubLLM
from .copilot import Copilot, Answer
from .strength import StrengthModel
from .committee import Committee, Review, SPEC
from .tools import cost, co2, water_cement

__all__ = [
    "KNOWLEDGE", "Note", "Retriever", "LLM", "GemmaLLM", "StubLLM",
    "Copilot", "Answer", "StrengthModel", "Committee", "Review", "SPEC",
    "cost", "co2", "water_cement",
]
