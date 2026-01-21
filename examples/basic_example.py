"""Basic example of using the Ingredient Analysis Agent"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.agents import IngredientAnalysisAgent
from src.models import RiskSensitivity


def example_1_simple_analysis():
    """Example 1: Simple analysis with minimal user profile"""
    print("=" * 80)
    print("EXAMPLE 1: Simple Product Analysis")
    print("=" * 80)

    agent = IngredientAnalysisAgent(locale="EU")

    ingredients = "Sugar, wheat flour, water, cocoa powder, E471, E202, vanilla extract"

    result = agent.analyze_simple(
        ingredients_text=ingredients,
        goals=["eat healthier", "reduce processed foods"],
        constraints=["no peanuts"],
        preferences=["minimize additives", "natural ingredients"],
        risk_sensitivity=RiskSensitivity.MEDIUM,
    )

    print("\nIngredient Summary:")
    for item in result.user_output.INGREDIENT_SUMMARY:
        print(f"  - {item}")

    print(f"\nVerdict: {result.user_output.USER_FIT_VERDICT}")

    print("\nWhy this matters for you:")
    for item in result.user_output.WHY_THIS_MATTERS_FOR_YOU:
        print(f"  - {item}")

    print(f"\nFinal Note: {result.user_output.FINAL_NOTE}")

    # Show JSON output
    print("\n" + "=" * 80)
    print("Full JSON Output:")
    print("=" * 80)
    print(result.to_json())


def example_2_allergen_detection():
    """Example 2: Analysis with allergen constraints"""
    print("\n\n" + "=" * 80)
    print("EXAMPLE 2: Allergen Detection")
    print("=" * 80)

    agent = IngredientAnalysisAgent(locale="US")

    ingredients = "Milk chocolate (sugar, cocoa butter, milk powder), peanuts, soy lecithin, E476"

    result = agent.analyze_simple(
        ingredients_text=ingredients,
        goals=["avoid allergens"],
        constraints=["peanut allergy", "lactose intolerant"],
        preferences=["natural ingredients"],
        risk_sensitivity=RiskSensitivity.HIGH,
    )

    print("\nIngredient Summary:")
    for item in result.user_output.INGREDIENT_SUMMARY:
        print(f"  - {item}")

    print(f"\nVerdict: {result.user_output.USER_FIT_VERDICT}")

    print("\nWhy this matters for you:")
    for item in result.user_output.WHY_THIS_MATTERS_FOR_YOU:
        print(f"  - {item}")

    print(f"\nFinal Note: {result.user_output.FINAL_NOTE}")


def example_3_vegan_diet():
    """Example 3: Vegan dietary restrictions"""
    print("\n\n" + "=" * 80)
    print("EXAMPLE 3: Vegan Diet Analysis")
    print("=" * 80)

    agent = IngredientAnalysisAgent(locale="EU")

    ingredients = "Wheat flour, water, sunflower oil, salt, yeast, E300, E471"

    result = agent.analyze_simple(
        ingredients_text=ingredients,
        goals=["plant-based diet", "healthy eating"],
        constraints=["vegan"],
        preferences=["organic when possible", "minimal processing"],
        risk_sensitivity=RiskSensitivity.MEDIUM,
    )

    print("\nIngredient Summary:")
    for item in result.user_output.INGREDIENT_SUMMARY:
        print(f"  - {item}")

    print(f"\nVerdict: {result.user_output.USER_FIT_VERDICT}")

    print("\nWhy this matters for you:")
    for item in result.user_output.WHY_THIS_MATTERS_FOR_YOU:
        print(f"  - {item}")

    print(f"\nFinal Note: {result.user_output.FINAL_NOTE}")


def example_4_low_sugar():
    """Example 4: Low sugar preference"""
    print("\n\n" + "=" * 80)
    print("EXAMPLE 4: Low Sugar Diet")
    print("=" * 80)

    agent = IngredientAnalysisAgent(locale="US")

    ingredients = "Water, E951 (aspartame), citric acid, natural flavors, E950, E955"

    result = agent.analyze_simple(
        ingredients_text=ingredients,
        goals=["weight loss", "reduce sugar intake"],
        constraints=[],
        preferences=["low sugar", "avoid artificial sweeteners when possible"],
        risk_sensitivity=RiskSensitivity.MEDIUM,
    )

    print("\nIngredient Summary:")
    for item in result.user_output.INGREDIENT_SUMMARY:
        print(f"  - {item}")

    print(f"\nVerdict: {result.user_output.USER_FIT_VERDICT}")

    print("\nWhy this matters for you:")
    for item in result.user_output.WHY_THIS_MATTERS_FOR_YOU:
        print(f"  - {item}")

    print(f"\nFinal Note: {result.user_output.FINAL_NOTE}")


if __name__ == "__main__":
    example_1_simple_analysis()
    example_2_allergen_detection()
    example_3_vegan_diet()
    example_4_low_sugar()
