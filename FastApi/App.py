from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Literal, Annotated
from mangum import Mangum
import pandas as pd
import pickle
import os

# ── Model Loading ──────────────────────────────────────────────────────────────
# In Lambda, your model file must be bundled in the deployment package or
# fetched from S3. Set MODEL_PATH via an environment variable for flexibility.
#
# Option A (bundled): place pipe.pkl alongside handler.py in the zip/layer.
# Option B (S3):      download to /tmp on cold start (see _load_model below).

MODEL_PATH = os.environ.get("MODEL_PATH", os.path.join(os.path.dirname(__file__), "pipe.pkl"))

def _load_model():
    """Load model from local path or S3 (cached in /tmp across warm invocations)."""
    local = "/tmp/pipe.pkl"

    # ── S3 path (uncomment + set MODEL_S3_URI env var if using S3) ────────────
    # import boto3, urllib.parse
    # s3_uri = os.environ.get("MODEL_S3_URI")   # e.g. s3://my-bucket/models/pipe.pkl
    # if s3_uri and not os.path.exists(local):
    #     parsed = urllib.parse.urlparse(s3_uri)
    #     boto3.client("s3").download_file(parsed.netloc, parsed.path.lstrip("/"), local)
    #     path = local
    # else:
    #     path = MODEL_PATH if os.path.exists(MODEL_PATH) else local

    path = MODEL_PATH
    with open(path, "rb") as f:
        return pickle.load(f)

# Module-level: loaded once per container (warm Lambda reuse)
model = _load_model()

LOAN_STATUS_MAP = {1: "Approved", 0: "Rejected"}

# ── App ────────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="LoanSense AI",
    description="Serverless loan approval prediction API",
    version="1.0.0",
)


# ── Schema ─────────────────────────────────────────────────────────────────────
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


# ── Routes ─────────────────────────────────────────────────────────────────────
@app.get("/")
def root():
    return {"message": "LoanSense AI API is running."}


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


# ── Serverless handler ─────────────────────────────────────────────────────────
# Mangum wraps the ASGI app and is called by AWS Lambda as the entry point.
# Set your Lambda handler to:  handler.lambda_handler
handler = Mangum(app, lifespan="off")


