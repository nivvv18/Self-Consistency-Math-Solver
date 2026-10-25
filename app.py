import os
import re
from collections import Counter
import streamlit as st

st.set_page_config(page_title="Self-Consistency Math Solver", page_icon="🧮", layout="centered")

st.title("🧮 Self-Consistency Math Solver")
st.write("Solve a word problem using several independent attempts, then select the answer that appears most consistently.")

st.info("Self-consistency runs the same problem through multiple independent solution attempts. The most frequent normalized answer is selected. This demo asks for concise solution summaries rather than hidden chain-of-thought.")

DEFAULT_PROBLEM = "A shop sells notebooks for ₹25 each. Riya buys 4 notebooks and pays with ₹200. How much change should she receive?"
problem = st.text_area("Enter a math word problem", value=DEFAULT_PROBLEM, height=120)
num_paths = st.slider("Number of independent attempts", min_value=3, max_value=9, value=5, step=2)
temperature = st.slider("Variation between attempts", min_value=0.0, max_value=1.0, value=0.7, step=0.1)

with st.expander("API settings (optional)"):
    st.write("For AI-powered attempts, add an OpenAI API key in the environment variable `OPENAI_API_KEY` and install the dependencies in requirements.txt.")
    st.code("Windows PowerShell:  $env:OPENAI_API_KEY='your-key'\nmacOS/Linux:       export OPENAI_API_KEY='your-key'")
    model = st.text_input("Model name", value=os.getenv("OPENAI_MODEL", "gpt-4o-mini"))

def demo_attempt(problem_text, i):
    # Small deterministic examples so the project can be explored without an API key.
    p = problem_text.lower()
    if "notebook" in p and "25" in p and "4" in p and "200" in p:
        variants = [
            ("4 notebooks cost 4 × ₹25 = ₹100. Change = ₹200 − ₹100.", "₹100"),
            ("Total cost is ₹25 + ₹25 + ₹25 + ₹25 = ₹100; ₹200 − ₹100 = ₹100.", "100 rupees"),
            ("Multiply 25 by 4 to get 100, then subtract from 200: 100.", "₹100"),
            ("Cost = 25 × 4 = 100. Change = 200 − 100 = 100.", "100"),
            ("Four notebooks cost ₹100, so the change is ₹100.", "₹100"),
            ("₹25 each for 4 is ₹100. The remaining amount from ₹200 is ₹100.", "₹100"),
            ("₹25 × 4 = ₹100; ₹200 − ₹100 = ₹100.", "100 rupees"),
            ("The purchase costs ₹100 and the payment is ₹200, leaving ₹100.", "₹100"),
            ("Total = ₹100. Change = ₹200 - ₹100 = ₹100.", "100"),
        ]
        return variants[i % len(variants)]
    # Generic offline fallback is deliberately transparent: it doesn't pretend to solve arbitrary questions.
    return ("Offline demo mode supports the included notebook example only. Add an API key for general word problems.", "Unable to solve offline")

def ai_attempt(problem_text, attempt_no, model_name, temp):
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model=model_name,
        temperature=temp,
        messages=[
            {"role": "system", "content": (
                "You are a careful math problem solver. Solve the user's word problem independently. "
                "Return exactly two sections: 'Solution summary:' with a short, checkable calculation "
                "(no private deliberation), and 'Final answer:' with one concise answer. "
                "If information is missing, say so rather than guessing."
            )},
            {"role": "user", "content": f"Independent attempt #{attempt_no}. Solve this problem:\n{problem_text}"}
        ]
    )
    content = response.choices[0].message.content or ""
    match = re.search(r"Final answer:\s*(.+)", content, re.I)
    answer = match.group(1).strip().splitlines()[0] if match else content.strip().splitlines()[-1]
    return content, answer

def normalize_answer(answer):
    a = answer.lower().strip()
    a = re.sub(r"^(the answer is|answer:|final answer:)\s*", "", a)
    a = a.replace(",", "")
    # Normalize common currency/number formatting while preserving non-numeric answers.
    nums = re.findall(r"-?\d+(?:\.\d+)?", a)
    if nums:
        return nums[-1]
    return re.sub(r"[^\w\s]", "", a).strip()

if st.button("Run self-consistency solver", type="primary", use_container_width=True):
    if not problem.strip():
        st.warning("Please enter a math word problem first.")
    else:
        api_key = os.getenv("OPENAI_API_KEY")
        attempts = []
        progress = st.progress(0)
        status = st.empty()
        try:
            for i in range(num_paths):
                status.write(f"Running independent attempt {i+1} of {num_paths}…")
                if api_key:
                    result, answer = ai_attempt(problem, i+1, model, temperature)
                else:
                    result, answer = demo_attempt(problem, i)
                attempts.append({"summary": result, "answer": answer, "normalized": normalize_answer(answer)})
                progress.progress((i+1)/num_paths)
            status.empty()
            progress.empty()

            counts = Counter(a["normalized"] for a in attempts)
            winner, votes = counts.most_common(1)[0]
            st.subheader("Selected answer")
            st.success(f"**{next((a['answer'] for a in attempts if a['normalized'] == winner), winner)}**")
            st.metric("Agreement", f"{votes}/{num_paths}", f"{votes/num_paths:.0%} of attempts")
            st.caption("Agreement is a consistency signal, not a guarantee of correctness. Different attempts can share the same mistake.")
            st.subheader("Attempt-by-attempt results")
            for idx, item in enumerate(attempts, 1):
                with st.expander(f"Attempt {idx} — answer: {item['answer']}"):
                    st.write(item["summary"])
                    st.caption(f"Normalized vote: `{item['normalized']}`")
            st.subheader("Vote distribution")
            for answer, count in counts.most_common():
                st.write(f"**{answer}** — {count} vote(s)")
                st.progress(count/num_paths)
            if not api_key:
                st.warning("You're in offline demo mode. The included notebook example is supported. Set OPENAI_API_KEY to solve general problems with an LLM.")
        except Exception as e:
            st.error(f"Could not complete the run: {e}")
            st.caption("Check your API key, model name, internet connection, and installed dependencies.")

with st.expander("How it works"):
    st.markdown("""
    1. Send the same problem to the model multiple times.
    2. Each attempt produces a short calculation summary and final answer.
    3. Normalize equivalent answer formats (for example, `₹100` and `100 rupees`).
    4. Count the votes and select the most common answer.
    5. Show the attempts and agreement rate so a user can inspect the result.
    """)
