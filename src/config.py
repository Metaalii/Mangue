"""Configuration for Mangue Ingredient Analysis Agent

This file centralizes hardcoded values that were previously scattered across the codebase,
making them easier to maintain and adjust.
"""

# Verdict scoring thresholds
# These values determine how conflict_severity_score maps to verdicts
VERDICT_THRESHOLDS = {
    "NOT_RECOMMENDED": 10,  # Score >= 10 results in NOT_RECOMMENDED
    "MIXED_FIT": 3,  # Score >= 3 results in MIXED_FIT
    # Score < 3 results in GOOD_FIT
}

# Scoring weights for different conflict types
CONFLICT_SCORES = {
    "HARD_CONSTRAINT": 10,  # Major conflict (e.g., allergen with allergy)
    "SOFT_PREFERENCE": 3,  # Minor conflict (e.g., additive when preferring natural)
    "POSITIVE_ALIGNMENT": -2,  # Positive alignment with goals (reduces conflict score)
}

# Non-vegan ingredients for dietary restriction checking
NON_VEGAN_KEYWORDS = [
    "milk", "egg", "honey", "gelatin", "whey", "casein", "lactose",
    "butter", "cream", "cheese", "yogurt", "ghee", "albumin", "ovalbumin",
    "shellac", "carmine", "cochineal", "isinglass", "lard", "tallow",
    "beeswax", "royal jelly", "propolis", "lanolin", "keratin",
    "collagen", "bone", "rennet", "pepsin", "anchovies"
]

# Non-vegetarian ingredients
NON_VEGETARIAN_KEYWORDS = [
    "gelatin", "cochineal", "carmine", "isinglass", "lard", "tallow",
    "rennet", "pepsin", "bone", "meat", "beef", "pork", "chicken",
    "fish", "anchovy", "anchovies"
]

# Natural ingredient patterns (used to infer ingredient type)
NATURAL_INGREDIENT_PATTERNS = [
    "flour", "wheat", "rice", "corn", "oat", "barley",
    "milk", "cream", "butter", "cheese",
    "egg", "water", "oil", "fat",
    "tomato", "onion", "garlic", "pepper",
    "cocoa", "chocolate", "vanilla",
    "fruit", "vegetable", "meat", "fish",
    "honey", "maple",
]

# Additive keyword to category mapping
from .models.schemas import AdditiveCategory

ADDITIVE_KEYWORD_MAP = {
    "color": AdditiveCategory.COLORING,
    "colour": AdditiveCategory.COLORING,
    "dye": AdditiveCategory.COLORING,
    "preservative": AdditiveCategory.PRESERVATIVE,
    "emulsifier": AdditiveCategory.EMULSIFIER,
    "thickener": AdditiveCategory.EMULSIFIER,
    "stabilizer": AdditiveCategory.EMULSIFIER,
    "stabiliser": AdditiveCategory.EMULSIFIER,
    "sweetener": AdditiveCategory.SWEETENER,
    "flavor": AdditiveCategory.FLAVORING,
    "flavour": AdditiveCategory.FLAVORING,
}

# Ingredient name normalization mappings
INGREDIENT_NAME_MAPPINGS = {
    "vit. c": "vitamin c",
    "vit c": "vitamin c",
    "msg": "monosodium glutamate",
    "hfcs": "high fructose corn syrup",
    "tbhq": "tertiary butylhydroquinone",
    "bha": "butylated hydroxyanisole",
    "bht": "butylated hydroxytoluene",
}

# API Configuration
API_CONFIG = {
    "MAX_INGREDIENT_TEXT_LENGTH": 50000,  # 50KB max input
    "DEFAULT_LOCALE": "EU",
}

# Output configuration
OUTPUT_CONFIG = {
    "MAX_KEY_REASONS": 6,  # Maximum number of key reasons to show
    "MAX_NOTABLE_ADDITIVES": 3,  # Maximum additives to highlight in summary
}
