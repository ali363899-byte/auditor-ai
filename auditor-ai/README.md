# AuditorAI 🛡️ — Automated Code Review & Security Scanner

An enterprise-focused developer productivity tool that analyzes source code for vulnerabilities, architectural bottlenecks, and code smell, rendering real-time radar quality metrics and production-ready refactored solutions.

## 🚀 Live Demo
Try the application live: **[auditor-ai-app.streamlit.app](https://auditor-ai-app.streamlit.app)**

## Architecture & Engineering Highlights
- **Heuristic Quality Scoring:** Parses incoming source across Security, Performance, and Readability vectors.
- **Strict JSON Contract:** Uses constrained structured schema output from LLM agents to ensure reproducible, machine-readable audit reports.
- **Data Visualization:** Renders interactive polar radar charts with Plotly for instant visual triage.
- **Multi-Language Support:** Analyzes Python, Java, JavaScript, TypeScript, C++, SQL, and Luau.

## Tech Stack
- **Frontend / Engine:** Python, Streamlit
- **Visualization:** Plotly
- **AI Core:** Google GenAI SDK (`gemini-3.8-flash`)

## Local Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/ali363899-byte/auditor-ai.git
   cd auditor-ai
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   streamlit run app.py
   ```
