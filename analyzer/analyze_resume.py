
import os
import re
import fitz  # PyMuPDF
import language_tool_python

def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def count_matched_keywords(resume_text, job_description):
    job_keywords = set(re.findall(r'\b\w+\b', job_description.lower()))
    resume_words = set(re.findall(r'\b\w+\b', resume_text.lower()))
    matched = job_keywords & resume_words
    return len(matched), len(job_keywords), matched, job_keywords - matched

def check_sections(text):
    sections = {
        "Work Experience": False,
        "Education": False,
        "Skills": False,
        "Phone": False,
        "Email": False,
    }
    lowered = text.lower()

    # Basic keyword checks
    sections["Work Experience"] = any(kw in lowered for kw in ["work experience", "employment", "experience", "professional experience"])
    sections["Education"] = "education" in lowered
    sections["Skills"] = "skills" in lowered

    # Contact details
    email_found = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
    phone_found = re.search(r'\+?\d[\d\s\-()]{7,}\d', text)

    sections["Email"] = bool(email_found)
    sections["Phone"] = bool(phone_found)

    return sections

def grammar_score(text):
    tool = language_tool_python.LanguageToolPublic("en-US")
    matches = tool.check(text)
    total_errors = len(matches)
    score = max(0, 100 - total_errors * 2)
    return score, total_errors

def analyze_resume(resume_path, job_description_text):
    resume_text = extract_text_from_pdf(resume_path)

    # Keyword Match
    match_count, total_keywords, matched, missing = count_matched_keywords(resume_text, job_description_text)
    keyword_score = int((match_count / total_keywords) * 50) if total_keywords else 0

    # Grammar Score
    grammar_score_val, total_errors = grammar_score(resume_text)
    grammar_score_scaled = int(grammar_score_val * 0.3)

    # Section check
    sections = check_sections(resume_text)
    section_score = sum(sections.values()) * 3  # 6 sections * 3 = 18 max

    total_score = keyword_score + grammar_score_scaled + section_score

    return {
        "score": min(total_score, 100),
        "matched_keywords": list(matched),
        "missing_keywords": list(missing),
        "grammar_errors": total_errors,
        "sections_present": sections
    }
