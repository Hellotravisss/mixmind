"""
MixMind local API server — serves the self-hosted Gemma 4 brain over HTTP so the
web demo (or anything else, in the plant) can call it. Nothing leaves the machine.

Run on the AMD notebook (after fine-tuning):
    PYTHONPATH=src python -m serve --adapter data/finetune/mixmind-gemma4-lora
    # then point the web app at http://<host>:8000

Endpoints (JSON, CORS-open for the local demo):
    POST /ask     {"question": "..."}                       -> {answer, sources}
    POST /review  {"baseline": {...}, "proposed": {...}}     -> {numbers, minutes}
    POST /review  {"baseline": {...}, "request": "plain EN"} -> {numbers, minutes, proposed}
    GET  /health                                            -> {status, r2}

Stdlib only (http.server) — no FastAPI/uvicorn needed.
"""
from __future__ import annotations
import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from mixmind.llm import GemmaLLM, StubLLM
from mixmind.copilot import Copilot
from mixmind.strength import StrengthModel
from mixmind.committee import Committee

STATE: dict = {}


class Handler(BaseHTTPRequestHandler):
    def _send(self, code: int, payload: dict) -> None:
        body = json.dumps(payload).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self) -> None:
        self._send(204, {})

    def do_GET(self) -> None:
        if self.path == "/health":
            self._send(200, {"status": "ok", "r2": STATE["strength"].metrics.r2})
        else:
            self._send(404, {"error": "not found"})

    def do_POST(self) -> None:
        n = int(self.headers.get("Content-Length", 0))
        try:
            req = json.loads(self.rfile.read(n) or b"{}")
        except json.JSONDecodeError:
            return self._send(400, {"error": "invalid JSON"})

        if self.path == "/ask":
            ans = STATE["copilot"].ask(req["question"])
            return self._send(200, {"answer": ans.text,
                                    "sources": [{"id": s.id, "text": s.text} for s in ans.sources]})

        if self.path == "/review":
            cm = STATE["committee"]
            base = req["baseline"]
            proposed = req.get("proposed")
            out = {}
            if proposed is None and req.get("request"):
                proposed = cm.parse_request(base, req["request"])
                out["proposed"] = proposed
            r = cm.review(base, proposed)
            out.update({"numbers": r.numbers, "minutes": r.minutes})
            return self._send(200, out)

        self._send(404, {"error": "not found"})

    def log_message(self, *a):  # quieter logs
        return


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8000)
    ap.add_argument("--adapter", default=None, help="fine-tuned LoRA adapter path")
    ap.add_argument("--stub", action="store_true", help="no GPU (stub the LLM)")
    args = ap.parse_args()

    print("Training strength model (UCI Concrete)...")
    strength = StrengthModel()
    strength.train()
    print(f"  R2={strength.metrics.r2}")
    llm = StubLLM() if args.stub else GemmaLLM(adapter_path=args.adapter)

    STATE.update(strength=strength, copilot=Copilot(llm),
                 committee=Committee(llm, strength))

    srv = ThreadingHTTPServer(("0.0.0.0", args.port), Handler)
    print(f"MixMind serving on http://0.0.0.0:{args.port}  (data stays on this machine)")
    srv.serve_forever()


if __name__ == "__main__":
    main()
