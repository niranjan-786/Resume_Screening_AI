import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import PyPDF2
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import csv
from flask import send_file
import io

# Flask app setup
app = Flask(__name__)
UPLOAD_FOLDER = os.path.join('static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///results.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# DB Setup
db = SQLAlchemy(app)

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# DB model
from datetime import datetime

class ResumeResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resume_name = db.Column(db.String(100))
    score = db.Column(db.Float)
    job_description = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Extract text from PDF
def extract_text_from_pdf(file_path):
    with open(file_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        text = ''
        for page in reader.pages:
            text += page.extract_text() or ''
    return text



@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    job_description = ''
    if request.method == 'POST':
        job_description = request.form['job_description']
        resumes = request.files.getlist('resumes[]')

        jd_text = job_description
        resume_texts = []
        filenames = []

        for resume in resumes:
            if resume.filename == '':
                continue

            filepath = os.path.join(app.config['UPLOAD_FOLDER'], resume.filename)
            resume.save(filepath)

            text = extract_text_from_pdf(filepath)
            resume_texts.append(text)
            filenames.append(resume.filename)

        documents = [jd_text] + resume_texts
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(documents)
        similarity_scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()

        # Save to DB
        for name, score in zip(filenames, similarity_scores):
            entry = ResumeResult(resume_name=name, score=round(score * 100, 2), job_description=job_description)
            db.session.add(entry)
        db.session.commit()

        results = sorted(zip(filenames, similarity_scores), key=lambda x: x[1], reverse=True)

    return render_template('index.html', results=results, job_description=job_description)
@app.route('/history')
def history():
    all_data = ResumeResult.query.order_by(ResumeResult.timestamp.desc()).all()
    return render_template('history.html', records=all_data)
@app.route('/download')
def download_csv():
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Resume Name', 'Score', 'Job Description', 'Timestamp'])

    results = ResumeResult.query.order_by(ResumeResult.timestamp.desc()).all()
    for row in results:
        writer.writerow([row.resume_name, row.score, row.job_description, row.timestamp])

    output.seek(0)
    return send_file(io.BytesIO(output.getvalue().encode('utf-8')),
                     mimetype='text/csv',
                     as_attachment=True,
                     download_name='resume_screening_results.csv')
@app.route('/clear_history')
def clear_history():
    ResumeResult.query.delete()
    db.session.commit()
    return "<h3>Screening history cleared successfully. <a href='/'>Go Back</a></h3>"
@app.route('/view_resume/<filename>')
def view_resume(filename):
    return render_template('view_resume.html', filename=filename)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
