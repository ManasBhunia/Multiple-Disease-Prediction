import streamlit as st
import pickle
import numpy as np
import sqlite3
from datetime import date

# ------------------ Page Config ------------------
st.set_page_config(page_title="Disease Prediction System", layout="centered")

# ------------------ Database ------------------
conn = sqlite3.connect("users.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS users (
    email TEXT PRIMARY KEY,
    password TEXT,
    first_name TEXT,
    last_name TEXT,
    mobile TEXT,
    dob TEXT,
    age INTEGER,
    gender TEXT,
    blood_group TEXT
)
""")
conn.commit()

# ------------------ Helper Functions ------------------
def signup(data):
    c.execute("INSERT INTO users VALUES (?,?,?,?,?,?,?,?,?)", data)
    conn.commit()

def login(email, password):
    c.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
    return c.fetchone()

def get_user(email):
    c.execute("SELECT * FROM users WHERE email=?", (email,))
    return c.fetchone()

def update_user(data):
    c.execute("""
        UPDATE users SET
        first_name=?,
        last_name=?,
        mobile=?,
        dob=?,
        age=?,
        gender=?,
        blood_group=?
        WHERE email=?
    """, data)
    conn.commit()

# ------------------ Load Models ------------------
diabetes_model = pickle.load(open("diabetes_model.pkl", "rb"))
diabetes_scaler = pickle.load(open("diabetes_scaler.pkl", "rb"))

heart_model = pickle.load(open("heart_model.pkl", "rb"))
heart_scaler = pickle.load(open("heart_scaler.pkl", "rb"))

# ------------------ Session ------------------
if "page" not in st.session_state:
    st.session_state.page = "login"

# ==========================================================
# LOGIN PAGE
# ==========================================================
if st.session_state.page == "login":

    st.title("🔐 Patient Login")

    email = st.text_input("Email ID")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = login(email, password)
        if user:
            st.session_state.user_email = email
            st.session_state.page = "dashboard"
            st.rerun()
        else:
            st.error("Invalid email or password")

    if st.button("New patient? Sign Up"):
        st.session_state.page = "signup"
        st.rerun()

# ==========================================================
# SIGNUP PAGE
# ==========================================================
elif st.session_state.page == "signup":

    st.title("📝 Patient Registration")

    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    email = st.text_input("Email ID")
    password = st.text_input("Password", type="password")
    mobile = st.text_input("Mobile Number")

    dob = st.date_input("Date of Birth",
                        min_value=date(1900,1,1),
                        max_value=date.today())

    age = st.number_input("Age", 1, 120)
    gender = st.selectbox("Gender", ["Male","Female","Other"])
    blood_group = st.selectbox(
        "Blood Group",
        ["Not specified","A+","A-","B+","B-","O+","O-","AB+","AB-"]
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Create Account", use_container_width=True):
            signup((email,password,first_name,last_name,
                    mobile,str(dob),age,gender,blood_group))
            st.success("Account created successfully")
            st.session_state.page = "login"
            st.rerun()

    with col2:
        if st.button("Back", use_container_width=True):
            st.session_state.page = "login"
            st.rerun()

# ==========================================================
# DASHBOARD
# ==========================================================
elif st.session_state.page == "dashboard":

    st.title("🏥 Patient Dashboard")

    user = get_user(st.session_state.user_email)

    if user:
        st.subheader("👤 Patient Details")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown("**Name**")
            st.write(f"{user[2]} {user[3]}")

        with col2:
            st.markdown("**DOB / Age**")
            st.write(f"{user[5]} / {user[6]}")

        with col3:
            st.markdown("**Gender / Blood Group**")
            st.write(f"{user[7]} / {user[8]}")

        with col4:
            st.markdown("**Mobile**")
            st.write(user[4])

    st.divider()

    colA, colB = st.columns(2)

    with colA:
        if st.button("❤️ Heart Disease Prediction", use_container_width=True):
            st.session_state.page = "heart"
            st.rerun()

    with colB:
        if st.button("🩸 Diabetes Prediction", use_container_width=True):
            st.session_state.page = "diabetes"
            st.rerun()

    st.divider()

    colX, colY = st.columns(2)

    with colX:
        if st.button("✏️ Edit Profile", use_container_width=True):
            st.session_state.page = "edit_profile"
            st.rerun()

    with colY:
        if st.button("Logout", use_container_width=True):
            st.session_state.page = "login"
            st.rerun()

# ==========================================================
# EDIT PROFILE
# ==========================================================
elif st.session_state.page == "edit_profile":

    st.title("✏️ Edit Patient Profile")

    user = get_user(st.session_state.user_email)

    if user:

        new_first = st.text_input("First Name", user[2])
        new_last = st.text_input("Last Name", user[3])
        new_mobile = st.text_input("Mobile Number", user[4])
        new_dob = st.date_input("Date of Birth", date.fromisoformat(user[5]))
        new_age = st.number_input("Age", 1, 120, user[6])

        gender_list = ["Male","Female","Other"]
        blood_list = ["Not specified","A+","A-","B+","B-","O+","O-","AB+","AB-"]

        new_gender = st.selectbox("Gender", gender_list,
                                  index=gender_list.index(user[7]))

        new_blood = st.selectbox("Blood Group", blood_list,
                                 index=blood_list.index(user[8]))

        st.divider()

        col1, col2 = st.columns(2)

        with col1:
            save_btn = st.button("Save Changes", use_container_width=True)

        with col2:
            back_btn = st.button("Back", use_container_width=True)

        if save_btn:
            update_user((
                new_first, new_last, new_mobile,
                str(new_dob), new_age,
                new_gender, new_blood,
                user[0]
            ))
            st.success("Profile updated successfully")
            st.session_state.page = "dashboard"
            st.rerun()

        if back_btn:
            st.session_state.page = "dashboard"
            st.rerun()

# ==========================================================
# HEART PAGE
# ==========================================================
elif st.session_state.page == "heart":

    st.title("❤️ Heart Disease Prediction")

    result_placeholder = st.empty()   # RESULT AT TOP

    heart_features = [
        st.number_input("Age", 1, 120),
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

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        predict_btn = st.button("Predict", use_container_width=True)

    with col2:
        back_btn = st.button("Back", use_container_width=True)

    if predict_btn:
        result = heart_model.predict(
            heart_scaler.transform(np.array(heart_features).reshape(1,-1))
        )[0]

        if result == 1:
            result_placeholder.error("⚠️ High Risk of Heart Disease")
        else:
            result_placeholder.success("✅ Low Risk of Heart Disease")

    if back_btn:
        st.session_state.page = "dashboard"
        st.rerun()

# ==========================================================
# DIABETES PAGE
# ==========================================================
elif st.session_state.page == "diabetes":

    st.title("🩸 Diabetes Prediction")

    result_placeholder = st.empty()   # RESULT AT TOP

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

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        predict_btn = st.button("Predict", use_container_width=True)

    with col2:
        back_btn = st.button("Back", use_container_width=True)

    if predict_btn:
        result = diabetes_model.predict(
            diabetes_scaler.transform(np.array(diabetes_features).reshape(1,-1))
        )[0]

        if result == 1:
            result_placeholder.error("⚠️ High Risk of Diabetes")
        else:
            result_placeholder.success("✅ Low Risk of Diabetes")

    if back_btn:
        st.session_state.page = "dashboard"
        st.rerun()
