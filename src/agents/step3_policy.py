"""STEP 3 — USER POLICY (NO NEW INVENTED INFO)"""

from ..models.schemas import UserProfile, UserPolicy, RiskSensitivity


def convert_user_profile(profile: UserProfile) -> UserPolicy:
    """
    Step 3: Convert user_profile into structured policy.

    Args:
        profile: Raw UserProfile

    Returns:
        UserPolicy with categorized constraints and preferences
    """
    hard_constraints = extract_hard_constraints(profile.constraints)
    soft_preferences = extract_soft_preferences(profile.preferences)

    return UserPolicy(
        goals=profile.goals,
        hard_constraints=hard_constraints,
        soft_preferences=soft_preferences,
        risk_sensitivity=profile.risk_sensitivity,
    )


def extract_hard_constraints(constraints: list) -> list:
    """
    Extract hard constraints (must avoid).

    Args:
        constraints: List of user constraints

    Returns:
        List of hard constraints
    """
    hard_constraints = []

    for constraint in constraints:
        constraint_lower = constraint.lower()

        # Allergies are always hard constraints
        if any(keyword in constraint_lower for keyword in ["allergy", "allergic", "intolerant", "intolerance"]):
            hard_constraints.append(constraint)
            continue

        # Medical conditions are hard constraints
        if any(keyword in constraint_lower for keyword in ["diabetes", "celiac", "phenylketonuria", "pku"]):
            hard_constraints.append(constraint)
            continue

        # Dietary restrictions can be hard or soft, default to hard
        if any(keyword in constraint_lower for keyword in ["vegan", "vegetarian", "halal", "kosher", "gluten-free"]):
            hard_constraints.append(constraint)
            continue

        # If labeled as "must avoid" or "cannot have"
        if any(keyword in constraint_lower for keyword in ["must avoid", "cannot have", "forbidden", "prohibited"]):
            hard_constraints.append(constraint)
            continue

        # Default: treat as hard constraint
        hard_constraints.append(constraint)

    return hard_constraints


def extract_soft_preferences(preferences: list) -> list:
    """
    Extract soft preferences (should avoid when possible).

    Args:
        preferences: List of user preferences

    Returns:
        List of soft preferences
    """
    soft_preferences = []

    for pref in preferences:
        pref_lower = pref.lower()

        # These are typically soft preferences
        soft_keywords = [
            "prefer", "avoid", "minimize", "reduce", "limit",
            "try to avoid", "should avoid", "would like to avoid",
            "less", "low", "no artificial", "natural", "organic",
            "minimally processed", "clean",
        ]

        # Check if it's phrased as a soft preference
        if any(keyword in pref_lower for keyword in soft_keywords):
            soft_preferences.append(pref)
            continue

        # Default: treat preferences as soft
        soft_preferences.append(pref)

    return soft_preferences
