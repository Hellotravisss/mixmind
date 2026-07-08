"""
MixMind end-to-end demo.

    python -m mixmind.demo            # real run (needs AMD GPU for Gemma)
    python -m mixmind.demo --stub     # no GPU: strength model + tools only,
                                      # LLM text is stubbed

Trains the strength model on UCI, then runs the Floor Copilot on a few real
questions and the Mix Committee on the three reference scenarios.
"""
from __future__ import annotations
import argparse

from .llm import GemmaLLM, StubLLM
from .copilot import Copilot
from .strength import StrengthModel
from .committee import Committee

BASELINE = {"cement": 320, "slag": 0, "sand": 780, "chips": 1000, "water": 160}
SCENARIOS = {
    "Sweet spot": {"cement": 260, "slag": 60, "sand": 730, "chips": 1050, "water": 155},
    "20% cement to slag": {"cement": 256, "slag": 64, "sand": 680, "chips": 1100, "water": 160},
    "Aggressive (45% slag)": {"cement": 180, "slag": 150, "sand": 730, "chips": 1050, "water": 175},
}
QUESTIONS = [
    "Material is stuck in the cement silo and won't come down — what do I do?",
    "The paver has a curled edge right off the press — what's wrong?",
    "What is the current market price of grey cement?",   # not in the notes -> honest refusal
]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stub", action="store_true", help="run without a GPU (stub the LLM)")
    ap.add_argument("--adapter", default=None, help="path to a fine-tuned LoRA adapter")
    args = ap.parse_args()

    print("Training strength model on UCI Concrete (Yeh 1998)...")
    strength = StrengthModel()
    m = strength.train()
    print(f"  held-out R2={m.r2}  MAE={m.mae} MPa\n")

    llm = StubLLM() if args.stub else GemmaLLM(adapter_path=args.adapter)

    print("=" * 70, "\nFLOOR COPILOT\n" + "=" * 70)
    copilot = Copilot(llm)
    for q in QUESTIONS:
        ans = copilot.ask(q)
        cites = ", ".join(n.id for n in ans.sources) or "—"
        print(f"\nQ: {q}\nA: {ans.text}\n   sources: {cites}")

    print("\n" + "=" * 70, "\nMIX COMMITTEE\n" + "=" * 70)
    committee = Committee(llm, strength)
    for name, proposed in SCENARIOS.items():
        print(f"\n--- {name} ---")
        review = committee.review(BASELINE, proposed)
        for k, v in review.numbers["proposed"].items():
            print(f"  {k}: {v}")
        print(review.minutes)


if __name__ == "__main__":
    main()
