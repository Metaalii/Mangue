"""STEP 1 — EXTRACT & NORMALIZE (NO JUDGMENT)"""

from typing import List
from ..models.schemas import ParsedIngredients, CanonicalMapping
from ..utils.text_utils import parse_ingredient_list, normalize_text, calculate_confidence
from ..data.additives import is_e_number


def extract_and_normalize(ingredients_text: str) -> ParsedIngredients:
    """
    Step 1: Parse ingredients_text into a list and normalize.

    Args:
        ingredients_text: Raw ingredient text

    Returns:
        ParsedIngredients with original list, canonical mappings, and unreadable segments
    """
    # Parse the text into individual ingredients
    original_list, unreadable_segments = parse_ingredient_list(ingredients_text)

    # Create canonical mappings
    canonical_map: List[CanonicalMapping] = []

    for original in original_list:
        canonical = canonicalize_ingredient(original)
        confidence = calculate_confidence(original, canonical)

        canonical_map.append(
            CanonicalMapping(
                original=original,
                canonical=canonical,
                confidence=confidence,
            )
        )

    return ParsedIngredients(
        original_list=original_list,
        canonical_map=canonical_map,
        unreadable_segments=unreadable_segments,
    )


def canonicalize_ingredient(ingredient: str) -> str:
    """
    Normalize an ingredient to its canonical form.

    Args:
        ingredient: Original ingredient text

    Returns:
        Canonical form
    """
    # Basic normalization
    canonical = normalize_text(ingredient)

    # Lowercase for consistency
    canonical_lower = canonical.lower()

    # Handle E-numbers specially
    if is_e_number(canonical_lower):
        # Standardize E-number format to uppercase E followed by digits
        return canonical_lower.upper()

    # Common ingredient name mappings
    name_mappings = {
        "vit. c": "vitamin c",
        "vit c": "vitamin c",
        "ascorbic acid": "vitamin c",
        "e300": "vitamin c",
        "tocopherol": "vitamin e",
        "e306": "vitamin e",
        "glucose-fructose syrup": "glucose syrup",
        "fructose-glucose syrup": "glucose syrup",
        "hfcs": "high fructose corn syrup",
        "msg": "monosodium glutamate",
        "e621": "monosodium glutamate",
        "bha": "butylated hydroxyanisole",
        "bht": "butylated hydroxytoluene",
    }

    if canonical_lower in name_mappings:
        return name_mappings[canonical_lower]

    # Handle parentheses - extract main ingredient
    if "(" in canonical:
        # e.g., "sugar (cane sugar)" -> "sugar"
        canonical = canonical.split("(")[0].strip()

    # Remove trailing periods
    canonical = canonical.rstrip(".")

    return canonical
