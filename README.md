# Self-Consistency Math Solver

## Project Overview
The Self-Consistency Math Solver is a Generative AI project designed to solve multi-step mathematical word problems using Large Language Models (LLMs). It generates multiple independent reasoning attempts, normalizes their final answers, and applies majority voting to select the most consistent answer.

## Features
- Solves mathematical word problems using Chain-of-Thought prompting.
- Generates multiple reasoning attempts.
- Uses answer normalization to handle different numerical formats and units.
- Applies majority voting to determine the final answer.
- Displays agreement metrics and individual attempts.
- Provides an interactive web interface using Streamlit.
- Supports offline demonstration mode and live API mode.

## Technology Stack
- Python
- Generative AI and Large Language Models
- OpenAI API
- Streamlit
- Regular Expressions
- Git and GitHub

## Project Structure

```text
Self-Consistency-Math-Solver/
├── app/
│   ├── app.py
│   ├── solver.py
│   ├── normalizer.py
│   └── prompts.py
├── evaluation/
│   └── evaluate.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_REPOSITORY_URL
cd YOUR_REPOSITORY_FOLDER
```

Replace the placeholders with your actual GitHub repository URL and folder name.

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
streamlit run app/app.py
```

The application should open in your browser. If it does not, open the local URL displayed in the terminal.

## API Configuration
For live language-model inference, configure the required API credentials using an environment variable named `OPENAI_API_KEY`. Keep your API key private and never commit it to GitHub.

The project also describes an offline demonstration mode when API credentials are unavailable.

## Working Principle
1. Accept a mathematical word problem from the user.
2. Generate multiple independent reasoning attempts.
3. Extract the final answer from each attempt.
4. Normalize numerical answers and remove unnecessary units or formatting.
5. Count the occurrences of each normalized answer.
6. Select the majority-vote answer.
7. Display the selected answer, agreement metrics, and reasoning attempts.

## Evaluation
The project report describes a benchmark comparison between greedy Chain-of-Thought decoding and self-consistency majority voting. It reports 74.20% accuracy for greedy decoding and 88.60% for self-consistency under the reported experimental setup.

These figures are the results stated in the project report; they should not be treated as independently reproduced results unless the benchmark is run and verified.

## Future Enhancements
- Integrate symbolic calculation tools.
- Implement weighted majority voting.
- Introduce adaptive sampling to reduce computation.
- Expand mathematical benchmark coverage.

## Author
Nivedita Sharma

## License
Add a suitable open-source license if you intend to distribute this project for reuse.

