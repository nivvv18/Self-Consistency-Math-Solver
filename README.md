# Self-Consistency Math Solver (GenAI Mini Project)

## Project 16 — Generative AI with Large Language Models

### Problem statement
Solve mathematical word problems using multiple independent LLM attempts and select the most consistent final answer using self-consistency prompting.

### Features
- Streamlit web interface
- Adjustable number of attempts (3–9)
- Optional OpenAI API integration
- Normalizes common answer formats before voting
- Displays individual attempt summaries, answer agreement, and vote distribution
- Offline demonstration for the sample notebook problem

### Requirements
- Python 3.10+
- Packages in `requirements.txt`
- Optional: OpenAI API key for solving general word problems

### Run locally
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

Open the local URL shown in the terminal (usually http://localhost:8501).

### Enable AI mode
Set your API key as an environment variable. Do not paste keys into source code or commit them to Git.

Windows PowerShell:
```powershell
$env:OPENAI_API_KEY="your-key"
$env:OPENAI_MODEL="gpt-4o-mini"
streamlit run app.py
```

macOS/Linux:
```bash
export OPENAI_API_KEY="your-key"
export OPENAI_MODEL="gpt-4o-mini"
streamlit run app.py
```

### Example problem
A shop sells notebooks for ₹25 each. Riya buys 4 notebooks and pays with ₹200. How much change should she receive?

Expected result: ₹100.

### Methodology
1. Generate multiple independent solution attempts.
2. Extract each final answer.
3. Normalize answer strings to reduce formatting differences.
4. Use majority voting to select the most common answer.
5. Report agreement as `votes for selected answer / total attempts`.

### Limitations
- Agreement is not proof of correctness; attempts may share the same error.
- Basic normalization handles simple numeric answers best. More advanced projects can add unit-aware parsing and symbolic verification.
- API mode incurs provider usage costs and requires internet access.
- Offline mode only demonstrates the included notebook example; it does not claim to solve arbitrary questions.

### Suggested extensions
- Add a benchmark set of 20–50 math word problems.
- Compare single-attempt accuracy with self-consistency accuracy.
- Add symbolic verification using SymPy.
- Save evaluation results to CSV and plot accuracy against number of attempts.
