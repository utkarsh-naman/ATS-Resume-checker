
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
from analyzer.resume_analyzer import analyze_resume

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'resumes'), exist_ok=True)
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'job_descriptions'), exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        resume_file = request.files['resume']
        jd_text = request.form.get('job_description')
        jd_file = request.files.get('jd_file')

        resume_path = ''
        jd_content = ''

        if resume_file:
            filename = secure_filename(resume_file.filename)
            resume_path = os.path.join(app.config['UPLOAD_FOLDER'], 'resumes', filename)
            resume_file.save(resume_path)

        if jd_file and jd_file.filename != '':
            jd_filename = secure_filename(jd_file.filename)
            jd_path = os.path.join(app.config['UPLOAD_FOLDER'], 'job_descriptions', jd_filename)
            jd_file.save(jd_path)
            with open(jd_path, 'r', encoding='utf-8') as f:
                jd_content = f.read()
        elif jd_text:
            jd_content = jd_text

        if resume_path and jd_content:
            result = analyze_resume(resume_path, jd_content)
            return render_template('index.html', result=result)

    return render_template('index.html')
    
if __name__ == '__main__':
    app.run(debug=True)
