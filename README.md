# Mangue - Personalized Ingredient Analysis Agent

A calm, factual, personalized ingredient analysis agent for consumer health applications.

## Overview

Mangue is an intelligent agent that analyzes food ingredient lists and provides personalized suitability verdicts based on user goals, constraints, and preferences. It separates objective facts from personalized judgments and avoids fear-mongering while providing clear, actionable insights.

## Core Principles

- **Factual & Objective**: Separates FACTS from PERSONALIZED JUDGMENT from UX wording
- **Nuanced**: Additives are not inherently bad; only raises concerns when relevant to user's goals
- **Responsible**: No medical advice, no diagnoses, no fear-mongering, no absolute claims
- **Transparent**: Flags uncertainties rather than guessing
- **Science-Based**: Prefers scientific/regulatory consensus over trends

## Features

- **Ingredient Parsing**: Extracts and normalizes ingredients from OCR or pasted text
- **E-Number Recognition**: Comprehensive database of E-numbers and common additives
- **Allergen Detection**: Identifies common allergens (FDA and EU recognized)
- **Regulatory Status**: Tracks EU and US approval status
- **Personalized Evaluation**: Matches ingredients against user goals, constraints, and preferences
- **Risk Sensitivity**: Adjustable sensitivity levels (low, medium, high)
- **Calm Communication**: User-facing output emphasizes moderation and choice

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

### Option 1: Web Interface (Recommended)

The easiest way to use Mangue is through the beautiful web interface:

```bash
# Start the web application
python run_app.py
```

Then open your browser to: **http://localhost:8000**

The web interface provides:
- 🎨 Beautiful, intuitive UI
- 📝 Easy ingredient input
- 🎯 Interactive profile builder with tag inputs
- 🎚️ Risk sensitivity selector
- 📊 Clear, visual results with color-coded verdicts
- 📱 Fully responsive (works on mobile)

**API Documentation**: http://localhost:8000/docs

### Option 2: Python API

Use Mangue programmatically in your Python code:

```python
from src.agents import IngredientAnalysisAgent
from src.models import RiskSensitivity

# Initialize the agent
agent = IngredientAnalysisAgent(locale="EU")

# Analyze ingredients
result = agent.analyze_simple(
    ingredients_text="Sugar, wheat flour, water, cocoa powder, E471, E202, vanilla extract",
    goals=["eat healthier", "reduce processed foods"],
    constraints=["no peanuts"],
    preferences=["minimize additives", "natural ingredients"],
    risk_sensitivity=RiskSensitivity.MEDIUM,
)

# Access the results
print(f"Verdict: {result.user_output.USER_FIT_VERDICT}")
for reason in result.user_output.WHY_THIS_MATTERS_FOR_YOU:
    print(f"  - {reason}")

# Get full JSON output
print(result.to_json())
```

## Usage Examples

### Example 1: Basic Analysis

```python
agent = IngredientAnalysisAgent(locale="EU")

result = agent.analyze_simple(
    ingredients_text="Sugar, flour, water, E300",
    goals=["healthy eating"],
    preferences=["natural ingredients"],
)

print(result.user_output.USER_FIT_VERDICT)  # "Good fit" or "Mixed fit"
```

### Example 2: Allergen Detection

```python
result = agent.analyze_simple(
    ingredients_text="Milk chocolate, peanuts, soy lecithin",
    constraints=["peanut allergy", "lactose intolerant"],
    risk_sensitivity=RiskSensitivity.HIGH,
)

# Will flag milk and peanuts as conflicts
```

### Example 3: Vegan Diet

```python
result = agent.analyze_simple(
    ingredients_text="Wheat flour, water, sunflower oil, salt, yeast",
    constraints=["vegan"],
    goals=["plant-based diet"],
)

# Analyzes compatibility with vegan requirements
```

### Example 4: Using Full API

```python
from src.models import AnalysisInput, UserProfile, RiskSensitivity

user_profile = UserProfile(
    goals=["weight loss", "reduce sugar"],
    constraints=["lactose intolerant"],
    preferences=["avoid artificial sweeteners"],
    risk_sensitivity=RiskSensitivity.HIGH,
)

analysis_input = AnalysisInput(
    ingredients_text="Water, E951, citric acid, natural flavors",
    user_profile=user_profile,
    locale="US",
)

result = agent.analyze(analysis_input)
```

## Output Format

The agent returns a structured `AnalysisResult` with the following components:

### 1. Parsed Ingredients
```json
{
  "original_list": ["Sugar", "E471", "vanilla extract"],
  "canonical_map": [
    {"original": "Sugar", "canonical": "sugar", "confidence": 1.0}
  ],
  "unreadable_segments": []
}
```

### 2. Ingredient Facts
```json
{
  "canonical": "E471",
  "is_additive": true,
  "category": "emulsifier",
  "common_name": "Mono- and diglycerides of fatty acids",
  "regulatory_status": {"EU": "approved", "US": "approved"},
  "notes": ["Common emulsifier"],
  "uncertainty_notes": []
}
```

### 3. User Policy
```json
{
  "goals": ["eat healthier"],
  "hard_constraints": ["no peanuts"],
  "soft_preferences": ["minimize additives"],
  "risk_sensitivity": "medium"
}
```

### 4. Evaluation
```json
{
  "verdict": "MIXED_FIT",
  "key_reasons": [
    {
      "ingredient": "E471",
      "user_rule": "minimize additives",
      "explanation": "Additive (emulsifier) that you prefer to avoid"
    }
  ],
  "tradeoffs": ["Suitable for occasional consumption..."],
  "uncertainty_notes": []
}
```

### 5. User Output
```json
{
  "INGREDIENT_SUMMARY": ["Contains 7 ingredients: 5 natural, 2 additive(s)"],
  "USER_FIT_VERDICT": "Mixed fit",
  "WHY_THIS_MATTERS_FOR_YOU": [
    "E471: Additive (emulsifier) that you prefer to avoid"
  ],
  "FINAL_NOTE": "This product has some ingredients..."
}
```

## Processing Steps

The agent follows a strict 5-step process:

1. **Extract & Normalize**: Parse and normalize ingredient text
2. **Ingredient Facts**: Extract objective facts about each ingredient
3. **User Policy**: Convert user profile into structured policy
4. **Personalized Evaluation**: Evaluate ingredients against user policy
5. **User-Facing Explanation**: Generate calm, factual explanations

## Risk Sensitivity Levels

- **LOW**: Only flags strong conflicts; lenient on soft preferences
- **MEDIUM**: Balanced approach (default)
- **HIGH**: Stricter on soft preferences and uncertain additives

## Additive Database

Includes comprehensive data on:
- E100-E199: Colorings
- E200-E299: Preservatives
- E300-E399: Antioxidants
- E400-E599: Emulsifiers, stabilizers, thickeners
- E600-E699: Flavor enhancers
- E900-E999: Sweeteners
- Common additives without E-numbers

## Allergen Detection

Recognizes major allergens per FDA and EU regulations:
- Milk and dairy
- Eggs
- Fish
- Shellfish
- Tree nuts
- Peanuts
- Wheat/gluten
- Soybeans
- Sesame
- Celery
- Mustard
- Lupin
- Molluscs
- Sulphites

## REST API

Mangue provides a RESTful API for integration with other applications.

### Start the API Server

```bash
python run_app.py
```

### API Endpoints

#### POST `/api/analyze-simple`

Simplified analysis endpoint.

**Request:**
```json
{
  "ingredients_text": "sugar, flour, E471",
  "goals": ["eat healthier"],
  "constraints": ["vegan"],
  "preferences": ["avoid additives"],
  "risk_sensitivity": "medium",
  "locale": "EU"
}
```

**Response:**
```json
{
  "parsed_ingredients": {...},
  "ingredient_facts": [...],
  "user_policy": {...},
  "evaluation": {...},
  "user_output": {...}
}
```

#### POST `/api/analyze`

Full analysis with structured `AnalysisInput`.

#### GET `/api/health`

Health check endpoint.

### Example API Usage

```bash
# Using curl
curl -X POST "http://localhost:8000/api/analyze-simple" \
  -H "Content-Type: application/json" \
  -d '{
    "ingredients_text": "sugar, wheat flour, E471, E202",
    "constraints": ["vegan"],
    "preferences": ["avoid additives"],
    "risk_sensitivity": "medium"
  }'
```

```python
# Using Python requests
import requests

response = requests.post(
    "http://localhost:8000/api/analyze-simple",
    json={
        "ingredients_text": "sugar, wheat flour, E471, E202",
        "constraints": ["vegan"],
        "preferences": ["avoid additives"],
        "risk_sensitivity": "medium"
    }
)

result = response.json()
print(result["user_output"]["USER_FIT_VERDICT"])
```

## Running Examples

```bash
# Run all examples
python examples/basic_example.py
```

## Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_agent.py -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html
```

## Project Structure

```
Mangue/
├── src/
│   ├── agents/              # Agent implementation
│   │   ├── ingredient_analyzer.py  # Main agent
│   │   ├── step1_extract.py        # Extraction & normalization
│   │   ├── step2_facts.py          # Ingredient facts
│   │   ├── step3_policy.py         # User policy
│   │   ├── step4_evaluate.py       # Evaluation
│   │   └── step5_output.py         # User output
│   ├── models/              # Data models (Pydantic)
│   │   └── schemas.py
│   ├── data/                # Reference data
│   │   ├── additives.py     # E-numbers & additives
│   │   └── allergens.py     # Allergen database
│   └── utils/               # Utilities
│       └── text_utils.py    # Text processing
├── tests/                   # Tests
├── examples/                # Usage examples
├── requirements.txt
└── README.md
```

## API Reference

### IngredientAnalysisAgent

Main agent class for ingredient analysis.

#### `__init__(locale="other")`
Initialize the agent with a default locale.

#### `analyze(analysis_input: AnalysisInput) -> AnalysisResult`
Full analysis with structured input.

#### `analyze_simple(...) -> AnalysisResult`
Simplified analysis with direct parameters.

Parameters:
- `ingredients_text` (str): Raw ingredient text
- `goals` (list, optional): User's health/dietary goals
- `constraints` (list, optional): Allergies, dietary rules
- `preferences` (list, optional): Preferences like avoiding additives
- `risk_sensitivity` (RiskSensitivity, optional): Risk sensitivity level

## Validation Rules

- Output is always valid JSON
- User output never introduces facts not present in ingredient_facts/evaluation
- Empty ingredient text returns MIXED_FIT with uncertainty notes
- All uncertainties are explicitly flagged in uncertainty_notes

## Limitations

- Not a substitute for medical advice
- Does not diagnose conditions
- Relies on accurate ingredient text input
- Limited to ingredients in the reference database (unknown ingredients are flagged)

## Contributing

Contributions are welcome! Please ensure:
- Code follows existing patterns
- Tests are included for new features
- Documentation is updated
- Principles of calm, factual communication are maintained

## License

[Add license information]

## Version

0.1.0 - Initial MVP release
