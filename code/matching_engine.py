import pandas as pd
MBTI_COMPATIBILITY = {
    ("INTJ", "ENFP"): 95,
    ("ENFP", "INTJ"): 95,
    ("INTP", "ENFJ"): 95,
    ("ENFJ", "INTP"): 95,
    ("INFJ", "ENTP"): 90,
    ("ENTP", "INFJ"): 90,
    ("INFP", "ENTJ"): 90,
    ("ENTJ", "INFP"): 90,
    ("INTJ", "INTJ"): 85,
    ("INTP", "INTP"): 85,
    ("ENTJ", "ENTJ"): 80,
    ("ENFP", "ENFP"): 80,
    ("INFJ", "INFJ"): 80,
    ("INFP", "INFP"): 75,
    ("INTJ", "INTP"): 80,
    ("INTP", "INTJ"): 80,
    ("ISTJ", "INTJ"): 75,
    ("INTJ", "ISTJ"): 75,
    ("ISTJ", "ISFJ"): 70,
    ("ISFJ", "ISTJ"): 70,
    ("ESTJ", "ISTJ"): 70,
    ("ISTJ", "ESTJ"): 70,
    ("INFP", "ENFP"): 75,
    ("ENFP", "INFP"): 75,
    ("ISFP", "ENFP"): 72,
    ("ENFP", "ISFP"): 72,
    ("ENTJ", "ENFJ"): 78,
    ("ENFJ", "ENTJ"): 78,
    ("ESTJ", "ENTJ"): 72,
    ("ENTJ", "ESTJ"): 72,
    ("ISTP", "ESTP"): 70,
    ("ESTP", "ISTP"): 70,
    ("ESFP", "ISFP"): 68,
    ("ISFP", "ESFP"): 68,
    ("ESFJ", "ISFJ"): 72,
    ("ISFJ", "ESFJ"): 72,
}
LOCATION_CLUSTERS = {
    "Mumbai": "West",
    "Pune": "West",
    "Ahmedabad": "West",
    "Surat": "West",
    "Delhi": "North",
    "Jaipur": "North",
    "Bangalore": "South",
    "Chennai": "South",
    "Hyderabad": "South",
    "Kolkata": "East"
}
DEFAULT_WEIGHTS = {"w1": 0.50,"w2": 0.30,"w3": 0.20}
def get_mbti_score(mbti1, mbti2):
    return MBTI_COMPATIBILITY.get((mbti1, mbti2),50)
def get_location_score(loc1, loc2):
    if loc1 == loc2:
        return 100
    region1 = LOCATION_CLUSTERS.get(loc1)
    region2 = LOCATION_CLUSTERS.get(loc2)
    if region1 == region2:
        return 60
    return 20
def compatibility_score(text_sim,mbti_score,location_score,weights):
    score = (weights["w1"]*text_sim*100+weights["w2"]*mbti_score+weights["w3"]*location_score)
    return round(score, 2)
def get_top_matches(user_id,users_df,cosine_matrix,weights):
    uid_to_idx = {uid : idx for idx, uid in enumerate(users_df["user_id"])}
    source_idx = uid_to_idx[user_id]
    source = users_df.iloc[source_idx]
    results = []
    for target_idx, target in users_df.iterrows():
        if target_idx == source_idx:
            continue
        text_sim = cosine_matrix[source_idx][target_idx]
        mbti_score = get_mbti_score(source["mbti"],target["mbti"])
        location_score = get_location_score(source["location"],target["location"])
        final_score = compatibility_score(text_sim,mbti_score,location_score,weights)
        results.append({
            "user_id": target["user_id"],
            "name": target["name"],
            "profession": target["profession"],
            "location": target["location"],
            "mbti": target["mbti"],
            "text_similarity": round(text_sim * 100, 2),
            "mbti_score": mbti_score,
            "location_score": location_score,
            "compatibility_score": final_score
        })
    return pd.DataFrame(results)\
        .sort_values("compatibility_score",ascending=False)\
        .head(5)