"""Hosted extraction client (Anthropic API) for PUBLIC registry text only. Never send patient data through this client.

Guards: a hard spend cap (the run stops when the estimated cost reaches it), usage tally, structured output so replies always
match the schema, no sampling parameters (not accepted by the model used), and no key handling in code: the SDK reads its
credentials from the environment.
"""

from __future__ import annotations

import json

from trial_reach.criteria import SENTINEL

# $ per million tokens for claude-haiku-5-5 prompts up to 100K tokens (cache reads and writes priced at standard multiples).
PRICES = {"claude-haiku-5-5": (0.10, 0.50)}


def hosted_schema(schema: dict) -> dict:
    """Structured outputs accept a subset of JSON Schema: no maxItems, nullable via anyOf, closed objects."""
    s = json.loads(json.dumps(schema))
    items = s["properties"]["items"]
    items.pop("maxItems", None)
    props = items["items"]["properties"]
    for k in ("value", "unit"):
        t = props[k]["type"]
        props[k] = {"anyOf": [{"type": t[0]}, {"type": "null"}]}
    items["items"]["additionalProperties"] = False
    s["additionalProperties"] = False
    return s


class SpendCapExceeded(RuntimeError):
    pass


class HostedLLM:
    def __init__(self, model: str, schema: dict, max_cost_usd: float, client=None, max_tokens: int = 600):
        if model not in PRICES:
            raise ValueError(f"no price table for {model}")
        if client is None:
            import anthropic  # imported here so tests and local runs do not need the SDK or credentials

            client = anthropic.Anthropic()
        self.model, self.schema, self.cap, self.client, self.max_tokens = model, hosted_schema(schema), max_cost_usd, client, max_tokens
        self.in_tokens = self.out_tokens = self.cache_read = self.cache_write = self.calls = 0

    @property
    def cost(self) -> float:
        pi, po = PRICES[self.model]
        return (self.in_tokens * pi + self.cache_write * pi * 1.25 + self.cache_read * pi * 0.1 + self.out_tokens * po) / 1e6

    def __call__(self, prompt: str) -> str:
        if self.cost >= self.cap:
            raise SpendCapExceeded(f"estimated ${self.cost:.2f} reached the ${self.cap:.2f} cap after {self.calls} calls")
        system, _, user = prompt.partition(SENTINEL)
        r = self.client.messages.create(
            model=self.model, max_tokens=self.max_tokens,
            system=[{"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}],
            messages=[{"role": "user", "content": user}],
            thinking={"type": "disabled"},
            output_config={"effort": "low", "format": {"type": "json_schema", "schema": self.schema}},
        )
        u = r.usage
        self.calls += 1
        self.in_tokens += u.input_tokens or 0
        self.out_tokens += u.output_tokens or 0
        self.cache_read += getattr(u, "cache_read_input_tokens", 0) or 0
        self.cache_write += getattr(u, "cache_creation_input_tokens", 0) or 0
        return next((b.text for b in r.content if b.type == "text"), "")
