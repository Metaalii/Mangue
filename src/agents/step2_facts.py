"""STEP 2 — INGREDIENT FACTS (OBJECTIVE)"""

from typing import List
from ..models.schemas import IngredientFact, AdditiveCategory, ParsedIngredients, RegulatoryStatus
from ..data.additives import get_additive_info, is_e_number


def extract_ingredient_facts(parsed: ParsedIngredients, locale: str = "other") -> List[IngredientFact]:
    """
    Step 2: Extract objective facts about each ingredient.

    Args:
        parsed: ParsedIngredients from step 1
        locale: Regulatory locale (EU, US, other)

    Returns:
        List of IngredientFact objects
    """
    facts: List[IngredientFact] = []

    for mapping in parsed.canonical_map:
        canonical = mapping.canonical
        fact = analyze_ingredient(canonical, locale)
        facts.append(fact)

    return facts


def analyze_ingredient(canonical: str, locale: str = "other") -> IngredientFact:
    """
    Analyze a single ingredient and extract objective facts.

    Args:
        canonical: Canonical ingredient name
        locale: Regulatory locale

    Returns:
        IngredientFact object
    """
    # Check if it's in our additive database
    additive_info = get_additive_info(canonical)

    if additive_info:
        # It's a known additive
        return IngredientFact(
            canonical=canonical,
            is_additive=True,
            category=additive_info["category"],
            common_name=additive_info["common_name"],
            regulatory_status=RegulatoryStatus(
                EU=additive_info["regulatory_status"]["EU"],
                US=additive_info["regulatory_status"]["US"],
            ),
            notes=additive_info["notes"],
            uncertainty_notes=[],
        )

    # Not in database - make best guess based on name
    is_additive, category, notes, uncertainty_notes = infer_ingredient_type(canonical)

    return IngredientFact(
        canonical=canonical,
        is_additive=is_additive,
        category=category,
        common_name=None,
        regulatory_status=RegulatoryStatus(EU="unknown", US="unknown"),
        notes=notes,
        uncertainty_notes=uncertainty_notes,
    )


def infer_ingredient_type(canonical: str) -> tuple:
    """
    Infer ingredient type based on name patterns when not in database.

    Args:
        canonical: Canonical ingredient name

    Returns:
        Tuple of (is_additive, category, notes, uncertainty_notes)
    """
    canonical_lower = canonical.lower()
    notes = []
    uncertainty_notes = []

    # Check for E-number pattern
    if is_e_number(canonical):
        uncertainty_notes.append(f"E-number {canonical} not found in database; classification uncertain")
        return True, AdditiveCategory.OTHER, notes, uncertainty_notes

    # Check for common ingredient patterns
    natural_ingredients = [
        "flour", "wheat", "rice", "corn", "oat", "barley",
        "milk", "cream", "butter", "cheese",
        "egg", "water", "oil", "fat",
        "tomato", "onion", "garlic", "pepper",
        "cocoa", "chocolate", "vanilla",
        "fruit", "vegetable", "meat", "fish",
        "honey", "maple",
    ]

    for natural in natural_ingredients:
        if natural in canonical_lower:
            notes.append("Natural ingredient")
            return False, AdditiveCategory.NONE, notes, uncertainty_notes

    # Check for additive-like keywords
    additive_keywords = {
        "color": AdditiveCategory.COLORING,
        "colour": AdditiveCategory.COLORING,
        "dye": AdditiveCategory.COLORING,
        "preservative": AdditiveCategory.PRESERVATIVE,
        "emulsifier": AdditiveCategory.EMULSIFIER,
        "thickener": AdditiveCategory.EMULSIFIER,
        "stabilizer": AdditiveCategory.EMULSIFIER,
        "sweetener": AdditiveCategory.SWEETENER,
        "flavor": AdditiveCategory.FLAVORING,
        "flavour": AdditiveCategory.FLAVORING,
    }

    for keyword, category in additive_keywords.items():
        if keyword in canonical_lower:
            uncertainty_notes.append(f"Classified as {category.value} based on name pattern")
            return True, category, notes, uncertainty_notes

    # Default: probably a natural ingredient but uncertain
    uncertainty_notes.append("Ingredient not found in database; assuming natural ingredient")
    return False, AdditiveCategory.NONE, notes, uncertainty_notes
