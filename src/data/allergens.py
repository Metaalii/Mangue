"""Common allergen database"""

from typing import List, Set

# Major allergens recognized by FDA and EU regulations
COMMON_ALLERGENS = {
    "milk": ["milk", "dairy", "lactose", "whey", "casein", "butter", "cream", "cheese", "yogurt"],
    "eggs": ["egg", "eggs", "albumin", "ovalbumin"],
    "fish": ["fish", "anchovy", "bass", "cod", "salmon", "tuna", "halibut"],
    "shellfish": ["shellfish", "crab", "lobster", "shrimp", "prawn", "crayfish"],
    "tree_nuts": ["almond", "cashew", "walnut", "pecan", "pistachio", "hazelnut", "macadamia"],
    "peanuts": ["peanut", "groundnut"],
    "wheat": ["wheat", "gluten", "flour"],
    "soybeans": ["soy", "soya", "soybean", "tofu"],
    "sesame": ["sesame", "tahini"],
    "celery": ["celery", "celeriac"],
    "mustard": ["mustard"],
    "lupin": ["lupin", "lupine"],
    "molluscs": ["mollusc", "mollusk", "snail", "squid", "octopus", "clam", "mussel", "oyster"],
    "sulphites": ["sulphite", "sulfite", "sulphur dioxide", "sulfur dioxide", "e220", "e221", "e222", "e223", "e224", "e228"],
}


def check_allergen(ingredient: str) -> List[str]:
    """
    Check if an ingredient contains common allergens.

    Args:
        ingredient: Ingredient name to check

    Returns:
        List of allergen categories found
    """
    ingredient_lower = ingredient.lower()
    found_allergens = []

    for allergen_category, keywords in COMMON_ALLERGENS.items():
        for keyword in keywords:
            if keyword in ingredient_lower:
                found_allergens.append(allergen_category)
                break

    return found_allergens


def get_all_allergen_keywords() -> Set[str]:
    """Get all allergen keywords as a flat set"""
    keywords = set()
    for allergen_list in COMMON_ALLERGENS.values():
        keywords.update(allergen_list)
    return keywords
