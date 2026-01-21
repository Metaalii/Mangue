"""Reference database of food additives including E-numbers"""

from typing import Dict, Optional, Tuple
from ..models.schemas import AdditiveCategory

# Comprehensive E-number and additive database
# Format: {identifier: (common_name, category, EU_status, US_status, notes)}
ADDITIVE_DATABASE: Dict[str, Tuple[str, AdditiveCategory, str, str, list]] = {
    # Colorings (E100-E199)
    "E100": ("Curcumin", AdditiveCategory.COLORING, "approved", "approved", ["Natural yellow coloring from turmeric"]),
    "E102": ("Tartrazine", AdditiveCategory.COLORING, "approved", "approved", ["Synthetic yellow coloring", "May cause allergic reactions in sensitive individuals"]),
    "E104": ("Quinoline Yellow", AdditiveCategory.COLORING, "approved", "banned", ["Synthetic yellow coloring"]),
    "E110": ("Sunset Yellow FCF", AdditiveCategory.COLORING, "approved", "approved", ["Synthetic orange coloring"]),
    "E120": ("Cochineal", AdditiveCategory.COLORING, "approved", "approved", ["Natural red coloring from insects"]),
    "E122": ("Carmoisine", AdditiveCategory.COLORING, "approved", "banned", ["Synthetic red coloring"]),
    "E124": ("Ponceau 4R", AdditiveCategory.COLORING, "approved", "banned", ["Synthetic red coloring"]),
    "E129": ("Allura Red AC", AdditiveCategory.COLORING, "approved", "approved", ["Synthetic red coloring"]),
    "E131": ("Patent Blue V", AdditiveCategory.COLORING, "approved", "banned", ["Synthetic blue coloring"]),
    "E132": ("Indigotine", AdditiveCategory.COLORING, "approved", "approved", ["Synthetic blue coloring"]),
    "E133": ("Brilliant Blue FCF", AdditiveCategory.COLORING, "approved", "approved", ["Synthetic blue coloring"]),
    "E140": ("Chlorophylls", AdditiveCategory.COLORING, "approved", "approved", ["Natural green coloring"]),
    "E141": ("Copper complexes of chlorophylls", AdditiveCategory.COLORING, "approved", "approved", ["Natural green coloring"]),
    "E150a": ("Plain caramel", AdditiveCategory.COLORING, "approved", "approved", ["Natural brown coloring"]),
    "E150b": ("Caustic sulphite caramel", AdditiveCategory.COLORING, "approved", "approved", ["Brown coloring"]),
    "E150c": ("Ammonia caramel", AdditiveCategory.COLORING, "approved", "approved", ["Brown coloring"]),
    "E150d": ("Sulphite ammonia caramel", AdditiveCategory.COLORING, "approved", "approved", ["Brown coloring"]),
    "E160a": ("Carotenes", AdditiveCategory.COLORING, "approved", "approved", ["Natural orange coloring from plants"]),
    "E160b": ("Annatto", AdditiveCategory.COLORING, "approved", "approved", ["Natural orange-red coloring"]),
    "E160c": ("Paprika extract", AdditiveCategory.COLORING, "approved", "approved", ["Natural red coloring"]),
    "E162": ("Beetroot Red", AdditiveCategory.COLORING, "approved", "approved", ["Natural red coloring from beets"]),
    "E163": ("Anthocyanins", AdditiveCategory.COLORING, "approved", "approved", ["Natural red/purple coloring from fruits"]),
    "E171": ("Titanium dioxide", AdditiveCategory.COLORING, "banned-2022", "approved", ["White coloring", "EU banned in 2022 due to safety concerns"]),

    # Preservatives (E200-E299)
    "E200": ("Sorbic acid", AdditiveCategory.PRESERVATIVE, "approved", "approved", ["Common preservative in foods"]),
    "E202": ("Potassium sorbate", AdditiveCategory.PRESERVATIVE, "approved", "approved", ["Common preservative"]),
    "E210": ("Benzoic acid", AdditiveCategory.PRESERVATIVE, "approved", "approved", ["Preservative, naturally occurs in some fruits"]),
    "E211": ("Sodium benzoate", AdditiveCategory.PRESERVATIVE, "approved", "approved", ["Common preservative"]),
    "E220": ("Sulphur dioxide", AdditiveCategory.PRESERVATIVE, "approved", "approved", ["Preservative and antioxidant", "May cause reactions in asthmatics"]),
    "E221": ("Sodium sulphite", AdditiveCategory.PRESERVATIVE, "approved", "approved", ["Preservative"]),
    "E222": ("Sodium bisulphite", AdditiveCategory.PRESERVATIVE, "approved", "approved", ["Preservative"]),
    "E223": ("Sodium metabisulphite", AdditiveCategory.PRESERVATIVE, "approved", "approved", ["Preservative"]),
    "E224": ("Potassium metabisulphite", AdditiveCategory.PRESERVATIVE, "approved", "approved", ["Preservative"]),
    "E228": ("Potassium bisulphite", AdditiveCategory.PRESERVATIVE, "approved", "approved", ["Preservative"]),
    "E234": ("Nisin", AdditiveCategory.PRESERVATIVE, "approved", "approved", ["Natural preservative from bacteria"]),
    "E242": ("Dimethyl dicarbonate", AdditiveCategory.PRESERVATIVE, "approved", "approved", ["Preservative for beverages"]),
    "E249": ("Potassium nitrite", AdditiveCategory.PRESERVATIVE, "approved", "approved", ["Preservative in cured meats"]),
    "E250": ("Sodium nitrite", AdditiveCategory.PRESERVATIVE, "approved", "approved", ["Preservative in cured meats", "Forms nitrosamines when heated at high temperatures"]),
    "E251": ("Sodium nitrate", AdditiveCategory.PRESERVATIVE, "approved", "approved", ["Preservative in cured meats"]),
    "E252": ("Potassium nitrate", AdditiveCategory.PRESERVATIVE, "approved", "approved", ["Preservative"]),
    "E280": ("Propionic acid", AdditiveCategory.PRESERVATIVE, "approved", "approved", ["Preservative in baked goods"]),
    "E281": ("Sodium propionate", AdditiveCategory.PRESERVATIVE, "approved", "approved", ["Preservative"]),
    "E282": ("Calcium propionate", AdditiveCategory.PRESERVATIVE, "approved", "approved", ["Preservative in bread"]),
    "E283": ("Potassium propionate", AdditiveCategory.PRESERVATIVE, "approved", "approved", ["Preservative"]),

    # Antioxidants (E300-E399)
    "E300": ("Ascorbic acid", AdditiveCategory.OTHER, "approved", "approved", ["Vitamin C, antioxidant"]),
    "E301": ("Sodium ascorbate", AdditiveCategory.OTHER, "approved", "approved", ["Vitamin C salt, antioxidant"]),
    "E302": ("Calcium ascorbate", AdditiveCategory.OTHER, "approved", "approved", ["Vitamin C salt, antioxidant"]),
    "E304": ("Fatty acid esters of ascorbic acid", AdditiveCategory.OTHER, "approved", "approved", ["Antioxidant"]),
    "E306": ("Tocopherols", AdditiveCategory.OTHER, "approved", "approved", ["Vitamin E, natural antioxidant"]),
    "E307": ("Alpha-tocopherol", AdditiveCategory.OTHER, "approved", "approved", ["Vitamin E, antioxidant"]),
    "E310": ("Propyl gallate", AdditiveCategory.OTHER, "approved", "approved", ["Synthetic antioxidant"]),
    "E320": ("Butylated hydroxyanisole (BHA)", AdditiveCategory.OTHER, "approved", "approved", ["Synthetic antioxidant", "Some studies suggest potential health concerns"]),
    "E321": ("Butylated hydroxytoluene (BHT)", AdditiveCategory.OTHER, "approved", "approved", ["Synthetic antioxidant", "Some studies suggest potential health concerns"]),
    "E330": ("Citric acid", AdditiveCategory.OTHER, "approved", "approved", ["Natural acid, antioxidant, flavoring"]),
    "E331": ("Sodium citrates", AdditiveCategory.OTHER, "approved", "approved", ["Acidity regulator"]),
    "E332": ("Potassium citrates", AdditiveCategory.OTHER, "approved", "approved", ["Acidity regulator"]),
    "E333": ("Calcium citrates", AdditiveCategory.OTHER, "approved", "approved", ["Acidity regulator"]),

    # Emulsifiers, stabilizers (E400-E599)
    "E400": ("Alginic acid", AdditiveCategory.EMULSIFIER, "approved", "approved", ["Natural thickener from seaweed"]),
    "E401": ("Sodium alginate", AdditiveCategory.EMULSIFIER, "approved", "approved", ["Natural thickener"]),
    "E402": ("Potassium alginate", AdditiveCategory.EMULSIFIER, "approved", "approved", ["Natural thickener"]),
    "E403": ("Ammonium alginate", AdditiveCategory.EMULSIFIER, "approved", "approved", ["Natural thickener"]),
    "E404": ("Calcium alginate", AdditiveCategory.EMULSIFIER, "approved", "approved", ["Natural thickener"]),
    "E406": ("Agar", AdditiveCategory.EMULSIFIER, "approved", "approved", ["Natural thickener from seaweed"]),
    "E407": ("Carrageenan", AdditiveCategory.EMULSIFIER, "approved", "approved", ["Natural thickener from seaweed"]),
    "E410": ("Locust bean gum", AdditiveCategory.EMULSIFIER, "approved", "approved", ["Natural thickener"]),
    "E412": ("Guar gum", AdditiveCategory.EMULSIFIER, "approved", "approved", ["Natural thickener from legumes"]),
    "E414": ("Acacia gum", AdditiveCategory.EMULSIFIER, "approved", "approved", ["Natural thickener"]),
    "E415": ("Xanthan gum", AdditiveCategory.EMULSIFIER, "approved", "approved", ["Thickener produced by bacteria"]),
    "E420": ("Sorbitol", AdditiveCategory.SWEETENER, "approved", "approved", ["Sugar alcohol, sweetener, humectant"]),
    "E421": ("Mannitol", AdditiveCategory.SWEETENER, "approved", "approved", ["Sugar alcohol, sweetener"]),
    "E422": ("Glycerol", AdditiveCategory.EMULSIFIER, "approved", "approved", ["Humectant, sweetener"]),
    "E440": ("Pectins", AdditiveCategory.EMULSIFIER, "approved", "approved", ["Natural thickener from fruits"]),
    "E450": ("Diphosphates", AdditiveCategory.EMULSIFIER, "approved", "approved", ["Emulsifier, raising agent"]),
    "E451": ("Triphosphates", AdditiveCategory.EMULSIFIER, "approved", "approved", ["Emulsifier"]),
    "E452": ("Polyphosphates", AdditiveCategory.EMULSIFIER, "approved", "approved", ["Emulsifier, sequestrant"]),
    "E460": ("Cellulose", AdditiveCategory.EMULSIFIER, "approved", "approved", ["Natural bulking agent from plants"]),
    "E461": ("Methylcellulose", AdditiveCategory.EMULSIFIER, "approved", "approved", ["Thickener, emulsifier"]),
    "E464": ("Hydroxypropyl methylcellulose", AdditiveCategory.EMULSIFIER, "approved", "approved", ["Thickener, emulsifier"]),
    "E466": ("Carboxymethyl cellulose", AdditiveCategory.EMULSIFIER, "approved", "approved", ["Thickener, stabilizer"]),
    "E470a": ("Sodium, potassium and calcium salts of fatty acids", AdditiveCategory.EMULSIFIER, "approved", "approved", ["Emulsifier"]),
    "E471": ("Mono- and diglycerides of fatty acids", AdditiveCategory.EMULSIFIER, "approved", "approved", ["Common emulsifier"]),
    "E472e": ("Mono- and diacetyl tartaric acid esters of mono- and diglycerides", AdditiveCategory.EMULSIFIER, "approved", "approved", ["Emulsifier"]),
    "E475": ("Polyglycerol esters of fatty acids", AdditiveCategory.EMULSIFIER, "approved", "approved", ["Emulsifier"]),
    "E476": ("Polyglycerol polyricinoleate", AdditiveCategory.EMULSIFIER, "approved", "approved", ["Emulsifier in chocolate"]),
    "E500": ("Sodium carbonates", AdditiveCategory.OTHER, "approved", "approved", ["Acidity regulator, raising agent"]),
    "E501": ("Potassium carbonates", AdditiveCategory.OTHER, "approved", "approved", ["Acidity regulator"]),
    "E503": ("Ammonium carbonates", AdditiveCategory.OTHER, "approved", "approved", ["Acidity regulator, raising agent"]),
    "E504": ("Magnesium carbonates", AdditiveCategory.OTHER, "approved", "approved", ["Acidity regulator, anti-caking agent"]),
    "E508": ("Potassium chloride", AdditiveCategory.OTHER, "approved", "approved", ["Salt substitute, gelling agent"]),
    "E509": ("Calcium chloride", AdditiveCategory.OTHER, "approved", "approved", ["Firming agent"]),
    "E516": ("Calcium sulphate", AdditiveCategory.OTHER, "approved", "approved", ["Firming agent, raising agent"]),

    # Flavor enhancers (E600-E699)
    "E620": ("Glutamic acid", AdditiveCategory.FLAVORING, "approved", "approved", ["Flavor enhancer"]),
    "E621": ("Monosodium glutamate (MSG)", AdditiveCategory.FLAVORING, "approved", "approved", ["Common flavor enhancer", "Some people report sensitivity"]),
    "E622": ("Monopotassium glutamate", AdditiveCategory.FLAVORING, "approved", "approved", ["Flavor enhancer"]),
    "E627": ("Disodium guanylate", AdditiveCategory.FLAVORING, "approved", "approved", ["Flavor enhancer"]),
    "E631": ("Disodium inosinate", AdditiveCategory.FLAVORING, "approved", "approved", ["Flavor enhancer"]),
    "E635": ("Disodium 5'-ribonucleotides", AdditiveCategory.FLAVORING, "approved", "approved", ["Flavor enhancer"]),

    # Sweeteners (E900-E999)
    "E950": ("Acesulfame K", AdditiveCategory.SWEETENER, "approved", "approved", ["Artificial sweetener"]),
    "E951": ("Aspartame", AdditiveCategory.SWEETENER, "approved", "approved", ["Artificial sweetener", "Not suitable for people with phenylketonuria"]),
    "E952": ("Cyclamate", AdditiveCategory.SWEETENER, "approved", "banned", ["Artificial sweetener"]),
    "E954": ("Saccharin", AdditiveCategory.SWEETENER, "approved", "approved", ["Artificial sweetener"]),
    "E955": ("Sucralose", AdditiveCategory.SWEETENER, "approved", "approved", ["Artificial sweetener"]),
    "E960": ("Steviol glycosides", AdditiveCategory.SWEETENER, "approved", "approved", ["Natural sweetener from stevia plant"]),
    "E965": ("Maltitol", AdditiveCategory.SWEETENER, "approved", "approved", ["Sugar alcohol", "May cause digestive discomfort in large amounts"]),
    "E966": ("Lactitol", AdditiveCategory.SWEETENER, "approved", "approved", ["Sugar alcohol"]),
    "E967": ("Xylitol", AdditiveCategory.SWEETENER, "approved", "approved", ["Sugar alcohol", "Toxic to dogs"]),

    # Common additives without E-numbers
    "sugar": ("Sugar", AdditiveCategory.SWEETENER, "approved", "approved", ["Common sweetener"]),
    "glucose syrup": ("Glucose syrup", AdditiveCategory.SWEETENER, "approved", "approved", ["Sweetener and thickener"]),
    "high fructose corn syrup": ("High fructose corn syrup", AdditiveCategory.SWEETENER, "approved", "approved", ["Sweetener"]),
    "corn syrup": ("Corn syrup", AdditiveCategory.SWEETENER, "approved", "approved", ["Sweetener"]),
    "maltodextrin": ("Maltodextrin", AdditiveCategory.OTHER, "approved", "approved", ["Bulking agent, carbohydrate"]),
    "salt": ("Salt", AdditiveCategory.OTHER, "approved", "approved", ["Flavor enhancer and preservative"]),
    "sodium chloride": ("Salt", AdditiveCategory.OTHER, "approved", "approved", ["Flavor enhancer and preservative"]),
    "lecithin": ("Lecithin", AdditiveCategory.EMULSIFIER, "approved", "approved", ["Natural emulsifier from soybeans or eggs"]),
    "soy lecithin": ("Soy lecithin", AdditiveCategory.EMULSIFIER, "approved", "approved", ["Natural emulsifier from soybeans"]),
    "sunflower lecithin": ("Sunflower lecithin", AdditiveCategory.EMULSIFIER, "approved", "approved", ["Natural emulsifier from sunflowers"]),
    "vanilla": ("Vanilla", AdditiveCategory.FLAVORING, "approved", "approved", ["Natural flavoring"]),
    "vanillin": ("Vanillin", AdditiveCategory.FLAVORING, "approved", "approved", ["Synthetic or natural vanilla flavoring"]),
    "natural flavors": ("Natural flavors", AdditiveCategory.FLAVORING, "approved", "approved", ["Flavoring from natural sources"]),
    "artificial flavors": ("Artificial flavors", AdditiveCategory.FLAVORING, "approved", "approved", ["Synthetic flavoring"]),
}


def get_additive_info(ingredient: str) -> Optional[Dict]:
    """
    Look up additive information by ingredient name or E-number.

    Args:
        ingredient: Ingredient name or E-number (case-insensitive)

    Returns:
        Dictionary with additive info or None if not found
    """
    ingredient_lower = ingredient.lower().strip()

    if ingredient_lower in ADDITIVE_DATABASE:
        common_name, category, eu_status, us_status, notes = ADDITIVE_DATABASE[ingredient_lower]
        return {
            "common_name": common_name,
            "category": category,
            "regulatory_status": {"EU": eu_status, "US": us_status},
            "notes": notes,
        }

    return None


def is_e_number(text: str) -> bool:
    """Check if text is an E-number format"""
    text = text.strip().upper()
    if not text.startswith("E"):
        return False
    rest = text[1:]
    # E-numbers are E + digits, optionally followed by a letter
    if rest and rest[0].isdigit():
        return True
    return False
