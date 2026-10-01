import pdfplumber
import os
import sys

from skill_extractor import extract_skills, calculate_skill_match
from similarity import calculate_similarity
from scorer import calculate_overall_score

sys.stdout.reconfigure(encoding="utf-8")


# -----------------------------
# 1. Resume PDF
# -----------------------------

pdf_path = r"C:\Desktop\VS CODE folders\Resume Screening\resumes\Rahul_Resume.pdf"


# -----------------------------
# 2. Job Description
# -----------------------------

job_path = r"C:\Desktop\VS CODE folders\Resume Screening\job_description.txt"


print("Resume exists:", os.path.exists(pdf_path))
print("Job description exists:", os.path.exists(job_path))


# -----------------------------
# 3. Extract resume text
# -----------------------------

resume_text = ""

with pdfplumber.open(pdf_path) as pdf:

    for page in pdf.pages:

        page_text = page.extract_text()

        if page_text:
            resume_text += page_text + "\n"


# -----------------------------
# 4. Read job description
# -----------------------------

with open(job_path, "r", encoding="utf-8") as file:

    job_text = file.read()


# -----------------------------
# 5. Extract skills
# -----------------------------

resume_skills = extract_skills(resume_text)

job_skills = extract_skills(job_text)


# -----------------------------
# 6. Calculate matching
# -----------------------------

matched_skills, missing_skills, score = calculate_skill_match(
    resume_skills,
    job_skills
)
nlp_score = calculate_similarity(
    resume_text,
    job_text
)
overall_score = calculate_overall_score(
    score,
    nlp_score
)

# -----------------------------
# 7. Display results
# -----------------------------

print("\n--------- RESUME SKILLS ---------\n")

for skill in resume_skills:
    print(skill)


print("\n--------- REQUIRED SKILLS ---------\n")

for skill in job_skills:
    print(skill)


print("\n--------- MATCHED SKILLS ---------\n")

for skill in matched_skills:
    print(skill)


print("\n--------- MISSING SKILLS ---------\n")

for skill in missing_skills:
    print(skill)


print("\n--------- SKILL MATCH SCORE ---------\n")

print(f"{score:.2f}%")


print("\n--------- NLP SIMILARITY SCORE ---------\n")

print(f"{nlp_score:.2f}%")
print("\n--------- OVERALL CANDIDATE SCORE ---------\n")
print(f"{overall_score:.2f}%")