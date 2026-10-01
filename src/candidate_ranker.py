import os
import pdfplumber
import sys

from skill_extractor import extract_skills, calculate_skill_match
from similarity import calculate_similarity
from scorer import calculate_overall_score


sys.stdout.reconfigure(encoding="utf-8")


# Paths
resume_folder = r"C:\Desktop\VS CODE folders\Resume Screening\resumes"
job_path = r"C:\Desktop\VS CODE folders\Resume Screening\job_description.txt"


# Read job description
with open(job_path, "r", encoding="utf-8") as file:
    job_text = file.read()


# Extract required skills
job_skills = extract_skills(job_text)


# Store candidate results
candidates = []


# Process every PDF
for filename in os.listdir(resume_folder):

    if filename.lower().endswith(".pdf"):

        pdf_path = os.path.join(resume_folder, filename)

        resume_text = ""

        with pdfplumber.open(pdf_path) as pdf:

            for page in pdf.pages:

                page_text = page.extract_text()

                if page_text:
                    resume_text += page_text + "\n"


        # Extract candidate skills
        resume_skills = extract_skills(resume_text)


        # Calculate skill match
        matched_skills, missing_skills, skill_score = calculate_skill_match(
            resume_skills,
            job_skills
        )


        # Calculate NLP similarity
        nlp_score = calculate_similarity(
            resume_text,
            job_text
        )


        # Calculate overall score
        overall_score = calculate_overall_score(
            skill_score,
            nlp_score
        )


        # Store result
        candidates.append({
            "name": filename,
            "skill_score": skill_score,
            "nlp_score": nlp_score,
            "overall_score": overall_score,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills
        })


# Sort candidates by overall score
candidates.sort(
    key=lambda x: x["overall_score"],
    reverse=True
)



SHORTLIST_THRESHOLD = 70


print("\n========================================")
print("       CANDIDATE RANKING")
print("========================================\n")


shortlisted = []
not_shortlisted = []


for rank, candidate in enumerate(candidates, start=1):

    if candidate["overall_score"] >= SHORTLIST_THRESHOLD:
        status = "SHORTLISTED"
        shortlisted.append(candidate)
    else:
        status = "NOT SHORTLISTED"
        not_shortlisted.append(candidate)


    print(f"Rank {rank}")
    print(f"Resume: {candidate['name']}")
    print(f"Skill Match: {candidate['skill_score']:.2f}%")
    print(f"NLP Similarity: {candidate['nlp_score']:.2f}%")
    print(f"Overall Score: {candidate['overall_score']:.2f}%")
    print(f"Status: {status}")

    print("----------------------------------------")


print("\n========================================")
print("          SHORTLISTED CANDIDATES")
print("========================================\n")


for candidate in shortlisted:

    print(
        f"{candidate['name']} "
        f"-> {candidate['overall_score']:.2f}%"
    )


print("\n========================================")
print("        NOT SHORTLISTED CANDIDATES")
print("========================================\n")


for candidate in not_shortlisted:

    print(
        f"{candidate['name']} "
        f"-> {candidate['overall_score']:.2f}%"
    )