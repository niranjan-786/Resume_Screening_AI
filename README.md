🧠 AI Powered Resume Screening System

An intelligent web app that automates the process of screening resumes using NLP and machine learning. It compares resumes against a given job description and ranks candidates based on their relevance — helping recruiters save time and effort.

🚀 Features

Upload multiple resumes (PDF)

Automatically extract text using PyPDF2

Compare resumes with job description using TF-IDF and cosine similarity

View top-scoring candidates instantly

Track screening history with timestamps

Export results as CSV

Simple, clean Flask-based web interface

🧩 Tech Stack

Backend: Flask (Python)

Database: SQLite (via SQLAlchemy)

ML/NLP: TF-IDF + Cosine Similarity (scikit-learn)

Frontend: HTML, CSS, Jinja Templates

⚙️ Installation
git clone https://github.com/niranjan-786/Resume_Screening_AI.git
cd AI-Powered-Resume-Screening-System
pip install -r requirements.txt
python app.py


Then open your browser at http://localhost:5000

📁 Project Structure
app.py               → Flask backend
templates/           → HTML templates
static/uploads/      → Uploaded resumes
requirements.txt     → Dependencies
results.db           → SQLite database

🧠 How It Works

Upload a job description and multiple resumes.

The system extracts text from PDFs.

It uses TF-IDF + cosine similarity to compute match scores.

Displays ranked results and saves them to the database.

📜 License

This project is licensed under the MIT License.
Feel free to modify and improve it!
