"""FastAPI backend for Mangue Ingredient Analysis"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

from src.agents.ingredient_analyzer import IngredientAnalysisAgent
from src.models.schemas import AnalysisInput, AnalysisResult, IngredientInput

app = FastAPI(
    title="Mangue - Ingredient Analysis API",
    description="Personalized ingredient analysis for consumer health",
    version="0.1.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
async def analyze_ingredients(input_data: AnalysisInput):
    """
    Analyze ingredients with user profile.

    Returns complete analysis including verdict, reasons, and user-facing output.
    """
    try:
        result = agent.analyze(input_data)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.post("/api/analyze-simple", response_model=AnalysisResult)
async def analyze_simple(input_data: IngredientInput):
    """
    Simplified analysis endpoint.

    Takes ingredients text and optional user parameters.
    """
    try:
        analysis_input = input_data.to_analysis_input()
        result = agent.analyze(analysis_input)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Mangue Ingredient Analysis"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
