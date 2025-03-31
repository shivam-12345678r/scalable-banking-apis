from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Define dispute input model
class Dispute(BaseModel):
    customer_id: str
    transaction_id: str
    dispute_reason: str
    dispute_description: str
    transaction_amount: float
    customer_history_score: int  # (0-10, 10 = trusted customer, 0 = high-risk)

# AI-based rule system for dispute classification
def classify_dispute(reason: str):
    categories = {
        "fraud": "Fraudulent Transaction",
        "duplicate": "Duplicate Charge",
        "unauthorized": "Unauthorized Access",
        "service": "Service Not Provided"
    }
    for keyword, category in categories.items():
        if keyword in reason.lower():
            return category
    return "Other"

# Assign priority based on history and amount
def assign_priority(amount: float, history_score: int):
    if amount > 5000 or history_score < 3:
        return "High"
    elif amount > 1000 or history_score < 7:
        return "Medium"
    else:
        return "Low"

# Recommend action based on classification and priority
def recommend_action(category: str, priority: str):
    if priority == "High":
        return f"Escalate to Fraud Investigation for {category}"
    elif priority == "Medium":
        return f"Manual review needed for {category}"
    return f"Auto-resolve: {category}"

@app.post("/process_dispute")
def process_dispute(dispute: Dispute):
    category = classify_dispute(dispute.dispute_reason)
    priority = assign_priority(dispute.transaction_amount, dispute.customer_history_score)
    action = recommend_action(category, priority)
    
    return {
        "transaction_id": dispute.transaction_id,
        "category": category,
        "priority": priority,
        "recommended_action": action
    }
