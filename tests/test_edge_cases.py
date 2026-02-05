"""Comprehensive edge case tests for Mangue Ingredient Analysis Agent"""

import pytest
from src.agents import IngredientAnalysisAgent
from src.agents.step2_facts import infer_ingredient_type, InferredIngredientInfo
from src.data.allergens import check_allergen
from src.utils.text_utils import calculate_confidence, parse_ingredient_list
from src.models import RiskSensitivity, Verdict, AdditiveCategory


class TestAllergenDetection:
    """Test allergen detection edge cases"""

    def test_nutmeg_not_detected_as_nut(self):
        """Nutmeg should NOT trigger tree_nuts allergen"""
        allergens = check_allergen("nutmeg")
        assert "tree_nuts" not in allergens

    def test_butternut_squash_not_detected_as_nut(self):
        """Butternut squash should NOT trigger tree_nuts allergen"""
        allergens = check_allergen("butternut squash")
        assert "tree_nuts" not in allergens

    def test_coconut_not_detected_as_nut(self):
        """Coconut should NOT trigger tree_nuts allergen (FDA doesn't classify it as tree nut)"""
        allergens = check_allergen("coconut")
        assert "tree_nuts" not in allergens

    def test_actual_almond_detected(self):
        """Actual almonds should trigger tree_nuts"""
        allergens = check_allergen("almonds")
        assert "tree_nuts" in allergens

    def test_buckwheat_not_detected_as_wheat(self):
        """Buckwheat should NOT trigger wheat allergen (it's not wheat)"""
        allergens = check_allergen("buckwheat")
        assert "wheat" not in allergens

    def test_actual_wheat_detected(self):
        """Actual wheat should trigger wheat allergen"""
        allergens = check_allergen("whole wheat flour")
        assert "wheat" in allergens

    def test_fishless_not_detected_as_fish(self):
        """Fishless should NOT trigger fish allergen"""
        allergens = check_allergen("fishless sauce")
        assert "fish" not in allergens

    def test_multiple_allergens_detected(self):
        """Ingredient with multiple allergens should return all"""
        # Egg mayo contains eggs and possibly soy
        allergens = check_allergen("egg mayonnaise with soy lecithin")
        assert "eggs" in allergens
        assert "soybeans" in allergens

    def test_molluscs_detected_for_oyster(self):
        """Oyster sauce should trigger molluscs"""
        allergens = check_allergen("oyster sauce")
        assert "molluscs" in allergens

    def test_shellfish_constraint_with_mollusc_ingredient(self):
        """Shellfish allergy constraint should catch mollusc ingredients"""
        agent = IngredientAnalysisAgent()
        result = agent.analyze_simple(
            ingredients_text="squid ink, water, salt",
            constraints=["shellfish allergy"],
            risk_sensitivity=RiskSensitivity.HIGH,
        )
        # Should have a reason about shellfish/molluscs
        assert result.evaluation.verdict in [Verdict.MIXED_FIT, Verdict.NOT_RECOMMENDED]
        assert len(result.evaluation.key_reasons) > 0


class TestVeganDetection:
    """Test vegan dietary restriction detection"""

    def test_ghee_detected_as_non_vegan(self):
        """Ghee (clarified butter) should be flagged for vegans"""
        agent = IngredientAnalysisAgent()
        result = agent.analyze_simple(
            ingredients_text="rice, ghee, salt",
            constraints=["vegan"],
        )
        assert result.evaluation.verdict in [Verdict.MIXED_FIT, Verdict.NOT_RECOMMENDED]

    def test_casein_detected_as_non_vegan(self):
        """Casein should be flagged for vegans"""
        agent = IngredientAnalysisAgent()
        result = agent.analyze_simple(
            ingredients_text="protein powder, casein, water",
            constraints=["vegan"],
        )
        assert result.evaluation.verdict in [Verdict.MIXED_FIT, Verdict.NOT_RECOMMENDED]

    def test_shellac_detected_as_non_vegan(self):
        """Shellac (insect-derived) should be flagged for vegans"""
        agent = IngredientAnalysisAgent()
        result = agent.analyze_simple(
            ingredients_text="sugar, shellac coating",
            constraints=["vegan"],
        )
        assert result.evaluation.verdict in [Verdict.MIXED_FIT, Verdict.NOT_RECOMMENDED]

    def test_carmine_detected_as_non_vegan(self):
        """Carmine (insect-derived red dye) should be flagged for vegans"""
        agent = IngredientAnalysisAgent()
        result = agent.analyze_simple(
            ingredients_text="sugar, carmine, water",
            constraints=["vegan"],
        )
        assert result.evaluation.verdict in [Verdict.MIXED_FIT, Verdict.NOT_RECOMMENDED]


class TestVegetarianDetection:
    """Test vegetarian dietary restriction detection"""

    def test_gelatin_detected_as_non_vegetarian(self):
        """Gelatin should be flagged for vegetarians"""
        agent = IngredientAnalysisAgent()
        result = agent.analyze_simple(
            ingredients_text="sugar, gelatin, water",
            constraints=["vegetarian"],
        )
        assert result.evaluation.verdict in [Verdict.MIXED_FIT, Verdict.NOT_RECOMMENDED]

    def test_isinglass_detected_as_non_vegetarian(self):
        """Isinglass (fish bladder) should be flagged for vegetarians"""
        agent = IngredientAnalysisAgent()
        result = agent.analyze_simple(
            ingredients_text="wine fined with isinglass",
            constraints=["vegetarian"],
        )
        assert result.evaluation.verdict in [Verdict.MIXED_FIT, Verdict.NOT_RECOMMENDED]


class TestIngredientTypeInference:
    """Test ingredient type inference"""

    def test_returns_named_tuple(self):
        """infer_ingredient_type should return InferredIngredientInfo"""
        result = infer_ingredient_type("sugar")
        assert isinstance(result, InferredIngredientInfo)
        assert hasattr(result, 'is_additive')
        assert hasattr(result, 'category')
        assert hasattr(result, 'notes')
        assert hasattr(result, 'uncertainty_notes')

    def test_e_number_not_in_database(self):
        """Unknown E-number should be flagged as uncertain additive"""
        result = infer_ingredient_type("E999")
        assert result.is_additive is True
        assert result.category == AdditiveCategory.OTHER
        assert len(result.uncertainty_notes) > 0
        assert "E999" in result.uncertainty_notes[0]

    def test_natural_ingredient_detected(self):
        """Natural ingredients should be detected as non-additives"""
        result = infer_ingredient_type("whole wheat flour")
        assert result.is_additive is False
        assert result.category == AdditiveCategory.NONE

    def test_colorant_keyword_detected(self):
        """Colorant keyword should classify as coloring additive"""
        result = infer_ingredient_type("natural colorant")
        assert result.is_additive is True
        assert result.category == AdditiveCategory.COLORING

    def test_discolor_not_matched_as_color(self):
        """'discolor' should not match 'color' keyword due to word boundaries"""
        result = infer_ingredient_type("anti-discoloration agent")
        # Should NOT be classified as coloring
        assert result.category != AdditiveCategory.COLORING


class TestConfidenceCalculation:
    """Test confidence score calculation edge cases"""

    def test_confidence_never_exceeds_one(self):
        """Confidence score should never exceed 1.0"""
        # Test case that previously could exceed 1.0
        score = calculate_confidence("test", "test")
        assert score <= 1.0

        # Test with similar strings that get boost
        score = calculate_confidence("abc", "ab")
        assert score <= 1.0

        score = calculate_confidence("testing", "test")
        assert score <= 1.0

    def test_empty_string_handling(self):
        """Empty strings should return 0.0 confidence"""
        assert calculate_confidence("", "test") == 0.0
        assert calculate_confidence("test", "") == 0.0
        assert calculate_confidence("", "") == 0.0

    def test_exact_match_is_one(self):
        """Exact match should return 1.0"""
        assert calculate_confidence("sugar", "sugar") == 1.0
        assert calculate_confidence("Sugar", "sugar") == 1.0  # Case insensitive


class TestIngredientParsing:
    """Test ingredient list parsing edge cases"""

    def test_empty_input(self):
        """Empty input should return empty list with unreadable note"""
        ingredients, unreadable = parse_ingredient_list("")
        assert len(ingredients) == 0
        assert len(unreadable) > 0

    def test_single_ingredient(self):
        """Single ingredient without delimiter should work"""
        ingredients, unreadable = parse_ingredient_list("sugar")
        assert "sugar" in ingredients

    def test_comma_separated(self):
        """Comma-separated ingredients should parse correctly"""
        ingredients, unreadable = parse_ingredient_list("sugar, salt, water")
        assert len(ingredients) == 3

    def test_semicolon_separated(self):
        """Semicolon-separated ingredients should parse correctly"""
        ingredients, unreadable = parse_ingredient_list("sugar; salt; water")
        assert len(ingredients) == 3

    def test_special_characters_rejected(self):
        """Items with excessive special chars should be marked unreadable"""
        ingredients, unreadable = parse_ingredient_list("sugar, @#$%^&, salt")
        assert "sugar" in ingredients
        assert "salt" in ingredients
        # The special char item should be in unreadable
        assert len(unreadable) >= 1 or len(ingredients) == 2


class TestVerdictThresholds:
    """Test verdict scoring and threshold logic"""

    def test_single_hard_constraint_violation_is_not_recommended(self):
        """A single hard constraint violation (allergen) should result in NOT_RECOMMENDED"""
        agent = IngredientAnalysisAgent()
        result = agent.analyze_simple(
            ingredients_text="peanut butter, water",
            constraints=["peanut allergy"],
            risk_sensitivity=RiskSensitivity.HIGH,
        )
        assert result.evaluation.verdict == Verdict.NOT_RECOMMENDED

    def test_soft_preference_only_is_mixed_fit(self):
        """Soft preference conflicts alone should result in MIXED_FIT at most"""
        agent = IngredientAnalysisAgent()
        result = agent.analyze_simple(
            ingredients_text="E621, water",
            preferences=["avoid additives"],
            risk_sensitivity=RiskSensitivity.HIGH,
        )
        # With only soft preference conflicts, should be MIXED_FIT
        assert result.evaluation.verdict in [Verdict.GOOD_FIT, Verdict.MIXED_FIT]

    def test_natural_ingredients_good_fit(self):
        """Natural ingredients with no conflicts should be GOOD_FIT"""
        agent = IngredientAnalysisAgent()
        result = agent.analyze_simple(
            ingredients_text="water, salt, flour",
            goals=["eat healthy"],
            constraints=[],
            preferences=["natural ingredients"],
        )
        assert result.evaluation.verdict == Verdict.GOOD_FIT


class TestRiskSensitivityLevels:
    """Test that risk sensitivity affects results appropriately"""

    def test_high_sensitivity_flags_more(self):
        """High sensitivity should flag more issues than low"""
        agent = IngredientAnalysisAgent()
        ingredients = "E621, E471, sugar, water"

        result_low = agent.analyze_simple(
            ingredients_text=ingredients,
            preferences=["minimize additives"],
            risk_sensitivity=RiskSensitivity.LOW,
        )

        result_high = agent.analyze_simple(
            ingredients_text=ingredients,
            preferences=["minimize additives"],
            risk_sensitivity=RiskSensitivity.HIGH,
        )

        # High should have at least as many (usually more) reasons
        assert len(result_high.evaluation.key_reasons) >= len(result_low.evaluation.key_reasons)


class TestDuplicateHandling:
    """Test handling of duplicate ingredients"""

    def test_duplicate_ingredients_parsed(self):
        """Duplicate ingredients should be parsed (even if unusual)"""
        agent = IngredientAnalysisAgent()
        result = agent.analyze_simple(
            ingredients_text="sugar, sugar, sugar",
        )
        # Should parse all three (handling duplicates is up to the product)
        assert len(result.parsed_ingredients.original_list) == 3


class TestLongInputHandling:
    """Test handling of long ingredient lists"""

    def test_many_ingredients(self):
        """Should handle many ingredients without error"""
        agent = IngredientAnalysisAgent()
        # Generate a long list
        ingredients = ", ".join([f"ingredient{i}" for i in range(100)])
        result = agent.analyze_simple(ingredients_text=ingredients)
        assert result is not None
        assert len(result.parsed_ingredients.original_list) == 100


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
