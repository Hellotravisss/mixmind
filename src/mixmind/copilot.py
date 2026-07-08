"""
Floor Copilot — grounded, cited answers to plant-floor questions.

Retrieves the relevant plant notes, hands them to the LLM, and requires the
answer to stay inside them and cite the note id. If the notes don't cover the
question, it says so instead of inventing a plant-specific fact.
"""
from __future__ import annotations
from dataclasses import dataclass

from .knowledge import Note
from .llm import LLM
from .retrieval import Retriever

SYSTEM = (
    "You are MixMind, a plant-floor assistant for a concrete paver plant. Answer only "
    "from the plant notes provided and cite the note id in square brackets like [KB-07]. "
    "If the notes do not cover the question, say you don't have a note on that — never "
    "invent plant-specific facts."
)


@dataclass
class Answer:
    text: str
    sources: list[Note]


class Copilot:
    def __init__(self, llm: LLM, retriever: Retriever | None = None) -> None:
        self.llm = llm
        self.retriever = retriever or Retriever()

    def ask(self, question: str, k: int = 2) -> Answer:
        hits = self.retriever.retrieve(question, k=k)
        notes = "\n".join(f"[{n.id}] {n.text}" for n in hits)
        user = f"Plant notes:\n{notes}\n\nQuestion: {question}"
        text = self.llm.generate(
            [{"role": "system", "content": SYSTEM}, {"role": "user", "content": user}],
            max_new_tokens=220)
        return Answer(text, hits)
