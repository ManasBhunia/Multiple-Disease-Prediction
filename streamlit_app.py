# streamlit_app.py

import streamlit as st
import numpy as np
import pickle

st.set_page_config(page_title="Multi-Disease Prediction", layout="centered")

st.title("🩺 Multi-Disease Prediction System")
st.write("Predict Diabetes and Heart Disease using Machine Learning")

# Load models
diabetes_model = pickle.load(open("diabetes_model.pkl", "rb"))
diabetes_scaler = pickle.load(open("diabetes_scaler.pkl", "rb"))

heart_model = pickle.load(open("heart_model.pkl", "rb"))
heart_scaler = pickle.load(open("heart_scaler.pkl", "rb"))

# ------------------ Diabetes Section ------------------
st.header("Diabetes Prediction")

diabetes_features = [
    st.number_input("Pregnancies", 0, 20),
    st.number_input("Glucose", 0, 200),
    st.number_input("Blood Pressure", 0, 150),
    st.number_input("Skin Thickness", 0, 100),
    st.number_input("Insulin", 0, 900),
    st.number_input("BMI", 0.0, 70.0),
    st.number_input("Diabetes Pedigree Function", 0.0, 3.0),
    st.number_input("Age", 1, 120)
]

if st.button("Predict Diabetes"):
    data = np.array(diabetes_features).reshape(1, -1)
    scaled = diabetes_scaler.transform(data)
    result = diabetes_model.predict(scaled)[0]

    if result == 1:
        st.error("⚠️ High risk of Diabetes")
    else:
        st.success("✅ Low risk of Diabetes")

# ------------------ Heart Disease Section ------------------
st.header("Heart Disease Prediction")

heart_features = [
    st.number_input("Age", 1, 120, key="age"),
    st.number_input("Sex (1=Male, 0=Female)", 0, 1),
    st.number_input("Chest Pain Type (0–3)", 0, 3),
    st.number_input("Resting BP", 80, 200),
    st.number_input("Cholesterol", 100, 600),
    st.number_input("Fasting Blood Sugar (1=True, 0=False)", 0, 1),
    st.number_input("Rest ECG (0–2)", 0, 2),
    st.number_input("Max Heart Rate", 60, 220),
    st.number_input("Exercise Induced Angina (1=Yes, 0=No)", 0, 1),
    st.number_input("Oldpeak", 0.0, 10.0),
    st.number_input("Slope (0–2)", 0, 2),
    st.number_input("CA (0–4)", 0, 4),
    st.number_input("Thal (0–3)", 0, 3)
]

if st.button("Predict Heart Disease"):
    data = np.array(heart_features).reshape(1, -1)
    scaled = heart_scaler.transform(data)
    result = heart_model.predict(scaled)[0]

    if result == 1:
        st.error("⚠️ High risk of Heart Disease")
    else:
        st.success("✅ Low risk of Heart Disease")
