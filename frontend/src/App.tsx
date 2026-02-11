import { useState } from "react";
import axios from "axios";
import "./App.css";

const API_URL = "https://justifi-qf3b.onrender.com";


type FinancialInput = {
  income: number;
  expenses: number;
  loan_amount: number;
  loan_term_months: number;
  interest_rate: number;
};

type Verdict = {
  status: string;
  details: string;
};

function App() {
  const [form, setForm] = useState<FinancialInput>({
    income: 0,
    expenses: 0,
    loan_amount: 0,
    loan_term_months: 0,
    interest_rate: 0,
  });

  const [result, setResult] = useState<Verdict | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({
      ...form,
      [e.target.name]: Number(e.target.value),
    });
  };

  const handleSubmit = async () => {
    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await axios.post<Verdict>(
        `${API_URL}/evaluate`,
        form
      );
      setResult(response.data);
    } catch (err) {
      setError("Failed to evaluate affordability.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "2rem", maxWidth: "500px", margin: "0 auto" }}>
      <h1>Justifi</h1>
      <p>Check if a loan or purchase fits your budget.</p>

      <label>
        Monthly Income
        <input name="income" type="number" onChange={handleChange} />
      </label>

      <label>
        Monthly Expenses
        <input name="expenses" type="number" onChange={handleChange} />
      </label>

      <label>
        Loan Amount
        <input name="loan_amount" type="number" onChange={handleChange} />
      </label>

      <label>
        Loan Term (months)
        <input name="loan_term_months" type="number" onChange={handleChange} />
      </label>

      <label>
        Interest Rate (%)
        <input name="interest_rate" type="number" onChange={handleChange} />
      </label>

      <button onClick={handleSubmit} disabled={loading}>
        {loading ? "Evaluating..." : "Evaluate"}
      </button>

      {error && <p style={{ color: "red" }}>{error}</p>}

      {result && (
        <div style={{ marginTop: "1rem" }}>
          <h3>{result.status}</h3>
          <p>{result.details}</p>
        </div>
      )}
    </div>
  );
}

export default App;
