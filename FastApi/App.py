from fastapi import FastAPI
from pydantic import BaseModel, Field
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Literal, Annotated
import pandas as pd
import pickle
import os
from datetime import datetime

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR   = os.path.dirname(BASE_DIR)
MODEL_PATH = os.path.join(ROOT_DIR, "Model", "pipe.pkl")

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

app = FastAPI()



LOAN_STATUS_MAP = {1: "Approved", 0: "Rejected"}


# ── Schema ────────────────────────────────────────────────────────────────────
class UserData(BaseModel):
    age:                 Annotated[int,   Field(..., gt=0)]
    gender:              Annotated[Literal["male", "female"], Field(...)]
    education:           Annotated[Literal["High School", "Associate", "Bachelor", "Master", "Doctorate"], Field(...)]
    person_income:       Annotated[float, Field(..., gt=0)]
    employee_experience: Annotated[int,   Field(..., ge=0)]
    credit_score:        Annotated[int,   Field(..., ge=300, le=850)]
    credit_history:      Annotated[int,   Field(..., gt=0)]
    loan_amount:         Annotated[float, Field(..., gt=0)]
    loan_interest_rate:  Annotated[float, Field(..., gt=0)]
    loan_intent:         Annotated[Literal["EDUCATION", "MEDICAL", "VENTURE", "PERSONAL", "DEBTCONSOLIDATION", "HOMEIMPROVEMENT"], Field(...)]
    home_ownership:      Annotated[Literal["RENT", "OWN", "MORTGAGE", "OTHER"], Field(...)]
    loan_percentage:     Annotated[float, Field(..., gt=0)]
    previous_loan:       Annotated[int,   Field(..., ge=0, le=1)]


# ── Routes ────────────────────────────────────────────────────────────────────
# Human readable root endpoint
@app.get("/")
def root():
    return {"message": "Loan Approval Prediction API"}

# Machine readable health check endpoint
@app.get("/health")
def health():
    return {
        "status": "OK",
        "timestamp": datetime.now().isoformat(),
        "Model Loaded": model is not None

    }


@app.post("/predict")
def predict(user: UserData):
    input_df = pd.DataFrame([{
        "Age":                 user.age,
        "Gender":              user.gender,
        "Education":           user.education,
        "Person Income":       user.person_income,
        "Employee Experience": user.employee_experience,
        "Home Onwership":      user.home_ownership,   # typo kept — must match trained model columns
        "Loan Amount":         user.loan_amount,
        "Loan Intent":         user.loan_intent,
        "Loan interest Rate":  user.loan_interest_rate,
        "Loan percentage":     user.loan_percentage,
        "Credit History":      user.credit_history,
        "Credit Score":        user.credit_score,
        "Previous Loan":       user.previous_loan,
    }])

    try:
        raw   = int(model.predict(input_df)[0])
        label = LOAN_STATUS_MAP[raw]
        return JSONResponse(status_code=200, content={"loan_status": label})

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


