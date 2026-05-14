from fastapi import FastAPI
from pydantic import BaseModel, Field
from fastapi.responses import JSONResponse
from typing import Literal, Annotated
import pandas as pd
import pickle
import json
import os
from datetime import datetime

# ── Paths (always correct regardless of where uvicorn is launched from) ──
BASE_DIR         = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR         = os.path.dirname(BASE_DIR)
MODEL_PATH       = os.path.join(ROOT_DIR, "Model", "pipe.pkl")
PREDICTIONS_FILE = os.path.join(BASE_DIR, "predictions.json")


with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

# rest of your code unchanged ...


app = FastAPI()
@app.get("/")
def root():
    return {"message": "Welcome to the Loan Approval Prediction API!"}



LOAN_STATUS_MAP = {
    1: "Approved",
    0: "Rejected"
}

class UserData(BaseModel):
    age: Annotated[int, Field(..., gt=0)]
    gender: Annotated[Literal['male', 'female'], Field(...)]
    education: Annotated[Literal['High School', 'Associate', 'Bachelor', 'Master', 'Doctorate'], Field(...)]
    person_income: Annotated[float, Field(..., gt=0)]
    employee_experience: Annotated[int, Field(..., ge=0)]
    credit_score: Annotated[int, Field(..., ge=300, le=850)]
    credit_history: Annotated[int, Field(..., gt=0)]
    loan_amount: Annotated[float, Field(..., gt=0)]
    loan_interest_rate: Annotated[float, Field(..., gt=0)]
    loan_intent: Annotated[Literal['EDUCATION', 'MEDICAL', 'VENTURE', 'PERSONAL', 'DEBTCONSOLIDATION', 'HOMEIMPROVEMENT'], Field(...)]
    home_ownership: Annotated[Literal['RENT', 'OWN', 'MORTGAGE', 'OTHER'], Field(...)]
    loan_percentage: Annotated[float, Field(..., gt=0)]
    previous_loan: Annotated[int, Field(..., ge=0, le=1)]


def load_predictions() -> list:
    if os.path.exists(PREDICTIONS_FILE):
        with open(PREDICTIONS_FILE, "r") as f:
            return json.load(f)
    return []


def save_prediction(user: UserData, prediction_label: str):
    records = load_predictions()

    record = {
        "timestamp": datetime.now().isoformat(),
        "input": {
            "age": user.age,
            "gender": user.gender,
            "education": user.education,
            "person_income": user.person_income,
            "employee_experience": user.employee_experience,
            "credit_score": user.credit_score,
            "credit_history": user.credit_history,
            "loan_amount": user.loan_amount,
            "loan_interest_rate": user.loan_interest_rate,
            "loan_intent": user.loan_intent,
            "home_ownership": user.home_ownership,
            "loan_percentage": user.loan_percentage,
            "previous_loan": user.previous_loan,
        },
        "prediction": prediction_label
    }

    records.append(record)

    with open(PREDICTIONS_FILE, "w") as f:
        json.dump(records, f, indent=4)


@app.post("/predict")
def predict(user: UserData):
    input_data = pd.DataFrame([{
        "Age": user.age,
        "Gender": user.gender,
        "Education": user.education,
        "Person Income": user.person_income,
        "Employee Experience": user.employee_experience,
        "Home Onwership": user.home_ownership,
        "Loan Amount": user.loan_amount,
        "Loan Intent": user.loan_intent,
        "Loan interest Rate": user.loan_interest_rate,
        "Loan percentage": user.loan_percentage,
        "Credit History": user.credit_history,
        "Credit Score": user.credit_score,
        "Previous Loan": user.previous_loan,
    }])

    raw_prediction = int(model.predict(input_data)[0])
    prediction_label = LOAN_STATUS_MAP[raw_prediction]   # 1 → "Approved", 0 → "Rejected"

    save_prediction(user, prediction_label)
    
    try:
        return JSONResponse(status_code=200, content={
            "prediction": raw_prediction,
            "loan_status": prediction_label
        })
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.get("/predictions")
def get_predictions():
    try:
        """Returns all saved predictions from the JSON file."""
        return JSONResponse(status_code=200, content=load_predictions())
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})