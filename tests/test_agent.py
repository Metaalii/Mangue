"""Tests for the main agent"""

import pytest
from src.agents import IngredientAnalysisAgent
from src.models import RiskSensitivity, Verdict


def test_agent_initialization():
    """Test agent can be initialized"""
    agent = IngredientAnalysisAgent(locale="EU")
    assert agent.locale == "EU"


def test_simple_analysis():
    """Test basic analysis works"""
    agent = IngredientAnalysisAgent()

    result = agent.analyze_simple(
        ingredients_text="sugar, flour, water",
        goals=["eat healthy"],
        constraints=[],
        preferences=["natural ingredients"],
    )

    assert result is not None
    assert result.parsed_ingredients is not None
    assert len(result.parsed_ingredients.original_list) == 3
    assert result.evaluation.verdict in [Verdict.GOOD_FIT, Verdict.MIXED_FIT, Verdict.NOT_RECOMMENDED]


def test_empty_ingredients():
    """Test handling of empty ingredient text"""
    agent = IngredientAnalysisAgent()

    result = agent.analyze_simple(
        ingredients_text="",
        goals=["test"],
    )

    assert result is not None
    assert result.evaluation.verdict == Verdict.MIXED_FIT
    assert len(result.evaluation.uncertainty_notes) > 0


def test_allergen_detection():
    """Test allergen detection in constraints"""
    agent = IngredientAnalysisAgent()

    result = agent.analyze_simple(
        ingredients_text="milk, eggs, peanuts",
        constraints=["peanut allergy"],
        risk_sensitivity=RiskSensitivity.HIGH,
    )

    assert result is not None
    # Should have key reasons about peanuts
    assert len(result.evaluation.key_reasons) > 0


def test_e_number_recognition():
    """Test E-number recognition"""
    agent = IngredientAnalysisAgent(locale="EU")

    result = agent.analyze_simple(
        ingredients_text="E300, E621, E202",
        preferences=["avoid additives"],
    )

    assert result is not None
    # All three should be recognized as additives
    additive_count = sum(1 for fact in result.ingredient_facts if fact.is_additive)
    assert additive_count >= 3


def test_vegan_constraint():
    """Test vegan dietary constraint"""
    agent = IngredientAnalysisAgent()

    result = agent.analyze_simple(
        ingredients_text="milk, eggs, honey",
        constraints=["vegan"],
    )

    assert result is not None
    # Should flag non-vegan ingredients
    assert len(result.evaluation.key_reasons) > 0
    assert result.evaluation.verdict in [Verdict.MIXED_FIT, Verdict.NOT_RECOMMENDED]


def test_json_output():
    """Test JSON serialization"""
    agent = IngredientAnalysisAgent()

    result = agent.analyze_simple(
        ingredients_text="sugar, salt",
    )

    json_output = result.to_json()
    assert json_output is not None
    assert isinstance(json_output, str)
    assert "parsed_ingredients" in json_output
    assert "ingredient_facts" in json_output
    assert "evaluation" in json_output


def test_risk_sensitivity():
    """Test different risk sensitivity levels"""
    agent = IngredientAnalysisAgent()

    ingredients = "sugar, E621, E471, water"

    # Low sensitivity
    result_low = agent.analyze_simple(
        ingredients_text=ingredients,
        preferences=["minimize additives"],
        risk_sensitivity=RiskSensitivity.LOW,
    )

    # High sensitivity
    result_high = agent.analyze_simple(
        ingredients_text=ingredients,
        preferences=["minimize additives"],
        risk_sensitivity=RiskSensitivity.HIGH,
    )

    # High sensitivity should flag more issues
    assert len(result_high.evaluation.key_reasons) >= len(result_low.evaluation.key_reasons)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
