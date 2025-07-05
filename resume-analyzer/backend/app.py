from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import os
from analyzer import analyze_resume

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    resume = request.files["resume"]
    jobdesc = request.form["jobdesc"]

    filename = secure_filename(resume.filename)
    path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    resume.save(path)

    score, matches, missing = analyze_resume(path, jobdesc)
    return render_template("result.html", score=score, matches=matches, missing=missing)

if __name__ == "__main__":
    app.run(debug=True)