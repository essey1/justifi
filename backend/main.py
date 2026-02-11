from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# -------------------------
# App setup
# -------------------------

app = FastAPI(title="Justifi", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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


# -------------------------
# Financial Calculation Engine
# -------------------------

def calculate_disposable_income(income: float, expenses: float) -> float:
    return income - expenses


def calculate_monthly_payment(
    amount: float,
    term_months: int,
    interest_rate: float
) -> float:
    r = interest_rate / 12 / 100
    return amount * (r * (1 + r) ** term_months) / ((1 + r) ** term_months - 1)


# -------------------------
# Decision Logic
# -------------------------

def evaluate_affordability(input: FinancialInput) -> dict:
    disposable_income = calculate_disposable_income(
        input.income,
        input.expenses
    )

    if disposable_income <= 0:
        return {
            "status": "Not Affordable",
            "details": "Your expenses are equal to or exceed your income."
        }

    monthly_payment = calculate_monthly_payment(
        input.loan_amount,
        input.loan_term_months,
        input.interest_rate
    )

    burden_ratio = monthly_payment / disposable_income

    if burden_ratio < 0.30:
        status = "Affordable"
    elif burden_ratio < 0.50:
        status = "Risky"
    else:
        status = "Not Affordable"

    details = (
        f"Monthly payment: ${monthly_payment:.2f}. "
        f"Disposable income: ${disposable_income:.2f}. "
        f"Burden ratio: {burden_ratio:.2f}."
    )

    return {
        "status": status,
        "details": details
    }


# -------------------------
# API Endpoints
# -------------------------

@app.post("/evaluate", response_model=Verdict)
def evaluate(financial_input: FinancialInput):
    return evaluate_affordability(financial_input)


@app.get("/")
def root():
    return {"message": "Justifi backend running"}
