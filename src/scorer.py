def calculate_overall_score(skill_score, nlp_score):

    overall_score = (skill_score * 0.60) + (nlp_score * 0.40)

    return overall_score