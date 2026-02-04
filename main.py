from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import pickle

app = FastAPI(
    title="Multi-Disease Prediction API",
    description="Predicts Diabetes and Heart Disease using ML models",
    version="1.0"
)

diabetes_model = pickle.load(open("diabetes_model.pkl", "rb"))
diabetes_scaler = pickle.load(open("diabetes_scaler.pkl", "rb"))

heart_model = pickle.load(open("heart_model.pkl", "rb"))
heart_scaler = pickle.load(open("heart_scaler.pkl", "rb"))

class PatientData(BaseModel):
    diabetes_features: list[float]
    heart_features: list[float]

@app.get("/")
def home():
    return {"message": "Multi-Disease Prediction API is running"}

@app.post("/predict")
def predict_disease(data: PatientData):
    
    diabetes_input = np.array(data.diabetes_features).reshape(1, -1)
    diabetes_scaled = diabetes_scaler.transform(diabetes_input)
    diabetes_prediction = diabetes_model.predict(diabetes_scaled)[0]

    
    heart_input = np.array(data.heart_features).reshape(1, -1)
    heart_scaled = heart_scaler.transform(heart_input)
    heart_prediction = heart_model.predict(heart_scaled)[0]

    return {
        "diabetes_prediction": int(diabetes_prediction),
        "heart_disease_prediction": int(heart_prediction)
    }
