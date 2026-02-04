import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import pickle

diabetes_data = pd.read_csv("diabetes.csv")

X_diabetes = diabetes_data.drop("Outcome", axis=1)
y_diabetes = diabetes_data["Outcome"]

diabetes_scaler = StandardScaler()
X_diabetes_scaled = diabetes_scaler.fit_transform(X_diabetes)

X_train, X_test, y_train, y_test = train_test_split(
    X_diabetes_scaled, y_diabetes, test_size=0.2, random_state=42
)

diabetes_model = RandomForestClassifier(random_state=42)
diabetes_model.fit(X_train, y_train)

pickle.dump(diabetes_model, open("diabetes_model.pkl", "wb"))
pickle.dump(diabetes_scaler, open("diabetes_scaler.pkl", "wb"))

print("✅ Diabetes model trained and saved")

heart_data = pd.read_csv("heart.csv")

X_heart = heart_data.drop("target", axis=1)
y_heart = heart_data["target"]

heart_scaler = StandardScaler()
X_heart_scaled = heart_scaler.fit_transform(X_heart)

X_train, X_test, y_train, y_test = train_test_split(
    X_heart_scaled, y_heart, test_size=0.2, random_state=42
)

heart_model = RandomForestClassifier(random_state=42)
heart_model.fit(X_train, y_train)

pickle.dump(heart_model, open("heart_model.pkl", "wb"))
pickle.dump(heart_scaler, open("heart_scaler.pkl", "wb"))

print("✅ Heart disease model trained and saved")
