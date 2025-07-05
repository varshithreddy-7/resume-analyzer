import docx2txt
import fitz  # PyMuPDF
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def extract_text(path):
    if path.endswith(".pdf"):
        with fitz.open(path) as doc:
            return " ".join([page.get_text() for page in doc])
    elif path.endswith(".docx"):
        return docx2txt.process(path)
    return ""

def analyze_resume(resume_path, job_desc):
    resume_text = extract_text(resume_path)
    corpus = [resume_text, job_desc]

    tfidf = TfidfVectorizer(stop_words="english")
    matrix = tfidf.fit_transform(corpus)
    score = cosine_similarity(matrix[0:1], matrix[1:2])[0][0]

    resume_words = set(resume_text.lower().split())
    jd_words = set(job_desc.lower().split())

    matches = resume_words & jd_words
    missing = jd_words - resume_words

    return round(score * 100, 2), list(matches), list(missing)[:10]