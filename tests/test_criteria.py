import json

from trial_reach import criteria as cr


def reply(items):
    return json.dumps({"criteria": items})


def test_parse_keeps_valid_drops_invalid_and_counts():
    raw = reply([
        {"type": "inclusion", "variable": "age", "operator": ">=", "value": 18, "unit": "years"},
        {"type": "exclusion", "variable": "pregnancy_or_lactation", "operator": "present", "value": None, "unit": None},
        {"type": "exclusion", "variable": "made_up", "operator": "present", "value": None, "unit": None},
        {"type": "inclusion", "variable": "bmi", "operator": ">=", "value": "high", "unit": None},
        "not an object",
    ])
    out, dropped = cr.parse(raw)
    # out-of-vocabulary variable and non-numeric threshold are kept (as other / value None); only bad types and non-objects drop
    assert [c.variable for c in out] == ["age", "pregnancy_or_lactation", "other", "bmi"] and dropped == 1
    assert out[0].value == 18.0 and out[1].value is None and out[3].value is None
    assert [c.computable for c in out] == [True, True, False, False]


def test_invalid_type_is_dropped_and_other_stays_in_denominator():
    out, dropped = cr.parse(reply([
        {"type": "maybe", "variable": "age", "operator": ">=", "value": 18, "unit": None},
        {"type": "inclusion", "variable": "consent", "operator": "present", "value": None, "unit": None},
        {"type": "inclusion", "variable": "age", "operator": ">=", "value": 18, "unit": "years"},
    ]))
    assert dropped == 1 and len(out) == 2 and cr.computable_fraction(out) == 0.5


def test_parse_unreadable_is_none_not_empty():
    assert cr.parse("no json here") == (None, 0)
    assert cr.parse('{"other": 1}') == (None, 0)
    assert cr.parse("{broken") == (None, 0)


def test_computable_flag_and_fraction():
    out, _ = cr.parse(reply([
        {"type": "inclusion", "variable": "age", "operator": ">=", "value": 40, "unit": "years"},
        {"type": "inclusion", "variable": "lvef", "operator": "<=", "value": 40, "unit": "%"},
    ]))
    assert [c.computable for c in out] == [True, False] and cr.computable_fraction(out) == 0.5
    assert cr.computable_fraction([]) is None


def test_prompt_is_hashed_truncated_and_lists_vocabulary():
    p = cr.build_prompt("Inclusion: adults.")
    assert "Inclusion: adults." in p and "egfr_or_crcl" in p and len(cr.prompt_hash()) == 64
    assert "[truncated]" in cr.build_prompt("x" * 20000)


def test_extract_uses_injected_model_only():
    seen = []

    def fake(prompt):
        seen.append(prompt)
        return reply([{"type": "inclusion", "variable": "hba1c", "operator": "<", "value": 9, "unit": "%"}])

    out, dropped = cr.extract("Invented text.", fake)
    assert len(seen) == 1 and out[0].variable == "hba1c" and dropped == 0


def test_computable_set_is_inside_vocabulary():
    assert cr.COMPUTABLE <= set(cr.VOCABULARY) and "other" not in cr.COMPUTABLE


def test_schema_enums_match_vocabulary_and_payload_uses_it():
    from trial_reach.llm import OllamaLLM

    item = cr.SCHEMA["properties"]["criteria"]["items"]["properties"]
    assert item["variable"]["enum"] == list(cr.VOCABULARY) and item["operator"]["enum"] == list(cr.OPERATORS)
    p = OllamaLLM("m", schema=cr.SCHEMA).payload("x")
    assert p["format"] == cr.SCHEMA and p["options"]["temperature"] == 0 and p["stream"] is False
    assert OllamaLLM("m").payload("x")["format"] == "json"


SAMPLE = """Inclusion Criteria:

* Age \\>18
* Referred for ablation for symptomatic
  persistent atrial fibrillation

Exclusion Criteria:

* Patients with a myocardial infarction in the previous 2 months
* LV ejection fraction < 35%
"""


def test_split_lines_uses_headers_joins_continuations():
    lines = cr.split_lines(SAMPLE)
    assert [r for r, _ in lines] == ["inclusion", "inclusion", "exclusion", "exclusion"]
    assert "persistent atrial fibrillation" in lines[1][1] and lines[2][1].startswith("Patients with")
    assert cr.split_lines("") == [] and cr.split_lines("Just one line of text")[0][0] == "inclusion"


def test_extract_lines_assigns_role_from_section_and_counts_failures():
    calls = []

    def fake(prompt):
        calls.append(prompt)
        line = prompt.split("<<<\n", 1)[1].split("\n>>>", 1)[0]  # the examples in the prompt must not drive the fake
        if "ejection" in line:
            raise RuntimeError("down")
        if "myocardial" in line:
            return json.dumps({"items": [{"variable": "prior_mi", "operator": "present", "value": None, "unit": None}]})
        return json.dumps({"items": []})

    out, failed = cr.extract_lines(SAMPLE, fake)
    assert failed == 1 and len(calls) == 4
    assert [(c.type, c.variable, c.operator) for c in out] == [("exclusion", "prior_mi", "present")]


def test_parse_line_items_out_of_vocabulary_becomes_other():
    out = cr.parse_line_items(json.dumps({"items": [{"variable": "made_up", "operator": ">=", "value": 3, "unit": None}]}), "inclusion")
    assert out[0].variable == "other" and out[0].variable_raw == "made_up" and not out[0].computable
    assert cr.parse_line_items("garbage", "inclusion") is None


def test_grounding_filters_drop_unsupported_absent_and_numbers():
    def items(line, *specs):
        raw = json.dumps({"items": [{"variable": v, "operator": op, "value": val, "unit": None} for v, op, val in specs]})
        return [(c.variable, c.operator) for c in cr.parse_line_items(raw, "exclusion", line)]

    assert items("Patients with congenital heart disease", ("heart_failure", "absent", None)) == []
    assert items("No history of stroke", ("prior_stroke", "absent", None)) == [("prior_stroke", "absent")]
    assert items("LVEF below 35%", ("lvef", "<", 35)) == [("lvef", "<")]
    assert items("Life expectancy under one year", ("life_expectancy", "<", 1)) == [("life_expectancy", "<")]
    assert items("Severe renal disease", ("egfr_or_crcl", "<", 30)) == []


def test_split_lines_unescapes_markdown_symbols():
    assert cr.split_lines("Inclusion Criteria:\n* Age \\>18")[0][1] == "Age >18"


def test_hosted_client_caps_spend_splits_prompt_and_makes_schema_safe():
    import pytest
    from types import SimpleNamespace as NS

    from trial_reach.hosted import HostedLLM, SpendCapExceeded, hosted_schema

    sch = hosted_schema(cr.LINE_SCHEMA)
    item = sch["properties"]["items"]
    assert "maxItems" not in item and item["items"]["additionalProperties"] is False
    assert item["items"]["properties"]["value"] == {"anyOf": [{"type": "number"}, {"type": "null"}]}
    assert cr.LINE_SCHEMA["properties"]["items"]["maxItems"] == 4  # original untouched

    seen = []

    class Fake:
        class messages:
            @staticmethod
            def create(**kw):
                seen.append(kw)
                return NS(content=[NS(type="text", text='{"items": []}')],
                          usage=NS(input_tokens=1_000_000, output_tokens=0, cache_read_input_tokens=0, cache_creation_input_tokens=0))

    llm = HostedLLM("claude-haiku-5-5", cr.LINE_SCHEMA, max_cost_usd=0.15, client=Fake)
    prompt = cr.build_line_prompt("exclusion", "Prior stroke")
    assert llm(prompt) == '{"items": []}'
    kw = seen[0]
    assert "Prior stroke" in kw["messages"][0]["content"] and "Prior stroke" not in kw["system"][0]["text"]
    assert "temperature" not in kw and kw["system"][0]["cache_control"] == {"type": "ephemeral"}
    assert llm.cost == pytest.approx(0.10)
    llm(prompt)  # second call brings the estimate to 0.20 which is over the cap
    with pytest.raises(SpendCapExceeded):
        llm(prompt)
