"""Pydantic schemas matching the exact JSON output format specification"""

from typing import List, Dict, Optional, Literal
from pydantic import BaseModel, Field
from enum import Enum


class RiskSensitivity(str, Enum):
    """User's risk sensitivity level"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Verdict(str, Enum):
    """Final verdict for product suitability"""
    GOOD_FIT = "GOOD_FIT"
    MIXED_FIT = "MIXED_FIT"
    NOT_RECOMMENDED = "NOT_RECOMMENDED"


class AdditiveCategory(str, Enum):
    """Categories of food additives"""
    COLORING = "coloring"
    PRESERVATIVE = "preservative"
    EMULSIFIER = "emulsifier"
    SWEETENER = "sweetener"
    FLAVORING = "flavoring"
    OTHER = "other"
    NONE = "none"


# INPUT MODELS

class UserProfile(BaseModel):
    """User profile with goals, constraints, and preferences"""
    goals: List[str] = Field(default_factory=list, description="User's health/dietary goals")
    constraints: List[str] = Field(default_factory=list, description="Allergies, dietary rules, health constraints")
    preferences: List[str] = Field(default_factory=list, description="Preferences like avoiding additives, low sugar, etc.")
    risk_sensitivity: RiskSensitivity = Field(default=RiskSensitivity.MEDIUM, description="User's risk sensitivity")


class AnalysisInput(BaseModel):
    """Input for ingredient analysis"""
    ingredients_text: str = Field(description="Raw ingredient text from OCR or paste")
    user_profile: UserProfile = Field(description="User's profile with goals and constraints")
    locale: Optional[Literal["EU", "US", "other"]] = Field(default="other", description="Regulatory locale")


# OUTPUT MODELS

class CanonicalMapping(BaseModel):
    """Mapping from original ingredient text to canonical form"""
    original: str = Field(description="Original ingredient text")
    canonical: str = Field(description="Normalized/canonical ingredient name")
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence in the mapping")


class ParsedIngredients(BaseModel):
    """Parsed and normalized ingredients"""
    original_list: List[str] = Field(description="Original ingredient list as parsed")
    canonical_map: List[CanonicalMapping] = Field(description="Mapping to canonical forms")
    unreadable_segments: List[str] = Field(default_factory=list, description="Segments that couldn't be parsed")


class RegulatoryStatus(BaseModel):
    """Regulatory status in different regions"""
    EU: Optional[str] = Field(default=None, description="EU regulatory status")
    US: Optional[str] = Field(default=None, description="US regulatory status")


class IngredientFact(BaseModel):
    """Objective facts about an ingredient"""
    canonical: str = Field(description="Canonical ingredient name")
    is_additive: bool = Field(description="Whether this is a food additive")
    category: AdditiveCategory = Field(description="Category of additive or 'none'")
    common_name: Optional[str] = Field(default=None, description="Common name if different from canonical")
    regulatory_status: RegulatoryStatus = Field(default_factory=RegulatoryStatus, description="Regulatory status")
    notes: List[str] = Field(default_factory=list, description="Well-established neutral notes")
    uncertainty_notes: List[str] = Field(default_factory=list, description="Uncertainties or unknowns")


class UserPolicy(BaseModel):
    """Interpreted user policy from profile"""
    goals: List[str] = Field(description="User's stated goals")
    hard_constraints: List[str] = Field(description="Must-avoid items")
    soft_preferences: List[str] = Field(description="Should-avoid items")
    risk_sensitivity: RiskSensitivity = Field(description="Risk sensitivity level")


class KeyReason(BaseModel):
    """A key reason for the verdict"""
    ingredient: str = Field(description="The ingredient in question")
    user_rule: str = Field(description="The user rule/constraint it relates to")
    explanation: str = Field(description="Clear explanation of the issue or benefit")


class Evaluation(BaseModel):
    """Personalized evaluation of the ingredient list"""
    verdict: Verdict = Field(description="Overall verdict")
    key_reasons: List[KeyReason] = Field(description="3-6 key reasons for the verdict")
    tradeoffs: List[str] = Field(default_factory=list, description="Trade-offs to consider")
    uncertainty_notes: List[str] = Field(default_factory=list, description="Uncertainties in the evaluation")


class UserOutput(BaseModel):
    """User-facing calm and factual output"""
    INGREDIENT_SUMMARY: List[str] = Field(description="Summary of notable ingredients")
    USER_FIT_VERDICT: str = Field(description="Human-readable verdict: 'Good fit', 'Mixed fit', or 'Not recommended'")
    WHY_THIS_MATTERS_FOR_YOU: List[str] = Field(description="3-6 personalized reasons")
    FINAL_NOTE: str = Field(description="Closing note emphasizing choice and moderation")


class AnalysisResult(BaseModel):
    """Complete analysis result matching the exact output format"""
    parsed_ingredients: ParsedIngredients = Field(description="Extracted and normalized ingredients")
    ingredient_facts: List[IngredientFact] = Field(description="Objective facts about each ingredient")
    user_policy: UserPolicy = Field(description="Interpreted user policy")
    evaluation: Evaluation = Field(description="Personalized evaluation")
    user_output: UserOutput = Field(description="User-facing explanation")

    def to_json(self) -> str:
        """Convert to JSON string"""
        return self.model_dump_json(indent=2, exclude_none=False)


# Convenience input model
class IngredientInput(BaseModel):
    """Simplified input for quick analysis"""
    ingredients_text: str
    goals: Optional[List[str]] = None
    constraints: Optional[List[str]] = None
    preferences: Optional[List[str]] = None
    risk_sensitivity: Optional[RiskSensitivity] = RiskSensitivity.MEDIUM
    locale: Optional[Literal["EU", "US", "other"]] = "other"

    def to_analysis_input(self) -> AnalysisInput:
        """Convert to full AnalysisInput"""
        return AnalysisInput(
            ingredients_text=self.ingredients_text,
            user_profile=UserProfile(
                goals=self.goals or [],
                constraints=self.constraints or [],
                preferences=self.preferences or [],
                risk_sensitivity=self.risk_sensitivity or RiskSensitivity.MEDIUM,
            ),
            locale=self.locale,
        )
