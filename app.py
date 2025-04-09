
from flask import Flask, render_template, request
import os
from werkzeug.utils import secure_filename
from analyzer.analyze_resume import analyze_resume

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        resume = request.files["resume"]
        jd_text = request.form.get("job_description")
        jd_file = request.files.get("jd_file")

        jd_content = jd_text if jd_text.strip() else jd_file.read().decode("utf-8")

        if resume and jd_content:
            filename = secure_filename(resume.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            resume.save(filepath)
            result = analyze_resume(filepath, jd_content)

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
