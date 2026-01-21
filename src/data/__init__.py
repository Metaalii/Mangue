"""Reference data for ingredient analysis"""

from .additives import ADDITIVE_DATABASE, get_additive_info
from .allergens import COMMON_ALLERGENS, check_allergen

__all__ = [
    "ADDITIVE_DATABASE",
    "get_additive_info",
    "COMMON_ALLERGENS",
    "check_allergen",
]
