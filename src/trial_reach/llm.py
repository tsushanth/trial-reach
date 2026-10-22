"""Minimal client for a locally running Ollama server. The host comes from the environment (default: this machine).

Structured output: pass a JSON schema as `schema` and the server constrains decoding to it, so enumerated fields cannot take
values outside the list. Temperature 0. Failures raise; the caller records them and never turns them into labels.
"""

from __future__ import annotations

import json
import os
import urllib.request


class OllamaLLM:
    def __init__(self, model: str, schema: dict | None = None, num_ctx: int = 8192, timeout: int = 900):
        self.model = model
        self.schema = schema
        self.num_ctx = num_ctx
        self.timeout = timeout
        self.host = os.environ.get("TRIAL_REACH_OLLAMA_HOST", "http://127.0.0.1:11434")

    def payload(self, prompt: str) -> dict:
        return {
            "model": self.model, "prompt": prompt, "stream": False, "format": self.schema or "json",
            "options": {"temperature": 0, "num_ctx": self.num_ctx},
        }

    def __call__(self, prompt: str) -> str:
        req = urllib.request.Request(self.host + "/api/generate", data=json.dumps(self.payload(prompt)).encode(),
                                     headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=self.timeout) as r:
            return json.load(r)["response"]
