"""Text processing utilities for ingredient parsing"""

import re
from typing import List, Tuple


def normalize_text(text: str) -> str:
    """
    Normalize ingredient text by removing extra whitespace and fixing common OCR errors.

    Args:
        text: Raw ingredient text

    Returns:
        Normalized text
    """
    # Remove extra whitespace
    text = " ".join(text.split())

    # Fix common OCR errors
    replacements = {
        "０": "0",
        "１": "1",
        "２": "2",
        "３": "3",
        "４": "4",
        "５": "5",
        "６": "6",
        "７": "7",
        "８": "8",
        "９": "9",
        "Ｅ": "E",
        "ｅ": "e",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    return text.strip()


def parse_ingredient_list(ingredients_text: str) -> Tuple[List[str], List[str]]:
    """
    Parse raw ingredient text into a list of individual ingredients.

    Args:
        ingredients_text: Raw ingredient text (may be comma-separated, OCR'd, etc.)

    Returns:
        Tuple of (ingredient_list, unreadable_segments)
    """
    if not ingredients_text or not ingredients_text.strip():
        return [], ["Empty ingredient text"]

    # Normalize the text first
    text = normalize_text(ingredients_text)

    # Split by common delimiters
    # Try comma first, then semicolon, then newline
    ingredients = []
    unreadable = []

    if "," in text:
        raw_ingredients = text.split(",")
    elif ";" in text:
        raw_ingredients = text.split(";")
    elif "\n" in text:
        raw_ingredients = text.split("\n")
    else:
        # If no delimiter, treat as single ingredient or space-separated
        raw_ingredients = [text]

    for ing in raw_ingredients:
        cleaned = ing.strip()
        if not cleaned:
            continue

        # Check if this looks like a valid ingredient
        if is_valid_ingredient(cleaned):
            ingredients.append(cleaned)
        else:
            # Mark as unreadable if it's too short, has too many special chars, etc.
            if len(cleaned) < 2 or has_excessive_special_chars(cleaned):
                unreadable.append(cleaned)
            else:
                # Give it the benefit of the doubt
                ingredients.append(cleaned)

    return ingredients, unreadable


def is_valid_ingredient(text: str) -> bool:
    """
    Check if text looks like a valid ingredient.

    Args:
        text: Text to check

    Returns:
        True if it looks like a valid ingredient
    """
    # Must have at least one letter
    if not re.search(r"[a-zA-Z]", text):
        return False

    # Should not be too short (except E-numbers)
    if len(text) < 2:
        return False

    # E-numbers are valid
    if re.match(r"E\d+[a-z]?", text, re.IGNORECASE):
        return True

    return True


def has_excessive_special_chars(text: str) -> bool:
    """
    Check if text has too many special characters to be a valid ingredient.

    Args:
        text: Text to check

    Returns:
        True if it has too many special characters
    """
    special_count = sum(1 for c in text if not c.isalnum() and not c.isspace())
    total_count = len(text)

    if total_count == 0:
        return True

    # If more than 50% special characters, probably not valid
    return (special_count / total_count) > 0.5


def calculate_confidence(original: str, canonical: str) -> float:
    """
    Calculate confidence score for ingredient normalization.

    Args:
        original: Original ingredient text
        canonical: Normalized/canonical form

    Returns:
        Confidence score between 0.0 and 1.0 (clamped)
    """
    # Handle empty strings
    if not original or not canonical:
        return 0.0

    # Exact match = 1.0
    if original.lower() == canonical.lower():
        return 1.0

    # Check how similar they are
    original_lower = original.lower()
    canonical_lower = canonical.lower()

    # If canonical is contained in original or vice versa, high confidence
    if canonical_lower in original_lower or original_lower in canonical_lower:
        return 0.95

    # Calculate simple similarity based on common characters
    common_chars = sum(1 for a, b in zip(original_lower, canonical_lower) if a == b)
    max_len = max(len(original_lower), len(canonical_lower))

    if max_len == 0:
        return 0.0

    similarity = common_chars / max_len

    # Boost confidence if both start with the same letter (clamp to 1.0)
    if original_lower and canonical_lower and original_lower[0] == canonical_lower[0]:
        similarity += 0.1

    # Always clamp to [0.0, 1.0]
    return round(min(1.0, max(0.0, similarity)), 2)


def tokenize_ingredient(ingredient: str) -> List[str]:
    """
    Tokenize an ingredient into meaningful parts.

    Args:
        ingredient: Ingredient text

    Returns:
        List of tokens
    """
    # Split on whitespace and common separators
    tokens = re.split(r"[\s\-()]+", ingredient.lower())
    return [t for t in tokens if t]
