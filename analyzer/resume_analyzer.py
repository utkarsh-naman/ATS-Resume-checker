
import fitz  # PyMuPDF
import re
from collections import Counter
import language_tool_python

tool = language_tool_python.LanguageTool('en-US')

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def clean_text(text):
    return re.sub(r'[^a-zA-Z0-9 ]', '', text.lower())

def extract_keywords(text):
    words = clean_text(text).split()
    return set(words)

def analyze_resume(resume_path, job_description):
    resume_text = extract_text_from_pdf(resume_path)
    resume_keywords = extract_keywords(resume_text)
    jd_keywords = extract_keywords(job_description)

    matched = resume_keywords & jd_keywords
    missing = jd_keywords - resume_keywords

    match_score = int((len(matched) / len(jd_keywords)) * 60) if jd_keywords else 0

    # Check grammar/syntax using LanguageTool
    grammar_matches = tool.check(resume_text)
    grammar_score = max(0, 20 - len(grammar_matches))  # lose 1 point for each mistake

    # Basic formatting check: if at least 2 font sizes are used
    doc = fitz.open(resume_path)
    font_sizes = set()
    for page in doc:
        for b in page.get_text("dict")["blocks"]:
            for l in b.get("lines", []):
                for s in l.get("spans", []):
                    font_sizes.add(round(s.get("size", 0)))

    formatting_score = 20 if len(font_sizes) >= 2 else 10

    final_score = min(100, match_score + grammar_score + formatting_score)

    return {
        "score": final_score,
        "matched_keywords": ', '.join(matched),
        "missing_keywords": ', '.join(missing)
    }
