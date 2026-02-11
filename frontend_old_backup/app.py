import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/final-match"

st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

st.title("🤖 AI Resume Analyzer & Job Match Engine")

st.markdown(
    "Analyze how well a resume matches a job description using "
    "**ATS logic + ML semantic similarity**."
)

# Input columns
col1, col2 = st.columns(2)

with col1:
    resume_text = st.text_area(
        "📄 Resume Text",
        height=250,
        placeholder="Paste resume content here..."
    )

with col2:
    job_text = st.text_area(
        "💼 Job Description",
        height=250,
        placeholder="Paste job description here..."
    )

# Analyze button
if st.button("🚀 Analyze Match"):
    if not resume_text or not job_text:
        st.warning("Please provide both Resume and Job Description.")
    else:
        with st.spinner("Analyzing..."):
            response = requests.post(
                API_URL,
                json={
                    "resume_text": resume_text,
                    "job_text": job_text
                }
            )

        if response.status_code == 200:
            data = response.json()

            st.success("Analysis Complete ✅")

            # Scores
            st.subheader("📊 Match Scores")
            score_col1, score_col2, score_col3 = st.columns(3)

            score_col1.metric(
                "Skill Match %",
                f"{data['skill_match_percentage']}%"
            )
            score_col2.metric(
                "Semantic Match %",
                f"{data['semantic_match_percentage']}%"
            )
            score_col3.metric(
                "Final Match %",
                f"{data['final_match_percentage']}%"
            )

            # Skills
            st.subheader("🧠 Skill Analysis")

            col_a, col_b, col_c = st.columns(3)

            col_a.write("✅ **Resume Skills**")
            col_a.write(data["resume_skills"])

            col_b.write("🔗 **Common Skills**")
            col_b.write(data["common_skills"])

            col_c.write("❌ **Missing Skills**")
            col_c.write(data["missing_skills"])

        else:
            st.error("API Error. Please ensure backend is running.")
