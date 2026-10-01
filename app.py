import streamlit as st
import pdfplumber
import sys
import os


# -----------------------------------
# ADD SRC FOLDER
# -----------------------------------

sys.path.append(
    os.path.join(os.path.dirname(__file__), "src")
)


from skill_extractor import (
    extract_skills,
    calculate_skill_match
)

from similarity import calculate_similarity

from scorer import calculate_overall_score


# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(
    page_title="AI Resume Screening System",
    page_icon="🤖",
    layout="wide"
)


# -----------------------------------
# TITLE
# -----------------------------------

st.title("🤖 AI Resume Screening System")

st.write(
    "AI-powered resume screening using "
    "skill matching and NLP similarity."
)

st.divider()


# -----------------------------------
# SIDEBAR
# -----------------------------------

st.sidebar.title("⚙️ Settings")

threshold = st.sidebar.slider(
    "Shortlisting Threshold",
    min_value=0,
    max_value=100,
    value=70,
    step=5
)

st.sidebar.write(
    f"Candidates scoring **{threshold}% or above** "
    "will be marked for recruiter review."
)


# -----------------------------------
# JOB DESCRIPTION
# -----------------------------------

st.header("📋 Job Description")

job_description = st.text_area(
    "Paste the job description below:",
    height=220,
    placeholder="Example: Python, SQL, React, Git..."
)


# -----------------------------------
# RESUME UPLOAD
# -----------------------------------

st.header("📄 Upload Candidate Resumes")

uploaded_resumes = st.file_uploader(
    "Upload one or more PDF resumes",
    type=["pdf"],
    accept_multiple_files=True
)


if uploaded_resumes:

    st.success(
        f"✅ {len(uploaded_resumes)} resume(s) uploaded"
    )


# -----------------------------------
# ANALYZE
# -----------------------------------

if st.button(
    "🔍 Analyze Candidates",
    use_container_width=True
):

    if not job_description:

        st.warning(
            "⚠️ Please enter a job description."
        )

        st.stop()


    if not uploaded_resumes:

        st.warning(
            "⚠️ Please upload at least one resume."
        )

        st.stop()


    # -----------------------------------
    # JOB SKILLS
    # -----------------------------------

    job_skills = extract_skills(
        job_description
    )


    candidates = []


    # -----------------------------------
    # PROCESS RESUMES
    # -----------------------------------

    with st.spinner(
        "🤖 Analyzing resumes..."
    ):

        for uploaded_file in uploaded_resumes:

            resume_text = ""


            # Extract PDF text

            with pdfplumber.open(
                uploaded_file
            ) as pdf:

                for page in pdf.pages:

                    page_text = page.extract_text()

                    if page_text:

                        resume_text += (
                            page_text + "\n"
                        )


            # Extract skills

            resume_skills = extract_skills(
                resume_text
            )


            # Skill matching

            matched_skills, missing_skills, skill_score = calculate_skill_match(
                resume_skills,
                job_skills
            )


            # NLP similarity

            nlp_score = calculate_similarity(
                resume_text,
                job_description
            )


            # Overall score

            overall_score = calculate_overall_score(
                skill_score,
                nlp_score
            )


            # Save candidate

            candidates.append({

                "Candidate": uploaded_file.name,

                "Skill Match": skill_score,

                "NLP Similarity": nlp_score,

                "Overall Score": overall_score,

                "Matched Skills": matched_skills,

                "Missing Skills": missing_skills

            })


    # -----------------------------------
    # SORT
    # -----------------------------------

    candidates.sort(
        key=lambda x: x["Overall Score"],
        reverse=True
    )


    # -----------------------------------
    # SUMMARY
    # -----------------------------------

    st.divider()

    st.header("📊 Screening Summary")


    total_candidates = len(candidates)


    shortlisted_count = sum(
        1
        for candidate in candidates
        if candidate["Overall Score"] >= threshold
    )


    average_score = sum(
        candidate["Overall Score"]
        for candidate in candidates
    ) / total_candidates


    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "👥 Total Candidates",
            total_candidates
        )


    with col2:

        st.metric(
            "✅ Shortlisted",
            shortlisted_count
        )


    with col3:

        st.metric(
            "📈 Average Score",
            f"{average_score:.2f}%"
        )


    # -----------------------------------
    # RANKING TABLE
    # -----------------------------------

    st.divider()

    st.header("🏆 Candidate Ranking")


    table_data = []


    for rank, candidate in enumerate(
        candidates,
        start=1
    ):

        status = (
            "✅ Shortlisted"
            if candidate["Overall Score"] >= threshold
            else "❌ Not Shortlisted"
        )


        table_data.append({

            "Rank": rank,

            "Candidate": candidate["Candidate"],

            "Skill Match": f"{candidate['Skill Match']:.2f}%",

            "NLP Similarity":
                f"{candidate['NLP Similarity']:.2f}%",

            "Overall Score":
                f"{candidate['Overall Score']:.2f}%",

            "Status": status

        })


    st.table(table_data)


    # -----------------------------------
    # CANDIDATE DETAILS
    # -----------------------------------

    st.divider()

    st.header("🔎 Candidate Details")


    for rank, candidate in enumerate(
        candidates,
        start=1
    ):

        with st.expander(
            f"#{rank} — {candidate['Candidate']}"
        ):

            col1, col2, col3 = st.columns(3)


            with col1:

                st.metric(
                    "Skill Match",
                    f"{candidate['Skill Match']:.2f}%"
                )


            with col2:

                st.metric(
                    "NLP Similarity",
                    f"{candidate['NLP Similarity']:.2f}%"
                )


            with col3:

                st.metric(
                    "Overall Score",
                    f"{candidate['Overall Score']:.2f}%"
                )


            if candidate["Overall Score"] >= threshold:

                st.success(
                    "✅ SHORTLISTED FOR RECRUITER REVIEW"
                )

            else:

                st.error(
                    "❌ BELOW SHORTLIST THRESHOLD"
                )


            st.write(
                "**Matched Skills:**"
            )


            if candidate["Matched Skills"]:

                st.write(
                    ", ".join(
                        candidate["Matched Skills"]
                    )
                )

            else:

                st.write("None")


            st.write(
                "**Missing Skills:**"
            )


            if candidate["Missing Skills"]:

                st.write(
                    ", ".join(
                        candidate["Missing Skills"]
                    )
                )

            else:

                st.write("None")