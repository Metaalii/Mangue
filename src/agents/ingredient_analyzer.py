"""Main Ingredient Analysis Agent

This is the main agent that orchestrates all steps of the ingredient analysis process.
It follows the specification exactly:
1. Extract & Normalize
2. Ingredient Facts
3. User Policy
4. Personalized Evaluation
5. User-Facing Explanation
"""

from typing import Optional
from ..models.schemas import (
    AnalysisInput,
    AnalysisResult,
    UserProfile,
    RiskSensitivity,
)
from .step1_extract import extract_and_normalize
from .step2_facts import extract_ingredient_facts
from .step3_policy import convert_user_profile
from .step4_evaluate import evaluate_ingredients
from .step5_output import generate_user_output


class IngredientAnalysisAgent:
    """
    Personalized Ingredient Analysis Agent

    This agent analyzes ingredient lists and provides personalized suitability verdicts
    based on user goals, constraints, and preferences.

    Core principles:
    - Separate FACTS from PERSONALIZED JUDGMENT from UX wording
    - Additives are not inherently bad; only raise concern when relevant to user's goals
    - No medical advice, no diagnoses, no fear-mongering
    - If uncertain, flag it in uncertainty_notes rather than guessing
    - Prefer scientific/regulatory consensus; avoid trends
    """

    def __init__(self, locale: str = "other"):
        """
        Initialize the agent.

        Args:
            locale: Default regulatory locale (EU, US, or other)
        """
        self.locale = locale

    def analyze(self, analysis_input: AnalysisInput) -> AnalysisResult:
        """
        Analyze an ingredient list with user profile.

        Args:
            analysis_input: AnalysisInput with ingredients_text, user_profile, and locale

        Returns:
            AnalysisResult with complete analysis
        """
        # Use input locale or default
        locale = analysis_input.locale or self.locale

        # Handle empty input
        if not analysis_input.ingredients_text or not analysis_input.ingredients_text.strip():
            return self._create_empty_result(analysis_input.user_profile)

        # STEP 1: Extract & Normalize
        parsed_ingredients = extract_and_normalize(analysis_input.ingredients_text)

        # STEP 2: Ingredient Facts (Objective)
        ingredient_facts = extract_ingredient_facts(parsed_ingredients, locale)

        # STEP 3: User Policy
        user_policy = convert_user_profile(analysis_input.user_profile)

        # STEP 4: Personalized Evaluation
        evaluation = evaluate_ingredients(ingredient_facts, user_policy)

        # STEP 5: User-Facing Explanation
        user_output = generate_user_output(ingredient_facts, evaluation)

        # Assemble complete result
        return AnalysisResult(
            parsed_ingredients=parsed_ingredients,
            ingredient_facts=ingredient_facts,
            user_policy=user_policy,
            evaluation=evaluation,
            user_output=user_output,
        )

    def analyze_simple(
        self,
        ingredients_text: str,
        goals: Optional[list] = None,
        constraints: Optional[list] = None,
        preferences: Optional[list] = None,
        risk_sensitivity: RiskSensitivity = RiskSensitivity.MEDIUM,
    ) -> AnalysisResult:
        """
        Simplified analysis method with direct parameters.

        Args:
            ingredients_text: Raw ingredient text
            goals: User's health/dietary goals
            constraints: Allergies, dietary rules, health constraints
            preferences: Preferences like avoiding additives, low sugar, etc.
            risk_sensitivity: User's risk sensitivity level

        Returns:
            AnalysisResult with complete analysis
        """
        user_profile = UserProfile(
            goals=goals or [],
            constraints=constraints or [],
            preferences=preferences or [],
            risk_sensitivity=risk_sensitivity,
        )

        analysis_input = AnalysisInput(
            ingredients_text=ingredients_text,
            user_profile=user_profile,
            locale=self.locale,
        )

        return self.analyze(analysis_input)

    def _create_empty_result(self, user_profile: UserProfile) -> AnalysisResult:
        """
        Create a result for empty ingredient text.

        Args:
            user_profile: User's profile

        Returns:
            AnalysisResult with MIXED_FIT verdict and uncertainty notes
        """
        from ..models.schemas import (
            ParsedIngredients,
            UserPolicy,
            Evaluation,
            Verdict,
            UserOutput,
        )

        parsed_ingredients = ParsedIngredients(
            original_list=[],
            canonical_map=[],
            unreadable_segments=["Empty or missing ingredient text"],
        )

        user_policy = convert_user_profile(user_profile)

        evaluation = Evaluation(
            verdict=Verdict.MIXED_FIT,
            key_reasons=[],
            tradeoffs=[],
            uncertainty_notes=["Cannot provide analysis due to missing ingredient information"],
        )

        user_output = UserOutput(
            INGREDIENT_SUMMARY=["No ingredient information provided"],
            USER_FIT_VERDICT="Mixed fit",
            WHY_THIS_MATTERS_FOR_YOU=["Unable to analyze without ingredient information"],
            FINAL_NOTE="Please provide ingredient information for a proper analysis.",
        )

        return AnalysisResult(
            parsed_ingredients=parsed_ingredients,
            ingredient_facts=[],
            user_policy=user_policy,
            evaluation=evaluation,
            user_output=user_output,
        )
