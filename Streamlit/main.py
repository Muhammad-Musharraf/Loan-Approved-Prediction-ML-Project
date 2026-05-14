import streamlit as st
import requests
import json
from datetime import datetime

API_URL = "http://127.0.0.1:8000"  # Make sure this matches your FastAPI endpoint

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="LoanSense AI",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="collapsed"
    )

# ─── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #0a0a0f;
    color: #e8e4dc;
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stAppViewContainer"] {
    background: radial-gradient(ellipse at 20% 50%, #1a0a2e 0%, #0a0a0f 60%),
                radial-gradient(ellipse at 80% 20%, #0d1a2e 0%, transparent 50%);
    min-height: 100vh;
}

[data-testid="stHeader"] { background: transparent; }
[data-testid="stToolbar"] { display: none; }
.block-container { padding: 2rem 3rem 4rem; max-width: 1300px; }

/* ── Hero Header ── */
.hero {
    text-align: center;
    padding: 3.5rem 0 2.5rem;
    position: relative;
}
.hero::before {
    content: '';
    position: absolute;
    top: 0; left: 50%;
    transform: translateX(-50%);
    width: 600px; height: 300px;
    background: radial-gradient(ellipse, rgba(120,80,255,0.15) 0%, transparent 70%);
    pointer-events: none;
}
.hero-badge {
    display: inline-block;
    background: rgba(120,80,255,0.15);
    border: 1px solid rgba(120,80,255,0.4);
    color: #a78bfa;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    padding: 0.35rem 1rem;
    border-radius: 100px;
    margin-bottom: 1.2rem;
}
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: clamp(2.8rem, 5vw, 4.2rem);
    font-weight: 900;
    line-height: 1.1;
    color: #f0ece4;
    margin-bottom: 0.8rem;
    letter-spacing: -0.02em;
}
.hero-title span {
    background: linear-gradient(135deg, #a78bfa 0%, #60a5fa 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-sub {
    color: #6b7280;
    font-size: 1.05rem;
    font-weight: 300;
    max-width: 520px;
    margin: 0 auto;
    line-height: 1.6;
}

/* ── Section Label ── */
.section-label {
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #a78bfa;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.6rem;
}
.section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(to right, rgba(167,139,250,0.3), transparent);
}

/* ── Card ── */
.card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 20px;
    padding: 2rem;
    margin-bottom: 1.2rem;
    backdrop-filter: blur(10px);
    transition: border-color 0.3s;
}
.card:hover { border-color: rgba(167,139,250,0.2); }

/* ── Streamlit widget overrides ── */
[data-testid="stSelectbox"] > div > div,
[data-testid="stNumberInput"] > div > div > input,
[data-testid="stSlider"] {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
    color: #e8e4dc !important;
}

label, .stSelectbox label, .stNumberInput label, .stSlider label {
    color: #9ca3af !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.03em !important;
}

/* ── Submit Button ── */
.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #7c3aed 0%, #2563eb 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 1rem 2rem !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.04em !important;
    cursor: pointer !important;
    transition: all 0.3s !important;
    box-shadow: 0 8px 32px rgba(124,58,237,0.35) !important;
    margin-top: 0.5rem;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 14px 40px rgba(124,58,237,0.5) !important;
}

/* ── Result Cards ── */
.result-approved {
    background: linear-gradient(135deg, rgba(16,185,129,0.12) 0%, rgba(5,150,105,0.06) 100%);
    border: 1px solid rgba(16,185,129,0.35);
    border-radius: 20px;
    padding: 2.5rem;
    text-align: center;
    animation: fadeSlideIn 0.5s ease;
}
.result-rejected {
    background: linear-gradient(135deg, rgba(239,68,68,0.12) 0%, rgba(185,28,28,0.06) 100%);
    border: 1px solid rgba(239,68,68,0.35);
    border-radius: 20px;
    padding: 2.5rem;
    text-align: center;
    animation: fadeSlideIn 0.5s ease;
}
.result-icon { font-size: 3.5rem; margin-bottom: 0.8rem; }
.result-status {
    font-family: 'Playfair Display', serif;
    font-size: 2.2rem;
    font-weight: 700;
    margin-bottom: 0.4rem;
}
.result-approved .result-status { color: #34d399; }
.result-rejected .result-status { color: #f87171; }
.result-desc { color: #9ca3af; font-size: 0.92rem; }

/* ── History Table ── */
.history-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.2rem;
}
.history-count {
    background: rgba(167,139,250,0.15);
    color: #a78bfa;
    font-size: 0.78rem;
    font-weight: 600;
    padding: 0.25rem 0.75rem;
    border-radius: 100px;
}
.history-item {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 14px;
    padding: 1rem 1.4rem;
    margin-bottom: 0.6rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    transition: background 0.2s;
}
.history-item:hover { background: rgba(255,255,255,0.045); }
.history-meta { color: #6b7280; font-size: 0.78rem; margin-top: 0.15rem; }
.badge-approved {
    background: rgba(16,185,129,0.15);
    color: #34d399;
    border: 1px solid rgba(16,185,129,0.3);
    padding: 0.25rem 0.85rem;
    border-radius: 100px;
    font-size: 0.8rem;
    font-weight: 600;
}
.badge-rejected {
    background: rgba(239,68,68,0.15);
    color: #f87171;
    border: 1px solid rgba(239,68,68,0.3);
    padding: 0.25rem 0.85rem;
    border-radius: 100px;
    font-size: 0.8rem;
    font-weight: 600;
}

/* ── Stats bar ── */
.stats-row {
    display: flex;
    gap: 1rem;
    margin-bottom: 2rem;
}
.stat-pill {
    flex: 1;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 1.2rem 1.4rem;
    text-align: center;
}
.stat-number {
    font-family: 'Playfair Display', serif;
    font-size: 1.8rem;
    font-weight: 700;
    color: #f0ece4;
}
.stat-label { color: #6b7280; font-size: 0.78rem; margin-top: 0.15rem; }

@keyframes fadeSlideIn {
    from { opacity: 0; transform: translateY(16px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* ── Divider ── */
hr { border: none; border-top: 1px solid rgba(255,255,255,0.06); margin: 2rem 0; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(167,139,250,0.3); border-radius: 3px; }
</style>
""", unsafe_allow_html=True)


# ─── Hero ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">✦ AI-Powered Decision Engine</div>
    <h1 class="hero-title">Loan<span>Sense</span> AI</h1>
    <p class="hero-sub">Intelligent loan approval predictions powered by machine learning — fast, accurate, and explainable.</p>
</div>
""", unsafe_allow_html=True)


# ─── Fetch history for stats ─────────────────────────────────────────────────
def fetch_history():
    try:
        r = requests.get(f"{API_URL}/predictions", timeout=4)
        return r.json() if r.status_code == 200 else []
    except:
        return []

history = fetch_history()
total   = len(history)
approved = sum(1 for h in history if h.get("prediction") == "Approved")
rejected = total - approved

# ── Stats Pills ──
st.markdown(f"""
<div class="stats-row">
    <div class="stat-pill">
        <div class="stat-number">{total}</div>
        <div class="stat-label">Total Predictions</div>
    </div>
    <div class="stat-pill">
        <div class="stat-number" style="color:#34d399">{approved}</div>
        <div class="stat-label">Approved</div>
    </div>
    <div class="stat-pill">
        <div class="stat-number" style="color:#f87171">{rejected}</div>
        <div class="stat-label">Rejected</div>
    </div>
    <div class="stat-pill">
        <div class="stat-number" style="color:#a78bfa">{f"{(approved/total*100):.0f}%" if total else "—"}</div>
        <div class="stat-label">Approval Rate</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ─── Layout ──────────────────────────────────────────────────────────────────
left, right = st.columns([1.05, 0.95], gap="large")

with left:
    st.markdown('<div class="section-label">Application Form</div>', unsafe_allow_html=True)

    with st.form("loan_form"):

        # Personal Info
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("**👤 Personal Information**")
        c1, c2 = st.columns(2)
        age    = c1.number_input("Age", min_value=18, max_value=100, value=28, step=1)
        gender = c2.selectbox("Gender", ["male", "female"])
        education = st.selectbox("Education Level", ["High School", "Associate", "Bachelor", "Master", "Doctorate"])
        c3, c4 = st.columns(2)
        person_income = c3.number_input("Annual Income ($)", min_value=1000.0, value=55000.0, step=500.0)
        employee_exp  = c4.number_input("Years of Experience", min_value=0, max_value=60, value=4, step=1)
        st.markdown('</div>', unsafe_allow_html=True)

        # Credit Info
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("**📊 Credit Profile**")
        c5, c6 = st.columns(2)
        credit_score   = c5.slider("Credit Score", min_value=300, max_value=850, value=650)
        credit_history = c6.number_input("Credit History (years)", min_value=1, max_value=40, value=5, step=1)
        previous_loan  = st.selectbox("Previous Loan Default?", [0, 1], format_func=lambda x: "No Default (0)" if x == 0 else "Has Default (1)")
        st.markdown('</div>', unsafe_allow_html=True)

        # Loan Details
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("**💰 Loan Details**")
        c7, c8 = st.columns(2)
        loan_amount       = c7.number_input("Loan Amount ($)", min_value=100.0, max_value=35000.0, value=8000.0, step=100.0)
        loan_interest_rate = c8.number_input("Interest Rate (%)", min_value=1.0, max_value=25.0, value=11.0, step=0.1)
        c9, c10 = st.columns(2)
        loan_percentage = c9.number_input("Loan % of Income", min_value=0.01, max_value=1.0, value=round(8000/55000, 2), step=0.01, format="%.2f")
        loan_intent     = c10.selectbox("Loan Purpose", ["EDUCATION", "MEDICAL", "VENTURE", "PERSONAL", "DEBTCONSOLIDATION", "HOMEIMPROVEMENT"])
        home_ownership  = st.selectbox("Home Ownership", ["RENT", "OWN", "MORTGAGE", "OTHER"])
        st.markdown('</div>', unsafe_allow_html=True)

        submitted = st.form_submit_button("⚡  Analyse & Predict")

    # ── Result ──
    if submitted:
        payload = {
            "age": age,
            "gender": gender,
            "education": education,
            "person_income": person_income,
            "employee_experience": employee_exp,
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
            with st.spinner("Running model inference…"):
                resp = requests.post(f"{API_URL}/predict", json=payload, timeout=8)

            if resp.status_code == 200:
                data   = resp.json()
                status = data.get("loan_status", "Unknown")
                is_app = status == "Approved"

                if is_app:
                    st.markdown(f"""
                    <div class="result-approved">
                        <div class="result-icon">✅</div>
                        <div class="result-status">Loan Approved</div>
                        <div class="result-desc">Congratulations! This application meets the approval criteria.</div>
                    </div>""", unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="result-rejected">
                        <div class="result-icon">❌</div>
                        <div class="result-status">Loan Rejected</div>
                        <div class="result-desc">This application does not meet the current approval criteria.</div>
                    </div>""", unsafe_allow_html=True)

                with st.expander("📦 Raw API Response"):
                    st.json(data)

            else:
                st.error(f"API Error {resp.status_code}: {resp.text}")

        except requests.exceptions.ConnectionError:
            st.error("🔌 Cannot reach the API. Make sure uvicorn is running on port 8000.")
        except Exception as e:
            st.error(f"Unexpected error: {e}")


# ─── Right Column — History ───────────────────────────────────────────────────
with right:
    st.markdown('<div class="section-label">Prediction History</div>', unsafe_allow_html=True)

    col_r1, col_r2 = st.columns([3, 1])
    with col_r2:
        if st.button("🔄 Refresh"):
            st.rerun()

    if not history:
        st.markdown("""
        <div class="card" style="text-align:center; padding:3rem 2rem; color:#4b5563;">
            <div style="font-size:2.5rem; margin-bottom:0.8rem;">📭</div>
            <div style="font-size:0.95rem;">No predictions yet.<br>Submit a form to get started.</div>
        </div>""", unsafe_allow_html=True)
    else:
        for item in reversed(history[-30:]):        # show latest 30
            ts  = item.get("timestamp", "")
            inp = item.get("input", {})
            pred = item.get("prediction", "")
            badge = f'<span class="badge-approved">✓ Approved</span>' if pred == "Approved" \
                    else f'<span class="badge-rejected">✗ Rejected</span>'

            try:
                dt = datetime.fromisoformat(ts).strftime("%b %d, %Y  %H:%M")
            except:
                dt = ts

            income = inp.get("person_income", "—")
            loan   = inp.get("loan_amount", "—")
            score  = inp.get("credit_score", "—")

            st.markdown(f"""
            <div class="history-item">
                <div>
                    <div style="font-size:0.88rem; font-weight:500; color:#d1d5db;">
                        ${loan:,.0f} loan · Score {score}
                    </div>
                    <div class="history-meta">{dt} &nbsp;·&nbsp; Income ${income:,.0f}</div>
                </div>
                {badge}
            </div>""", unsafe_allow_html=True)

    # ── JSON download ──
    if history:
        st.markdown("<hr>", unsafe_allow_html=True)
        st.download_button(
            label="⬇  Download predictions.json",
            data=json.dumps(history, indent=4),
            file_name="predictions.json",
            mime="application/json",
            use_container_width=True
        )