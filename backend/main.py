from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

import os
from groq import Groq


# -------------------------
# App setup
# -------------------------

app = FastAPI(title="Justifi", version="0.1.0")
client = Groq(api_key=os.getenv("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"))

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
# Generate AI Recommendations
# -------------------------

def generate_ai_recommendations(
    input: FinancialInput,
    monthly_payment: float,
    disposable_income: float,
    burden_ratio: float,
    status: str
) -> str:

    prompt = f"""
    A user has:
    Monthly income: ${input.income}
    Monthly expenses: ${input.expenses}
    Loan amount: ${input.loan_amount}
    Loan term: {input.loan_term_months} months
    Interest rate: {input.interest_rate}%

    Monthly payment: ${monthly_payment:.2f}
    Disposable income: ${disposable_income:.2f}
    Burden ratio: {burden_ratio:.2f}
    Status: {status}

    Provide practical financial recommendations.

    Only suggest:
    - Lowering loan amount
    - Extending term
    - Cutting expenses
    - Delaying purchase
    - Cheaper alternatives

    Keep it short.
    Be direct.
    Avoid emotional tone.
    """

    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "user", "content": prompt}
        ],
        model="llama3-8b-8192",
        temperature=0.3,
    )

    return chat_completion.choices[0].message.content



# -------------------------
# Decision Logic
# -------------------------

def evaluate_affordability(input: FinancialInput) -> dict:
    disposable_income = calculate_disposable_income(
        input.income,
        input.expenses
    )

    # Handle zero or negative disposable income
    if disposable_income <= 0:
        status = "Not Affordable"
        monthly_payment = 0
        burden_ratio = 1
    else:
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

    # Default details (used for Affordable cases)
    details = (
        f"Monthly payment: ${monthly_payment:.2f}. "
        f"Disposable income: ${disposable_income:.2f}. "
        f"Burden ratio: {burden_ratio:.2f}."
    )

    # Only trigger AI for risky cases
    if status in ["Risky", "Not Affordable"]:
        ai_details = generate_ai_recommendations(
            input,
            monthly_payment,
            disposable_income,
            burden_ratio,
            status
        )
        details = ai_details

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
