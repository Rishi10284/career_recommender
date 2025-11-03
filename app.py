import streamlit as st
import joblib
import docx2txt
import numpy as np
import pandas as pd
import altair as alt
from fpdf import FPDF
from datetime import datetime

# Load saved components
model = joblib.load('career_model.pkl')
vectorizer = joblib.load('vectorizer.pkl')
le = joblib.load('label_encoder.pkl')

# Project suggestions
project_ideas = {
    'Data Scientist': ['Loan Default Predictor', 'Customer Segmentation', 'Time Series Forecasting'],
    'Frontend Developer': ['Portfolio Website', 'Responsive Blog UI', 'E-commerce Landing Page'],
    'Backend Developer': ['REST API with Spring Boot', 'Authentication System', 'Inventory Manager'],
    'Software Developer': ['Sorting Visualizer', 'Quiz App', 'Chat Application'],
    'Data Analyst': ['Sales Dashboard', 'Excel Automation', 'Survey Insights'],
    'AI Engineer': ['Chatbot with NLP', 'Emotion Detection', 'AI Resume Screener'],
    'Generalist': ['Task Manager', 'Weather App', 'To-Do List with CRUD']
}

# Career roadmaps
career_roadmaps = {
    'Data Scientist': [
        "Learn Python, NumPy, Pandas",
        "Master data visualization (Matplotlib, Seaborn)",
        "Study statistics and machine learning (scikit-learn)",
        "Build projects: Loan Predictor, Customer Segmentation",
        "Take courses: Coursera, Kaggle, Analytics Vidhya",
        "Apply for internships or freelance gigs"
    ],
    'Backend Developer': [
        "Learn Python, Java, or Node.js",
        "Understand REST APIs and databases (SQL, MongoDB)",
        "Build projects: Auth System, Inventory Manager",
        "Explore frameworks: Django, Spring Boot, Express",
        "Take backend-focused courses (Udemy, freeCodeCamp)",
        "Contribute to open-source or backend internships"
    ],
    # Add more careers as needed
}

# Scoring function
def calculate_scores(user_skills, user_interests, model, vectorizer, le):
    input_text = user_skills + " " + user_interests
    input_vec = vectorizer.transform([input_text])
    
    probs = model.predict_proba(input_vec)[0]
    top_idx = np.argmax(probs)
    top_career = le.inverse_transform([top_idx])[0]
    confidence = round(probs[top_idx] * 100, 2)

    skill_score = min(len(user_skills.split(',')) * 10, 100)
    interest_score = min(len(user_interests.split()) * 10, 100)

    return top_career, confidence, skill_score, interest_score

# Chart function
def show_dashboard(confidence, skill_score, interest_score):
    data = pd.DataFrame({
        'Metric': ['Confidence', 'Skill Match', 'Interest Match'],
        'Score': [confidence, skill_score, interest_score]
    })

    chart = alt.Chart(data).mark_bar().encode(
        x='Metric',
        y='Score',
        color='Metric'
    ).properties(
        title='Career Recommendation Breakdown'
    )

    st.altair_chart(chart, use_container_width=True)

# Feedback form
def collect_feedback():
    st.markdown("---")
    st.subheader("📣 Share Your Feedback")

    rating = st.slider("How helpful was this recommendation?", 1, 5, 3)
    comments = st.text_area("Any suggestions or feedback?")

    if st.button("Submit Feedback"):
        st.success("✅ Thank you for your feedback!")
        with open("feedback_log.txt", "a") as f:
            f.write(f"Rating: {rating}, Comments: {comments}\n")

# PDF generator
def generate_pdf(career, projects, confidence, skill_score, interest_score, roadmap):
    pdf = FPDF()
    pdf.add_page()

    # Add logo
    try:
        pdf.image("logo.png.png", x=10, y=8, w=30)
    except:
        pass

    pdf.set_xy(50, 10)
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(100, 10, txt="Career Recommendation Summary", ln=True, align='C')
    pdf.ln(20)

    # Timestamp
    timestamp = datetime.now().strftime("%d %B %Y, %I:%M %p")
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt=f"Generated on: {timestamp}", ln=True)
    pdf.ln(5)

    # Career and scores
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Recommended Career: {career}", ln=True)
    pdf.cell(200, 10, txt=f"Confidence: {confidence}%", ln=True)
    pdf.cell(200, 10, txt=f"Skill Match Score: {skill_score}", ln=True)
    pdf.cell(200, 10, txt=f"Interest Match Score: {interest_score}", ln=True)
    pdf.ln(10)

    # Projects
    pdf.cell(200, 10, txt="Suggested Projects:", ln=True)
    for proj in projects:
        pdf.cell(200, 10, txt=f"- {proj}", ln=True)

    # Roadmap
    pdf.cell(200, 10, txt="Career Roadmap:", ln=True)
    for step in roadmap:
        pdf.cell(200, 10, txt=f"- {step}", ln=True)

    return pdf.output(dest='S').encode('latin-1')

# UI
st.title("🎓 Career Path Recommender for College Students")
st.markdown("Enter your skills and interests, or upload your resume to get a personalized career suggestion.")

skills = st.text_input("🛠️ Enter your skills (comma-separated):")
interests = st.text_input("💡 Enter your interests:")

uploaded_file = st.file_uploader("📄 Or upload your resume (.docx)", type=["docx"])
resume_text = ""

if uploaded_file is not None:
    resume_text = docx2txt.process(uploaded_file)
    st.text_area("📃 Extracted Resume Text", resume_text[:1000])

if st.button("🚀 Recommend Career"):
    if resume_text:
        profile = resume_text.lower()
        skills = ""
        interests = ""
    else:
        profile = skills.lower() + " " + interests.lower()

    career, confidence, skill_score, interest_score = calculate_scores(skills, interests, model, vectorizer, le)

    st.success(f"🎯 Recommended Career Path: {career}")
    st.write("💡 Suggested Projects to Build:")

    suggested_projects = project_ideas.get(career, ['Explore open-source ideas on GitHub'])
    for proj in suggested_projects:
        st.markdown(f"- {proj}")

    st.markdown("### 🛣️ Career Roadmap")
    roadmap = career_roadmaps.get(career, ["Explore learning paths on LinkedIn Learning or Coursera"])
    for step in roadmap:
        st.markdown(f"- {step}")

    show_dashboard(confidence, skill_score, interest_score)
    collect_feedback()

    pdf_data = generate_pdf(career, suggested_projects, confidence, skill_score, interest_score, roadmap)

    st.download_button(
        label="📥 Download Summary as PDF",
        data=pdf_data,
        file_name="career_summary.pdf",
        mime="application/pdf"
    )