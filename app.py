
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
    try:
        if request.method == "POST":
            resume = request.files.get("resume")
            jd_text = request.form.get("job_description")
            jd_file = request.files.get("jd_file")

            if not resume:
                raise Exception("Resume file is missing.")

            if not jd_text.strip() and not jd_file:
                raise Exception("No job description provided.")

            jd_content = jd_text.strip() if jd_text.strip() else jd_file.read().decode("utf-8")

            filename = secure_filename(resume.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            resume.save(filepath)

            result = analyze_resume(filepath, jd_content)

    except Exception as e:
        print("🔥 Internal Server Error:", e)

    
    print("🎯 Analysis Result:", result)
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
