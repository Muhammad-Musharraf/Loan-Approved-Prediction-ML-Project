import streamlit as st
import requests

# ─────────────────────────────────────────────
# Page Config
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="LoanSense AI",
    page_icon="💰",
    layout="centered"
)

# ─────────────────────────────────────────────
# FastAPI URL
# ─────────────────────────────────────────────
# Local API
API_URL = "http://127.0.0.1:8000/predict"

# Deployment Example:
# API_URL = "https://your-fastapi-api.onrender.com/predict"

# ─────────────────────────────────────────────
# Title
# ─────────────────────────────────────────────
st.title("💰 LoanSense AI")
st.markdown("### Loan Approval Prediction System")

st.divider()

# ─────────────────────────────────────────────
# Form
# ─────────────────────────────────────────────
with st.form("loan_form"):

    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input(
            "Age",
            min_value=18,
            max_value=100,
            value=25
        )

        gender = st.selectbox(
            "Gender",
            ["male", "female"]
        )

        education = st.selectbox(
            "Education",
            [
                "High School",
                "Associate",
                "Bachelor",
                "Master",
                "Doctorate"
            ]
        )

        person_income = st.number_input(
            "Person Income",
            min_value=0.0,
            value=50000.0
        )

        employee_experience = st.number_input(
            "Employee Experience",
            min_value=0,
            value=2
        )

        credit_score = st.slider(
            "Credit Score",
            min_value=300,
            max_value=850,
            value=650
        )

    with col2:
        credit_history = st.number_input(
            "Credit History",
            min_value=1,
            value=5
        )

        loan_amount = st.number_input(
            "Loan Amount",
            min_value=1000.0,
            value=10000.0
        )

        loan_interest_rate = st.number_input(
            "Loan Interest Rate",
            min_value=0.0,
            value=8.5
        )

        loan_intent = st.selectbox(
            "Loan Intent",
            [
                "EDUCATION",
                "MEDICAL",
                "VENTURE",
                "PERSONAL",
                "DEBTCONSOLIDATION",
                "HOMEIMPROVEMENT"
            ]
        )

        home_ownership = st.selectbox(
            "Home Ownership",
            ["RENT", "OWN", "MORTGAGE", "OTHER"]
        )

        loan_percentage = st.number_input(
            "Loan Percentage",
            min_value=0.0,
            value=20.0
        )

        previous_loan = st.selectbox(
            "Previous Loan",
            [0, 1]
        )

    submit = st.form_submit_button("Predict Loan Status")

# ─────────────────────────────────────────────
# Prediction
# ─────────────────────────────────────────────
if submit:

    payload = {
        "age": age,
        "gender": gender,
        "education": education,
        "person_income": person_income,
        "employee_experience": employee_experience,
        "credit_score": credit_score,
        "credit_history": credit_history,
        "loan_amount": loan_amount,
        "loan_interest_rate": loan_interest_rate,
        "loan_intent": loan_intent,
        "home_ownership": home_ownership,
        "loan_percentage": loan_percentage,
        "previous_loan": previous_loan
    }

    try:
        response = requests.post(API_URL, json=payload)

        if response.status_code == 200:

            result = response.json()

            prediction = result["loan_status"]

            st.divider()

            if prediction == "Approved":
                st.success(f"✅ Loan Status: {prediction}")

            else:
                st.error(f"❌ Loan Status: {prediction}")

        else:
            st.error(f"API Error: {response.text}")

    except Exception as e:
        st.error(f"Connection Error: {e}")
