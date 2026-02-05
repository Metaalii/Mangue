"""STEP 5 — USER-FACING EXPLANATION (CALM)"""

from typing import List
from ..models.schemas import (
    IngredientFact,
    Evaluation,
    UserOutput,
    Verdict,
    AdditiveCategory,
)


def generate_user_output(
    facts: List[IngredientFact],
    evaluation: Evaluation,
) -> UserOutput:
    """
    Step 5: Generate calm, user-facing explanation.

    Args:
        facts: List of ingredient facts
        evaluation: Evaluation results

    Returns:
        UserOutput with summary, verdict, and explanations
    """
    # Generate ingredient summary
    ingredient_summary = generate_ingredient_summary(facts)

    # Convert verdict to user-friendly text
    verdict_map = {
        Verdict.GOOD_FIT: "Good fit",
        Verdict.MIXED_FIT: "Mixed fit",
        Verdict.NOT_RECOMMENDED: "Not recommended",
    }
    user_fit_verdict = verdict_map[evaluation.verdict]

    # Generate personalized reasons
    why_matters = generate_why_matters(evaluation.key_reasons)

    # Generate final note
    final_note = generate_final_note(evaluation.verdict)

    return UserOutput(
        INGREDIENT_SUMMARY=ingredient_summary,
        USER_FIT_VERDICT=user_fit_verdict,
        WHY_THIS_MATTERS_FOR_YOU=why_matters,
        FINAL_NOTE=final_note,
    )


def generate_ingredient_summary(facts: List[IngredientFact]) -> List[str]:
    """Generate a summary of notable ingredients"""
    summary = []

    # Count ingredients by type
    total_count = len(facts)
    additive_count = sum(1 for f in facts if f.is_additive)
    natural_count = total_count - additive_count

    # Add count summary
    if natural_count > 0 and additive_count > 0:
        summary.append(f"Contains {total_count} ingredients: {natural_count} natural, {additive_count} additive(s)")
    elif additive_count == 0:
        summary.append(f"Contains {total_count} ingredients, primarily natural")
    else:
        summary.append(f"Contains {total_count} ingredients including {additive_count} additive(s)")

    # Highlight notable additives
    notable_additives = []
    for fact in facts:
        if fact.is_additive and fact.category in [
            AdditiveCategory.COLORING,
            AdditiveCategory.PRESERVATIVE,
            AdditiveCategory.SWEETENER,
        ]:
            common_name = fact.common_name or fact.canonical
            notable_additives.append(f"{common_name} ({fact.category.value})")

    if notable_additives:
        summary.append(f"Notable additives: {', '.join(notable_additives[:3])}")

    # Mention regulatory concerns
    banned_items = [f for f in facts if "banned" in (f.regulatory_status.EU or "") or "banned" in (f.regulatory_status.US or "")]
    if banned_items:
        for item in banned_items:
            if "banned" in (item.regulatory_status.EU or ""):
                summary.append(f"{item.canonical} is banned in the EU as of 2022")

    return summary


def generate_why_matters(key_reasons: List) -> List[str]:
    """Generate user-facing reasons (calm and factual)"""
    matters = []

    for reason in key_reasons:
        # Rewrite explanation to be calmer and more neutral
        explanation = reason.explanation

        # Remove alarmist language if any slipped through
        alarmist_replacements = {
            "dangerous": "may not be suitable",
            "toxic": "not recommended",
            "harmful": "may not align with your preferences",
            "bad for you": "may not be ideal for your goals",
        }
        for alarmist, calm in alarmist_replacements.items():
            explanation = explanation.replace(alarmist, calm)

        matters.append(f"{reason.ingredient}: {explanation}")

    return matters


def generate_final_note(verdict: Verdict) -> str:
    """Generate a calm closing note"""
    if verdict == Verdict.GOOD_FIT:
        return "This product aligns well with your stated preferences. As always, consider your individual needs and consumption patterns."

    elif verdict == Verdict.MIXED_FIT:
        return "This product has some ingredients that don't fully align with your preferences. Consider your priorities and how often you'd consume this."

    elif verdict == Verdict.NOT_RECOMMENDED:
        return "Based on your constraints, this product may not be the best fit. Consider alternatives that better match your requirements."

    return "Consider your individual needs and priorities when making food choices."
