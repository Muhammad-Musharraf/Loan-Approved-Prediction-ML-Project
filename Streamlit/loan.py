import streamlit as st
import pickle
import numpy as np
import pandas as pd

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Loan Approval Predictor",
    page_icon="🏦",
    layout="centered",
)

# ── Load model ────────────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    with open("Model/pipe.pkl", "rb") as f:
        return pickle.load(f)

pipe = load_model()

# ── Styling ───────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #f8fafc; }
    .stButton > button {
        width: 100%;
        background-color: #2563eb;
        color: white;
        font-size: 18px;
        font-weight: 600;
        padding: 0.6rem 1rem;
        border-radius: 10px;
        border: none;
        margin-top: 10px;
    }
    .stButton > button:hover { background-color: #1d4ed8; }
    .result-box {
        padding: 1.5rem;
        border-radius: 14px;
        text-align: center;
        font-size: 22px;
        font-weight: 700;
        margin-top: 1.5rem;
    }
    .approved  { background-color: #dcfce7; color: #166534; border: 2px solid #86efac; }
    .rejected  { background-color: #fee2e2; color: #991b1b; border: 2px solid #fca5a5; }
    .section-title {
        font-size: 15px;
        font-weight: 600;
        color: #6b7280;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.3rem;
    }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.title("🏦 Loan Approval Predictor")
st.markdown("Fill in the applicant details below to instantly predict loan approval status.")
st.divider()

# ── Form ──────────────────────────────────────────────────────────────────────
with st.form("loan_form"):

    # ── Personal Information ──────────────────────────────────────────────────
    st.markdown('<p class="section-title">👤 Personal Information</p>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        age = st.number_input("Age", min_value=18, max_value=100, value=30, step=1)
    with col2:
        gender = st.selectbox("Gender", ["male", "female"])
    with col3:
        education = st.selectbox(
            "Education Level",
            ["High School", "Associate", "Bachelor", "Master", "Doctorate"]
        )

    col4, col5 = st.columns(2)
    with col4:
        person_income = st.number_input(
            "Annual Income ($)", min_value=0, max_value=10_000_000,
            value=60_000, step=1_000
        )
    with col5:
        emp_exp = st.number_input(
            "Employment Experience (yrs)", min_value=0, max_value=60, value=5, step=1
        )

    home_ownership = st.selectbox(
        "Home Ownership", ["RENT", "OWN", "MORTGAGE", "OTHER"]
    )

    st.divider()

    # ── Loan Details ──────────────────────────────────────────────────────────
    st.markdown('<p class="section-title">💰 Loan Details</p>', unsafe_allow_html=True)
    col6, col7 = st.columns(2)
    with col6:
        loan_amount = st.number_input(
            "Loan Amount ($)", min_value=500, max_value=500_000,
            value=10_000, step=500
        )
    with col7:
        loan_intent = st.selectbox(
            "Loan Intent",
            ["PERSONAL", "EDUCATION", "MEDICAL", "VENTURE", "HOMEIMPROVEMENT", "DEBTCONSOLIDATION"]
        )

    col8, col9 = st.columns(2)
    with col8:
        loan_int_rate = st.number_input(
            "Interest Rate (%)", min_value=1.0, max_value=30.0,
            value=10.0, step=0.01, format="%.2f"
        )
    with col9:
        loan_pct_income = st.number_input(
            "Loan % of Income (0–1)", min_value=0.0, max_value=1.0,
            value=0.20, step=0.01, format="%.2f"
        )

    st.divider()

    # ── Credit Information ────────────────────────────────────────────────────
    st.markdown('<p class="section-title">📊 Credit Information</p>', unsafe_allow_html=True)
    col10, col11, col12 = st.columns(3)
    with col10:
        credit_history = st.number_input(
            "Credit History (yrs)", min_value=0, max_value=30, value=5, step=1
        )
    with col11:
        credit_score = st.number_input(
            "Credit Score", min_value=300, max_value=850, value=650, step=1
        )
    with col12:
        previous_loan = st.selectbox("Previous Loan Default?", ["No", "Yes"])

    st.divider()
    submitted = st.form_submit_button("🔍 Predict Loan Approval")

# ── Prediction ────────────────────────────────────────────────────────────────
if submitted:
    prev_loan_val = 1 if previous_loan == "Yes" else 0

    input_df = pd.DataFrame(
        columns=[
            'Age', 'Gender', 'Education', 'Person Income',
            'Employee Experience', 'Home Onwership', 'Loan Amount',
            'Loan Intent', 'Loan interest Rate', 'Loan percentage',
            'Credit History', 'Credit Score', 'Previous Loan'
        ],
        data=np.array([
            age, gender, education, person_income,
            emp_exp, home_ownership, loan_amount,
            loan_intent, loan_int_rate, loan_pct_income,
            credit_history, credit_score, prev_loan_val
        ]).reshape(1, 13)
    )

    # Cast numeric columns back to proper dtypes
    numeric_cols = [
        'Age', 'Person Income', 'Employee Experience', 'Loan Amount',
        'Loan interest Rate', 'Loan percentage', 'Credit History',
        'Credit Score', 'Previous Loan'
    ]
    for c in numeric_cols:
        input_df[c] = pd.to_numeric(input_df[c])

    prediction = pipe.predict(input_df)[0]
    proba = pipe.predict_proba(input_df)[0]

    if prediction == 1:
        st.markdown(
            '<div class="result-box approved">✅ Loan Approved'
            f'<br><span style="font-size:16px;font-weight:500;">'
            f'Confidence: {proba[1]*100:.1f}%</span></div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            '<div class="result-box rejected">❌ Loan Rejected'
            f'<br><span style="font-size:16px;font-weight:500;">'
            f'Confidence: {proba[0]*100:.1f}%</span></div>',
            unsafe_allow_html=True
        )

    # Probability bar
    st.markdown("#### Approval Probability")
    prob_df = pd.DataFrame(
        {"Status": ["Rejected", "Approved"], "Probability": [proba[0], proba[1]]}
    )
    st.bar_chart(prob_df.set_index("Status"), color=["#ef4444"] if prediction == 0 else ["#22c55e"])

    # Input summary
    with st.expander("📋 Input Summary"):
        summary = {
            "Age": age, "Gender": gender, "Education": education,
            "Annual Income": f"${person_income:,}", "Employment Exp (yrs)": emp_exp,
            "Home Ownership": home_ownership, "Loan Amount": f"${loan_amount:,}",
            "Loan Intent": loan_intent, "Interest Rate": f"{loan_int_rate}%",
            "Loan % of Income": loan_pct_income, "Credit History (yrs)": credit_history,
            "Credit Score": credit_score, "Previous Default": previous_loan,
        }
        st.table(pd.DataFrame(summary.items(), columns=["Field", "Value"]))

st.divider()
st.caption("Powered by RandomForestClassifier · scikit-learn pipeline")