from trial_reach import grouping as gp


def test_primary_group_uses_the_trials_own_conditions_in_listed_order():
    assert gp.primary_group(["Heart Failure", "Hypertension"]) == "heart_failure"
    assert gp.primary_group(["Hypertension", "Stroke"]) == "hypertension"
    assert gp.primary_group(["Acute Ischemic Stroke"]) == "stroke"
    assert gp.primary_group(["Myocardial Infarction", "Coronary Artery Disease"]) == "coronary"
    assert gp.groups_of(["Heart Failure", "Hypertension", "Stroke"]) == ["heart_failure", "hypertension", "stroke"]


def test_other_diseases_with_the_same_word_are_not_matched():
    for c in ["Pulmonary Arterial Hypertension", "Portal Hypertension", "Ocular Hypertension", "Intracranial Hypertension",
              "Pre-eclampsia", "Gestational Hypertension", "Atrial Fibrillation", "Diabetes"]:
        assert gp.primary_group([c]) is None, c
    assert gp.primary_group(["Pulmonary Hypertension", "Heart Failure"]) == "heart_failure"
    assert gp.primary_group([]) is None and gp.primary_group(None) is None
