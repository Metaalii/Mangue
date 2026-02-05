"""STEP 4 — PERSONALIZED EVALUATION"""

from typing import List
from ..models.schemas import (
    IngredientFact,
    UserPolicy,
    Evaluation,
    KeyReason,
    Verdict,
    RiskSensitivity,
    AdditiveCategory,
)
from ..data.allergens import check_allergen


def evaluate_ingredients(
    facts: List[IngredientFact],
    policy: UserPolicy,
) -> Evaluation:
    """
    Step 4: Evaluate ingredients against user policy.

    Args:
        facts: List of ingredient facts
        policy: User policy

    Returns:
        Evaluation with verdict, reasons, and trade-offs
    """
    # Find all conflicts and benefits
    key_reasons = []
    uncertainty_notes = []
    conflict_severity_score = 0

    for fact in facts:
        # Check hard constraints
        hard_conflicts = check_hard_constraints(fact, policy.hard_constraints)
        for conflict in hard_conflicts:
            key_reasons.append(conflict)
            conflict_severity_score += 10  # Hard constraint = major conflict

        # Check soft preferences
        soft_conflicts = check_soft_preferences(fact, policy.soft_preferences, policy.risk_sensitivity)
        for conflict in soft_conflicts:
            key_reasons.append(conflict)
            conflict_severity_score += 3  # Soft preference = minor conflict

        # Check goals alignment
        goal_alignments = check_goal_alignment(fact, policy.goals)
        for alignment in goal_alignments:
            key_reasons.append(alignment)
            conflict_severity_score -= 2  # Positive alignment

        # Collect uncertainties
        if fact.uncertainty_notes:
            uncertainty_notes.extend(fact.uncertainty_notes)

    # Determine verdict based on conflict severity
    if conflict_severity_score >= 10:
        verdict = Verdict.NOT_RECOMMENDED
    elif conflict_severity_score >= 3:
        verdict = Verdict.MIXED_FIT
    else:
        verdict = Verdict.GOOD_FIT

    # Limit key_reasons to 3-6 most important
    key_reasons = prioritize_reasons(key_reasons, policy.risk_sensitivity)[:6]

    # Generate trade-offs
    tradeoffs = generate_tradeoffs(facts, verdict, policy)

    return Evaluation(
        verdict=verdict,
        key_reasons=key_reasons,
        tradeoffs=tradeoffs,
        uncertainty_notes=uncertainty_notes,
    )


def check_hard_constraints(fact: IngredientFact, hard_constraints: List[str]) -> List[KeyReason]:
    """Check if ingredient violates hard constraints"""
    reasons = []

    # Map allergen categories to common constraint keywords users might type
    ALLERGEN_CONSTRAINT_MAP = {
        "milk": ["milk", "dairy", "lactose"],
        "eggs": ["egg", "eggs"],
        "fish": ["fish"],
        "shellfish": ["shellfish", "crustacean", "shrimp", "crab", "lobster"],
        "tree_nuts": ["nut", "nuts", "tree nut", "almond", "walnut", "cashew", "pecan", "pistachio", "hazelnut"],
        "peanuts": ["peanut", "groundnut"],
        "wheat": ["wheat", "gluten", "celiac", "coeliac"],
        "soybeans": ["soy", "soya", "soybean"],
        "sesame": ["sesame"],
        "celery": ["celery"],
        "mustard": ["mustard"],
        "lupin": ["lupin", "lupine"],
        "molluscs": ["mollusc", "mollusk", "shellfish", "squid", "octopus", "clam", "mussel", "oyster"],
        "sulphites": ["sulphite", "sulfite", "sulphur", "sulfur"],
    }

    for constraint in hard_constraints:
        constraint_lower = constraint.lower()

        # Check for allergens - improved matching logic
        allergens = check_allergen(fact.canonical)
        for allergen in allergens:
            # Check if constraint mentions this allergen category or related keywords
            is_allergy_constraint = any(kw in constraint_lower for kw in ["allergy", "allergic", "intolerant", "intolerance"])
            allergen_keywords = ALLERGEN_CONSTRAINT_MAP.get(allergen, [allergen])
            constraint_mentions_allergen = any(kw in constraint_lower for kw in allergen_keywords)

            if constraint_mentions_allergen or (is_allergy_constraint and allergen in constraint_lower):
                reasons.append(
                    KeyReason(
                        ingredient=fact.canonical,
                        user_rule=constraint,
                        explanation=f"Contains {allergen}, which conflicts with your constraint: {constraint}",
                    )
                )
                break  # Don't add duplicate reasons for same constraint

        # Check for dietary restrictions - expanded vegan keywords
        if "vegan" in constraint_lower:
            non_vegan_keywords = [
                "milk", "egg", "honey", "gelatin", "whey", "casein", "lactose",
                "butter", "cream", "cheese", "yogurt", "ghee", "albumin", "ovalbumin",
                "shellac", "carmine", "cochineal", "isinglass", "lard", "tallow",
                "beeswax", "royal jelly", "propolis", "lanolin", "keratin",
                "collagen", "bone", "rennet", "pepsin", "anchovies"
            ]
            if any(keyword in fact.canonical.lower() for keyword in non_vegan_keywords):
                reasons.append(
                    KeyReason(
                        ingredient=fact.canonical,
                        user_rule=constraint,
                        explanation=f"Not suitable for vegan diet",
                    )
                )

        if "vegetarian" in constraint_lower:
            non_vegetarian_keywords = [
                "gelatin", "cochineal", "carmine", "isinglass", "lard", "tallow",
                "rennet", "pepsin", "bone", "meat", "beef", "pork", "chicken",
                "fish", "anchovy", "anchovies"
            ]
            if any(keyword in fact.canonical.lower() for keyword in non_vegetarian_keywords):
                reasons.append(
                    KeyReason(
                        ingredient=fact.canonical,
                        user_rule=constraint,
                        explanation=f"May not be suitable for vegetarian diet",
                    )
                )

        # Check if ingredient name is in constraint
        if fact.canonical.lower() in constraint_lower or constraint_lower in fact.canonical.lower():
            reasons.append(
                KeyReason(
                    ingredient=fact.canonical,
                    user_rule=constraint,
                    explanation=f"Directly conflicts with your constraint",
                )
            )

    return reasons


def check_soft_preferences(
    fact: IngredientFact,
    soft_preferences: List[str],
    risk_sensitivity: RiskSensitivity,
) -> List[KeyReason]:
    """Check if ingredient conflicts with soft preferences"""
    reasons = []

    for pref in soft_preferences:
        pref_lower = pref.lower()

        # Avoid artificial additives
        if any(keyword in pref_lower for keyword in ["artificial", "additive", "e-number", "synthetic"]):
            if fact.is_additive and fact.category in [
                AdditiveCategory.COLORING,
                AdditiveCategory.PRESERVATIVE,
                AdditiveCategory.SWEETENER,
            ]:
                # For high risk sensitivity, flag all additives
                if risk_sensitivity == RiskSensitivity.HIGH:
                    reasons.append(
                        KeyReason(
                            ingredient=fact.canonical,
                            user_rule=pref,
                            explanation=f"Additive ({fact.category.value}) that you prefer to avoid",
                        )
                    )
                # For medium/low, only flag if notes suggest concerns
                elif any(keyword in " ".join(fact.notes).lower() for keyword in ["may cause", "concern", "sensitive"]):
                    reasons.append(
                        KeyReason(
                            ingredient=fact.canonical,
                            user_rule=pref,
                            explanation=f"Additive with potential sensitivity concerns",
                        )
                    )

        # Avoid sugar/sweeteners
        if any(keyword in pref_lower for keyword in ["sugar", "sweet"]):
            if fact.category == AdditiveCategory.SWEETENER or "sugar" in fact.canonical.lower() or "syrup" in fact.canonical.lower():
                reasons.append(
                    KeyReason(
                        ingredient=fact.canonical,
                        user_rule=pref,
                        explanation=f"Sweetener or sugar that you prefer to limit",
                    )
                )

        # Minimally processed
        if "processed" in pref_lower or "natural" in pref_lower or "clean" in pref_lower:
            if fact.is_additive and risk_sensitivity == RiskSensitivity.HIGH:
                reasons.append(
                    KeyReason(
                        ingredient=fact.canonical,
                        user_rule=pref,
                        explanation=f"Processed additive that may not align with preference for natural ingredients",
                    )
                )

    return reasons


def check_goal_alignment(fact: IngredientFact, goals: List[str]) -> List[KeyReason]:
    """Check if ingredient aligns positively with user goals"""
    reasons = []

    for goal in goals:
        goal_lower = goal.lower()

        # Weight loss / low calorie
        if any(keyword in goal_lower for keyword in ["weight", "calorie", "slim", "lose"]):
            if fact.category == AdditiveCategory.SWEETENER and fact.canonical.lower() not in ["sugar", "glucose", "fructose"]:
                reasons.append(
                    KeyReason(
                        ingredient=fact.canonical,
                        user_rule=goal,
                        explanation=f"Low-calorie sweetener that may support your goal",
                    )
                )

        # Natural / whole foods
        if any(keyword in goal_lower for keyword in ["natural", "whole", "clean"]):
            if not fact.is_additive or fact.category == AdditiveCategory.NONE:
                reasons.append(
                    KeyReason(
                        ingredient=fact.canonical,
                        user_rule=goal,
                        explanation=f"Natural ingredient aligning with your goal",
                    )
                )

    return reasons


def prioritize_reasons(reasons: List[KeyReason], risk_sensitivity: RiskSensitivity) -> List[KeyReason]:
    """Prioritize reasons by importance"""
    # Sort by whether they mention conflicts/concerns first
    def reason_priority(reason: KeyReason) -> int:
        explanation_lower = reason.explanation.lower()

        if "conflicts with your constraint" in explanation_lower:
            return 0  # Highest priority
        if "allergy" in explanation_lower or "allergen" in explanation_lower:
            return 1
        if "not suitable" in explanation_lower:
            return 2
        if "concern" in explanation_lower:
            return 3
        if "prefer to avoid" in explanation_lower:
            return 4
        if "may support" in explanation_lower or "aligning with" in explanation_lower:
            return 5  # Positive reasons

        return 6

    return sorted(reasons, key=reason_priority)


def generate_tradeoffs(facts: List[IngredientFact], verdict: Verdict, policy: UserPolicy) -> List[str]:
    """Generate trade-off considerations"""
    tradeoffs = []

    # Count additives
    additive_count = sum(1 for f in facts if f.is_additive)

    if verdict == Verdict.MIXED_FIT:
        tradeoffs.append("Suitable for occasional consumption, but may not align with daily dietary preferences")

        if additive_count > 0:
            tradeoffs.append(f"Contains {additive_count} additive(s); consider frequency of consumption")

    elif verdict == Verdict.GOOD_FIT:
        if policy.risk_sensitivity == RiskSensitivity.HIGH and additive_count > 0:
            tradeoffs.append("While generally suitable, contains some additives that may be worth noting given your preferences")

    elif verdict == Verdict.NOT_RECOMMENDED:
        tradeoffs.append("Consider alternatives that better align with your dietary requirements")

    return tradeoffs
