from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Define loan application input model
class LoanApplication(BaseModel):
    customer_id: str
    income: float
    credit_score: int
    existing_loans: float
    debt_to_income_ratio: float

# AI-based rule system for loan eligibility
def calculate_loan_score(credit_score, income, existing_loans, dti):
    if credit_score > 750 and dti < 0.3:
        return 90, "Highly Eligible"
    elif credit_score > 600 and dti < 0.5:
        return 60, "Moderately Eligible"
    else:
        return 30, "Not Eligible"

@app.post("/check_loan_eligibility")
def check_loan_eligibility(application: LoanApplication):
    score, recommendation = calculate_loan_score(
        application.credit_score, application.income, application.existing_loans, application.debt_to_income_ratio
    )
    
    return {
        "customer_id": application.customer_id,
        "loan_eligibility_score": score,
        "recommendation": recommendation
    }
