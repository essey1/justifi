from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# -------------------------
# App setup
# -------------------------

app = FastAPI(title="Justifi", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# Data Models
# -------------------------

class FinancialInput(BaseModel):
    income: float
    expenses: float
    loan_amount: float
    loan_term_months: int
    interest_rate: float


class Verdict(BaseModel):
    status: str  # "Affordable", "Risky", "Not Affordable"
    details: str


