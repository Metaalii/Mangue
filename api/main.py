"""FastAPI backend for Mangue Ingredient Analysis"""

import logging
import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

from src.agents.ingredient_analyzer import IngredientAnalysisAgent
from src.models.schemas import AnalysisInput, AnalysisResult, IngredientInput

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Configuration
MAX_INGREDIENT_TEXT_LENGTH = 50000  # 50KB max input
ALLOWED_ORIGINS = os.environ.get("ALLOWED_ORIGINS", "http://localhost:8000,http://127.0.0.1:8000").split(",")

app = FastAPI(
    title="Mangue - Ingredient Analysis API",
    description="Personalized ingredient analysis for consumer health",
    version="0.1.0",
)

# CORS middleware - configurable origins for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS if os.environ.get("PRODUCTION") else ["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

# Mount static files
static_dir = Path(__file__).parent / "static"
static_dir.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Initialize agent
agent = IngredientAnalysisAgent(locale="EU")


@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main UI"""
    ui_file = Path(__file__).parent / "ui" / "index.html"
    if ui_file.exists():
        return FileResponse(ui_file)
    return """
    <html>
        <body>
            <h1>Mangue API</h1>
            <p>API is running. UI not found.</p>
            <p>Visit <a href="/docs">/docs</a> for API documentation.</p>
        </body>
    </html>
    """


@app.post("/api/analyze", response_model=AnalysisResult)
async def analyze_ingredients(input_data: AnalysisInput, request: Request):
    """
    Analyze ingredients with user profile.

    Returns complete analysis including verdict, reasons, and user-facing output.
    """
    # Input size validation
    ingredients_text = input_data.ingredients_text
    if len(ingredients_text) > MAX_INGREDIENT_TEXT_LENGTH:
        logger.warning(f"Input too large: {len(ingredients_text)} bytes from {request.client.host}")
        raise HTTPException(
            status_code=400,
            detail=f"Ingredient text too large. Maximum {MAX_INGREDIENT_TEXT_LENGTH} characters allowed."
        )

    try:
        logger.info(f"Analyzing {len(ingredients_text)} chars from {request.client.host}")
        result = agent.analyze(input_data)
        logger.info(f"Analysis complete: verdict={result.evaluation.verdict}")
        return result
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception(f"Analysis failed: {e}")
        raise HTTPException(status_code=500, detail="Analysis failed. Please try again.")


@app.post("/api/analyze-simple", response_model=AnalysisResult)
async def analyze_simple(input_data: IngredientInput, request: Request):
    """
    Simplified analysis endpoint.

    Takes ingredients text and optional user parameters.
    """
    # Input size validation
    ingredients_text = input_data.ingredients_text
    if len(ingredients_text) > MAX_INGREDIENT_TEXT_LENGTH:
        logger.warning(f"Input too large: {len(ingredients_text)} bytes from {request.client.host}")
        raise HTTPException(
            status_code=400,
            detail=f"Ingredient text too large. Maximum {MAX_INGREDIENT_TEXT_LENGTH} characters allowed."
        )

    try:
        logger.info(f"Simple analysis: {len(ingredients_text)} chars from {request.client.host}")
        analysis_input = input_data.to_analysis_input()
        result = agent.analyze(analysis_input)
        logger.info(f"Analysis complete: verdict={result.evaluation.verdict}")
        return result
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception(f"Analysis failed: {e}")
        raise HTTPException(status_code=500, detail="Analysis failed. Please try again.")


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Mangue Ingredient Analysis"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
