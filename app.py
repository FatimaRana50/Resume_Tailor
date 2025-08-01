# app.py

import streamlit as st
import tempfile
import os
from resume_tailor_core import analyze_resume

st.set_page_config(page_title="Resume Tailor", layout="centered")
st.title("📄 Resume Tailoring Assistant")
st.markdown("Upload your **Resume** and **Job Description** PDFs to get personalized suggestions.")

# File upload
resume_file = st.file_uploader("Upload Resume (PDF)", type="pdf")
jd_file = st.file_uploader("Upload Job Description (PDF)", type="pdf")

if st.button("Analyze Resume") and resume_file and jd_file:
    with st.spinner("Analyzing your resume..."):

        # Save uploaded files temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_resume:
            tmp_resume.write(resume_file.read())
            resume_path = tmp_resume.name

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_jd:
            tmp_jd.write(jd_file.read())
            jd_path = tmp_jd.name

        try:
            # Call analysis logic
            response = analyze_resume(resume_path, jd_path)

            # Show results
            st.success("Analysis Complete!")
            st.subheader("📌 Suggested Improvements:")
            st.write(response)

        except Exception as e:
            st.error(f"Something went wrong: {e}")

        finally:
            os.remove(resume_path)
            os.remove(jd_path)
