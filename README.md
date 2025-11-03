# career_recommender
A career recommender for guiding the learners

This Streamlit web app helps college students discover personalized career paths based on their skills, interests, and resume content. It uses a trained machine learning model to recommend careers, suggest relevant projects, and provide a step-by-step roadmap — all wrapped in a downloadable PDF summary.

---

##  Features

-  **Career Prediction** using NLP and ML
-  **Dashboard Visualization** of confidence, skill match, and interest match
-  **Suggested Projects** tailored to the recommended career
-  **Career Roadmap** with actionable next steps
-  **Resume Upload** (.docx) for automatic profile extraction
-  **Feedback Form** to collect user insights
-  **PDF Export** with logo, timestamp, and full summary

---

##  Tech Stack

- **Frontend**: Streamlit
- **ML Model**: scikit-learn + joblib
- **NLP**: docx2txt + TF-IDF vectorizer
- **Visualization**: Altair
- **PDF Generation**: fpdf
- **Deployment**: Streamlit Cloud

---

## 📦 Installation

```bash
pip install -r requirements.txt
streamlit run app.py

Files
- app.py: Main Streamlit app
- career_model.pkl: Trained ML model
- vectorizer.pkl: TF-IDF vectorizer
- label_encoder.pkl: Career label encoder
- logo.png: Branding image for PDF
- requirements.txt: Dependencies

 Sample Output
Users receive:
- Career recommendation (e.g., Data Scientist)
- Confidence score (e.g., 87.5%)
- Suggested projects (e.g., Loan Predictor)
- Career roadmap (e.g., Learn Python → Build Projects → Apply for internships)
- Downloadable PDF summary

Author
Rishi — Aspiring AI/ML and Data Analytics professional
Focused on building impactful, user-friendly tools that showcase end-to-end ownership and real-world relevance.

Live Demo
https://careerrecommenderryryry.streamlit.app/

Feedback
Feel free to open issues or submit pull requests. Feedback is welcome!

