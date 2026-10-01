import re


# -----------------------------------
# SKILL DATABASE
# -----------------------------------

skills = [
    "python",
    "java",
    "c++",
    "javascript",
    "html",
    "css",
    "react",
    "node.js",
    "sql",
    "mysql",
    "mongodb",
    "git",
    "github",
    "docker",
    "aws",
    "machine learning",
    "deep learning",
    "tensorflow",
    "pytorch",
    "flask",
    "django",
    "rest api"
]


# -----------------------------------
# NORMALIZE TEXT
# -----------------------------------

def normalize_text(text):

    text = text.lower()

    # Replace common variations

    text = text.replace("node js", "node.js")
    text = text.replace("nodejs", "node.js")

    text = text.replace("react.js", "react")

    text = text.replace("restful api", "rest api")
    text = text.replace("restful apis", "rest api")

    text = text.replace("machine-learning", "machine learning")
    text = text.replace("deep-learning", "deep learning")

    return text


# -----------------------------------
# EXTRACT SKILLS
# -----------------------------------

def extract_skills(text):

    text = normalize_text(text)

    found_skills = []


    for skill in skills:

        # Escape special characters
        # such as + and .

        pattern = r"\b" + re.escape(skill) + r"\b"


        if re.search(pattern, text):

            found_skills.append(skill)


    return found_skills


# -----------------------------------
# CALCULATE SKILL MATCH
# -----------------------------------

def calculate_skill_match(
    resume_skills,
    required_skills
):

    resume_skills = set(resume_skills)

    required_skills = set(required_skills)


    matched_skills = (
        resume_skills.intersection(
            required_skills
        )
    )


    missing_skills = (
        required_skills - resume_skills
    )


    if len(required_skills) == 0:

        score = 0

    else:

        score = (
            len(matched_skills)
            / len(required_skills)
        ) * 100


    return (
        matched_skills,
        missing_skills,
        score
    )