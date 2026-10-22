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
