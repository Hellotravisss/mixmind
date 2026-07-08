"""
LLM backend — the plant-private brain.

Gemma 4, loaded and run locally on the plant's own AMD GPU (ROCm). Nothing
leaves the building. Optionally loads a LoRA adapter fine-tuned on plant data.

Requires a ROCm PyTorch + transformers>=5.13 environment (what the AMD notebook
ships). `StubLLM` lets the rest of the package be imported and tested on a
machine without a GPU.
"""
from __future__ import annotations

Messages = list[dict[str, str]]


class LLM:
    def generate(self, messages: Messages, max_new_tokens: int = 400) -> str:
        raise NotImplementedError


class GemmaLLM(LLM):
    """Self-hosted Gemma 4 on an AMD GPU. `adapter_path` loads a LoRA adapter."""

    def __init__(self, model: str = "google/gemma-4-12B-it",
                 adapter_path: str | None = None) -> None:
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer
        self.torch = torch
        self.tok = AutoTokenizer.from_pretrained(model)
        self.model = AutoModelForCausalLM.from_pretrained(
            model, dtype=torch.bfloat16, device_map="cuda", attn_implementation="sdpa")
        if adapter_path:
            from peft import PeftModel
            self.model = PeftModel.from_pretrained(self.model, adapter_path)
        self.model.eval()

    def generate(self, messages: Messages, max_new_tokens: int = 400) -> str:
        ids = self.tok.apply_chat_template(
            messages, add_generation_prompt=True, return_tensors="pt",
            return_dict=True).to("cuda")
        with self.torch.no_grad():
            out = self.model.generate(**ids, max_new_tokens=max_new_tokens)
        return self.tok.decode(out[0][ids["input_ids"].shape[1]:],
                               skip_special_tokens=True).strip()


class StubLLM(LLM):
    """Deterministic placeholder so the package imports without a GPU."""

    def generate(self, messages: Messages, max_new_tokens: int = 400) -> str:
        return "[StubLLM] Connect a GemmaLLM backend (AMD GPU) for real answers."
