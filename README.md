# Justifi

## System Design

This application is a **financial decision engine** that evaluates whether a loan or large purchase is affordable based on a user’s income and expenses. When a purchase is risky or unaffordable, the system provides **AI-generated alternatives** aligned with the user’s budget and intent.

### Architecture

```
React + TypeScript (Frontend)
        |
        v
FastAPI (Backend)
        |
        ├── Financial Calculation Engine
        ├── Decision Logic Engine
        └── AI Recommendation Service
```


### Frontend
- Built with React and TypeScript  
- Collects financial inputs and purchase details  
- Displays affordability verdicts with clear explanations  
- Shows AI-driven alternatives when applicable  

### Backend
- Built with FastAPI  
- Performs deterministic financial calculations  
- Applies rule-based affordability decisions  
- Integrates with an LLM to generate realistic alternatives  

### Financial Evaluation
- Calculates disposable income and monthly cost  
- Uses burden ratios to assess affordability  
- Produces a clear verdict: **Affordable**, **Risky**, or **Not Affordable**  
- Explains each decision  

### AI Recommendations
- Triggered only when a purchase is risky or unaffordable  
- Suggests practical, budget-conscious alternatives  
- Focuses on realistic substitutions, delays, or cost reductions

## Next Steps

### User Account System
- Implement secure user accounts with authentication.
- Allow users to store income, fixed expenses, debts, and preferences once.
- Enable instant affordability checks for new purchases without reentering financial data each time.
- Support profile updates to reflect changing financial situations.

### Saved Scenarios and Purchase History
- Let users save past affordability evaluations.
- Compare multiple purchase options side by side.
- Track how affordability changes over time as income or expenses change.

### Budget Planning Tools
- Provide monthly budget breakdowns with clear visual summaries.
- Alert users when a proposed purchase exceeds safe spending thresholds.
- Support adjustable financial goals such as savings or debt reduction targets.

