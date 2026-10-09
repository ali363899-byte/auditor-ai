import streamlit as st
import json
import plotly.graph_objects as go
from google import genai
from google.genai import types

st.set_page_config(
    page_title="AuditorAI — Automated Code Reviewer",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main { background-color: #0b0f19; }
    .stMetric { background-color: #161e2e; padding: 1rem; border-radius: 10px; border: 1px solid #2d3748; }
    h1, h2, h3 { color: #f8fafc; }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("🛡️ AuditorAI")
    st.caption("Enterprise Code Quality & Security Auditor")
    st.divider()
    
    api_key = st.text_input("Gemini API Key (Free tier):", type="password", help="Get a free key from aistudio.google.com")
    language = st.selectbox("Language Target:", ["Python", "Java", "JavaScript/TypeScript", "C++", "SQL", "Luau/Lua"])
    audit_depth = st.radio("Audit Focus:", ["Full Inspection (Security + Performance + Style)", "Strict Security & Vulnerabilities", "Big-O Performance & Efficiency"])
    
    st.divider()
    st.info("💡 **Recruiter Tip:** This tool performs static syntax parsing combined with zero-shot LLM heuristic analysis.")

# Main UI
st.title("Automated Code Review & Security Scanner")
st.write("Submit source code below to generate a vulnerability index, Big-O profile, and refactored implementation.")

code_input = st.text_area(
    "Paste your source code:",
    height=240,
    placeholder="// Paste your functions, classes, or queries here..."
)

def run_audit(code: str, lang: str, focus: str, key: str):
    client = genai.Client(api_key=key)
    
    system_prompt = f"""
    You are a Principal Software Architect and Security Engineer.
    Analyze the provided {lang} code under the focus: '{focus}'.
    
    You MUST respond with valid, parseable JSON matching this schema exactly:
    {{
        "security_score": <integer from 0 to 100>,
        "performance_score": <integer from 0 to 100>,
        "cleanliness_score": <integer from 0 to 100>,
        "overall_grade": "<A+|A|B|C|D|F>",
        "summary": "<1-2 sentence executive summary>",
        "vulnerabilities": [
            {{"severity": "<Critical|Medium|Low>", "issue": "<title>", "explanation": "<details>"}}
        ],
        "refactored_code": "<full refactored code without markdown ticks>"
    }}
    Do NOT output any markdown backticks around the JSON.
    """
    
    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=f"{system_prompt}\n\nSource Code:\n{code}",
    )
    return response.text

if st.button("🚀 Run Architecture Audit", type="primary"):
    if not api_key:
        st.error("Please provide an API key in the sidebar. You can get one in 10 seconds at https://aistudio.google.com")
    elif not code_input.strip():
        st.warning("Please provide code to analyze.")
    else:
        with st.spinner("Analyzing abstract syntax tree and security vectors..."):
            try:
                raw_result = run_audit(code_input, language, audit_depth, api_key)
                clean_json = raw_result.strip().removeprefix("```json").removesuffix("```").strip()
                data = json.loads(clean_json)

                # Metrics Row
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Security Score", f"{data['security_score']}/100")
                m2.metric("Performance Score", f"{data['performance_score']}/100")
                m3.metric("Code Cleanliness", f"{data['cleanliness_score']}/100")
                m4.metric("Overall Grade", data['overall_grade'])

                st.divider()

                # Visual Chart + Vulnerabilities
                c1, c2 = st.columns([1, 1.4])
                
                with c1:
                    st.subheader("📊 Quality Matrix")
                    fig = go.Figure(data=go.Scatterpolar(
                        r=[data['security_score'], data['performance_score'], data['cleanliness_score']],
                        theta=['Security', 'Performance', 'Cleanliness'],
                        fill='toself',
                        line_color='#38bdf8'
                    ))
                    fig.update_layout(
                        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                        showlegend=False,
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                        font=dict(color="#f8fafc")
                    )
                    st.plotly_chart(fig, use_container_width=True)

                with c2:
                    st.subheader("⚠️ Findings & Vulnerabilities")
                    st.write(f"**Executive Summary:** {data['summary']}")
                    
                    if not data['vulnerabilities']:
                        st.success("No critical or high-risk vulnerabilities detected.")
                    else:
                        for v in data['vulnerabilities']:
                            color = "🔴" if v['severity'] == "Critical" else ("🟡" if v['severity'] == "Medium" else "🟢")
                            with st.expander(f"{color} {v['severity']}: {v['issue']}"):
                                st.write(v['explanation'])

                st.divider()

                # Refactored Code Output
                st.subheader("✨ Optimized Implementation")
                st.code(data['refactored_code'], language=language.lower())

            except Exception as e:
                st.error(f"Execution Error: {str(e)}")