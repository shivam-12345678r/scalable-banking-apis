from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from threading import Lock

app = FastAPI()

# Simulated in-memory database
accounts = {
    "123": {"balance": 5000.0},
    "456": {"balance": 3000.0}
}
account_locks = {"123": Lock(), "456": Lock()}  # Prevent race conditions

# Transaction model
class Transaction(BaseModel):
    account_id: str
    amount: float

@app.get("/balance/{account_id}")
def get_balance(account_id: str):
    if account_id not in accounts:
        raise HTTPException(status_code=404, detail="Account not found")
    return {"account_id": account_id, "balance": accounts[account_id]["balance"]}

@app.post("/credit")
def credit(transaction: Transaction):
    if transaction.account_id not in accounts:
        raise HTTPException(status_code=404, detail="Account not found")
    
    with account_locks[transaction.account_id]:
        accounts[transaction.account_id]["balance"] += transaction.amount
    return {"account_id": transaction.account_id, "new_balance": accounts[transaction.account_id]["balance"]}

@app.post("/debit")
def debit(transaction: Transaction):
    if transaction.account_id not in accounts:
        raise HTTPException(status_code=404, detail="Account not found")
    
    with account_locks[transaction.account_id]:
        if accounts[transaction.account_id]["balance"] < transaction.amount:
            raise HTTPException(status_code=400, detail="Insufficient balance")
        
        accounts[transaction.account_id]["balance"] -= transaction.amount
    return {"account_id": transaction.account_id, "new_balance": accounts[transaction.account_id]["balance"]}
