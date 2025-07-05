#!/usr/bin/env python3
"""
Disease Prediction FastAPI Application
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import sys
import os

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.inference import predict_from_symptoms, get_available_symptoms, get_available_diseases, get_disease_info

# Create FastAPI app
app = FastAPI(
    title="Disease Prediction API",
    description="Predict diseases based on symptoms using machine learning",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your MERN app's domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class SymptomRequest(BaseModel):
    symptoms: List[str]
    model_name: Optional[str] = "randomforest"

class PredictionResponse(BaseModel):
    prediction: str
    confidence: float
    top_predictions: List[dict]
    disease_info: dict

class HealthResponse(BaseModel):
    status: str
    available_symptoms: int
    available_diseases: int

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Disease Prediction API",
        "version": "1.0.0",
        "endpoints": {
            "/health": "Check API health",
            "/symptoms": "Get available symptoms",
            "/diseases": "Get available diseases",
            "/predict": "Predict disease from symptoms",
            "/docs": "API documentation"
        }
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Check API health"""
    try:
        symptoms = get_available_symptoms()
        diseases = get_available_diseases()
        
        return HealthResponse(
            status="healthy",
            available_symptoms=len(symptoms),
            available_diseases=len(diseases)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")

@app.get("/symptoms", response_model=List[str])
async def get_symptoms():
    """Get list of available symptoms"""
    try:
        symptoms = get_available_symptoms()
        if not symptoms:
            raise HTTPException(status_code=404, detail="No symptoms found")
        return symptoms
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting symptoms: {str(e)}")

@app.get("/diseases", response_model=List[str])
async def get_diseases():
    """Get list of available diseases"""
    try:
        diseases = get_available_diseases()
        if not diseases:
            raise HTTPException(status_code=404, detail="No diseases found")
        return diseases
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting diseases: {str(e)}")

@app.post("/predict", response_model=PredictionResponse)
async def predict_disease(request: SymptomRequest):
    """Predict disease from symptoms"""
    try:
        if not request.symptoms:
            raise HTTPException(status_code=400, detail="No symptoms provided")
        
        prediction, top_predictions, error = predict_from_symptoms(
            request.symptoms, 
            request.model_name
        )
        
        if error:
            raise HTTPException(status_code=400, detail=error)
        
        if not prediction:
            raise HTTPException(status_code=500, detail="Prediction failed")
        
        disease_info = get_disease_info(prediction)
        confidence = top_predictions[0]['probability'] if top_predictions else 0.0
        
        return PredictionResponse(
            prediction=prediction,
            confidence=confidence,
            top_predictions=top_predictions,
            disease_info=disease_info
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@app.get("/predict/{symptoms}")
async def predict_disease_get(symptoms: str):
    """Predict disease from symptoms (GET method)"""
    try:
        symptom_list = [s.strip().lower() for s in symptoms.split(',')]
        request = SymptomRequest(symptoms=symptom_list)
        return await predict_disease(request)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    host = "0.0.0.0" if os.environ.get("PORT") else "127.0.0.1"
    
    print("🚀 Starting Disease Prediction API...")
    print(f"📖 API Documentation: http://{host}:{port}/docs")
    print(f"🔍 Health Check: http://{host}:{port}/health")
    print(f"🏥 Predict Disease: http://{host}:{port}/predict")
    
    uvicorn.run(
        app,
        host=host,
        port=port,
        reload=False,
        log_level="info"
    ) 