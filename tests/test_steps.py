"""Tests for individual processing steps"""

import pytest
from src.agents.step1_extract import extract_and_normalize
from src.agents.step2_facts import extract_ingredient_facts
from src.models import UserProfile, RiskSensitivity
from src.agents.step3_policy import convert_user_profile
from src.agents.step4_evaluate import evaluate_ingredients


def test_step1_extract():
    """Test step 1: extraction and normalization"""
    result = extract_and_normalize("sugar, flour, water, E300")

    assert result is not None
    assert len(result.original_list) == 4
    assert len(result.canonical_map) == 4
    assert result.canonical_map[3].canonical == "VITAMIN C" or result.canonical_map[3].canonical == "E300"


def test_step1_empty_input():
    """Test step 1 with empty input"""
    result = extract_and_normalize("")

    assert result is not None
    assert len(result.original_list) == 0
    assert len(result.unreadable_segments) > 0


def test_step2_facts():
    """Test step 2: ingredient facts extraction"""
    parsed = extract_and_normalize("E202, sugar, E621")
    facts = extract_ingredient_facts(parsed, locale="EU")

    assert len(facts) == 3
    # E202 should be recognized as preservative
    e202_fact = next(f for f in facts if "202" in f.canonical)
    assert e202_fact.is_additive is True


def test_step3_policy():
    """Test step 3: user policy conversion"""
    profile = UserProfile(
        goals=["eat healthy"],
        constraints=["peanut allergy", "vegan"],
        preferences=["avoid additives", "low sugar"],
        risk_sensitivity=RiskSensitivity.HIGH,
    )

    policy = convert_user_profile(profile)

    assert len(policy.hard_constraints) == 2
    assert len(policy.soft_preferences) == 2
    assert policy.risk_sensitivity == RiskSensitivity.HIGH


def test_step4_evaluation():
    """Test step 4: evaluation"""
    parsed = extract_and_normalize("milk, eggs")
    facts = extract_ingredient_facts(parsed)

    profile = UserProfile(
        constraints=["vegan"],
    )
    policy = convert_user_profile(profile)

    evaluation = evaluate_ingredients(facts, policy)

    assert evaluation is not None
    # Should flag milk and eggs for vegan constraint
    assert len(evaluation.key_reasons) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
