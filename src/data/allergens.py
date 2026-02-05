"""Common allergen database"""

import re
from typing import List, Set

# Major allergens recognized by FDA and EU regulations
COMMON_ALLERGENS = {
    "milk": ["milk", "dairy", "lactose", "whey", "casein", "butter", "cream", "cheese", "yogurt", "ghee"],
    "eggs": ["egg", "eggs", "albumin", "ovalbumin", "ovomucin", "lysozyme"],
    "fish": ["fish", "anchovy", "anchovies", "bass", "cod", "salmon", "tuna", "halibut", "mackerel", "sardine"],
    "shellfish": ["shellfish", "crab", "lobster", "shrimp", "prawn", "crayfish", "crawfish"],
    "tree_nuts": ["almond", "cashew", "walnut", "pecan", "pistachio", "hazelnut", "macadamia", "brazil nut", "chestnut", "pine nut"],
    "peanuts": ["peanut", "groundnut", "arachis"],
    "wheat": ["wheat", "gluten", "spelt", "kamut", "semolina", "durum", "farina", "triticale"],
    "soybeans": ["soy", "soya", "soybean", "tofu", "tempeh", "edamame", "miso"],
    "sesame": ["sesame", "tahini", "halvah", "hummus"],
    "celery": ["celery", "celeriac"],
    "mustard": ["mustard"],
    "lupin": ["lupin", "lupine", "lupini"],
    "molluscs": ["mollusc", "mollusk", "snail", "squid", "octopus", "clam", "mussel", "oyster", "scallop", "abalone"],
    "sulphites": ["sulphite", "sulfite", "sulphur dioxide", "sulfur dioxide", "e220", "e221", "e222", "e223", "e224", "e228"],
}

# Keywords that should NOT trigger allergen detection (false positive prevention)
# e.g., "nutmeg" should not match "nut", "fishless" should not match "fish"
ALLERGEN_EXCLUSIONS = {
    "tree_nuts": ["nutmeg", "butternut squash", "coconut", "water chestnut", "doughnut", "donut"],
    "fish": ["fishless", "jellyfish", "starfish", "crayfish", "crawfish", "silverfish"],
    "wheat": ["buckwheat"],
}


def _word_boundary_match(keyword: str, text: str) -> bool:
    """Check if keyword exists with word boundaries (not as substring of another word)

    Handles plurals and common word variations by allowing 's', 'es', 'ed' suffixes.
    """
    # For multi-word keywords, use simple contains
    if " " in keyword:
        return keyword in text
    # For single words, match keyword at word boundary, allowing common suffixes
    # This matches: almond, almonds, egg, eggs, etc.
    pattern = r'\b' + re.escape(keyword) + r'(?:s|es|ed)?\b'
    return bool(re.search(pattern, text))


def check_allergen(ingredient: str) -> List[str]:
    """
    Check if an ingredient contains common allergens.

    Uses word boundary matching to avoid false positives like:
    - "nutmeg" matching "nut"
    - "fishless" matching "fish"

    Args:
        ingredient: Ingredient name to check

    Returns:
        List of allergen categories found
    """
    ingredient_lower = ingredient.lower()
    found_allergens = []

    for allergen_category, keywords in COMMON_ALLERGENS.items():
        # First check if ingredient is in exclusion list for this allergen
        exclusions = ALLERGEN_EXCLUSIONS.get(allergen_category, [])
        if any(excl in ingredient_lower for excl in exclusions):
            continue

        for keyword in keywords:
            if _word_boundary_match(keyword, ingredient_lower):
                found_allergens.append(allergen_category)
                break

    return found_allergens


def get_all_allergen_keywords() -> Set[str]:
    """Get all allergen keywords as a flat set"""
    keywords = set()
    for allergen_list in COMMON_ALLERGENS.values():
        keywords.update(allergen_list)
    return keywords
