import streamlit as st
import pandas as pd
import nltk
from datetime import datetime
from feedback_model import learn_weights
from nlp_engine import build_similarity_matrix
from matching_engine import (get_top_matches,DEFAULT_WEIGHTS)
nltk.download("stopwords")
st.set_page_config(page_title="Intelligent Hybrid Recommendation System",page_icon="🌐",layout="wide")
USERS_FILE = "data/users.csv"
FEEDBACK_FILE = "data/feedback.csv"
users_df = pd.read_csv(USERS_FILE)
feedback_df = pd.read_csv(FEEDBACK_FILE)
if len(feedback_df) > 20:
    try:
        LEARNED_WEIGHTS, MODEL_ACCURACY = (learn_weights(feedback_df))
    except Exception:
        LEARNED_WEIGHTS = DEFAULT_WEIGHTS
        MODEL_ACCURACY = 0
else:
    LEARNED_WEIGHTS = DEFAULT_WEIGHTS
    MODEL_ACCURACY = 0
def get_user_weights(user_id):
    user_feedback = feedback_df[feedback_df["user_id"] == user_id]
    required_columns = {"text_score","mbti_score","location_score","action"}
    if not required_columns.issubset(user_feedback.columns):
        return DEFAULT_WEIGHTS, 0
    if len(user_feedback) < 20:
        return DEFAULT_WEIGHTS, 0
    if user_feedback["action"].nunique() < 2:
        return DEFAULT_WEIGHTS, 0
    try:
        return learn_weights(user_feedback)
    except Exception:
        return DEFAULT_WEIGHTS, 0
cosine_matrix = build_similarity_matrix(users_df)
# Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio("Menu",["Dashboard","Profiles","Recommendations","Analytics"])
# Dashboard
if page == "Dashboard":
    st.title("🌐 Intelligent Hybrid Recommendation System")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Users",len(users_df))
    col2.metric("Feedback Records",len(feedback_df))
    col3.metric("Acceptance Rate",f"{feedback_df['action'].mean()*100:.1f}%")
    col4.metric("Model Accuracy",f"{MODEL_ACCURACY:.2%}")
    st.markdown("---")
    st.subheader("Global Learned Weights")
    weights_df = pd.DataFrame({"Factor": ["Text Similarity","MBTI","Location"],"Weight": [LEARNED_WEIGHTS["w1"],LEARNED_WEIGHTS["w2"],LEARNED_WEIGHTS["w3"]]})
    st.bar_chart(weights_df.set_index("Factor"))
    st.subheader("Current Recommendation Formula")
    st.latex(rf"""Score=({LEARNED_WEIGHTS['w1']:.2f})\times TextSimilarity+({LEARNED_WEIGHTS['w2']:.2f})\times MBTI+({LEARNED_WEIGHTS['w3']:.2f})\times Location""")
# Profiles
elif page == "Profiles":
    st.title("User Profiles")
    uid = st.selectbox("Select User",users_df["user_id"])
    user = users_df[users_df["user_id"] == uid].iloc[0]
    st.subheader(user["name"])
    st.write(f"Profession: {user['profession']}")
    st.write(f"Location: {user['location']}")
    st.write(f"MBTI: {user['mbti']}")
    st.write(f"Experience: {user['experience_years']} years")
    st.write(f"Interests: {user['interests']}")
    st.markdown("### Professional Summary")
    st.write(user["professional_summary"])
    st.markdown("### About Me")
    st.write(user["about_me"])
# Recommendations
elif page == "Recommendations":
    st.title("Top 5 Recommendations")
    uid = st.selectbox("Choose User",users_df["user_id"])
    USER_WEIGHTS, USER_ACC = (get_user_weights(uid))
    matches = get_top_matches(uid,users_df,cosine_matrix,USER_WEIGHTS)
    for _, row in matches.iterrows():
        st.subheader(row["name"])
        st.progress(row["compatibility_score"] / 100)
        st.metric("Compatibility Score",f"{row['compatibility_score']}%")
        st.write(f"Profession: {row['profession']}")
        st.write(f"Location: {row['location']}")
        st.write(f"MBTI: {row['mbti']}")
        with st.expander("Score Breakdown"):
            st.write(f"Text Similarity: {row['text_similarity']}%")
            st.write(f"MBTI Score: {row['mbti_score']}")
            st.write(f"Location Score: {row['location_score']}")
        col1, col2 = st.columns(2)
        with col1:
            if st.button(f"👍 Accept {row['user_id']}"):
                feedback_df.loc[len(feedback_df)] = [uid,row["user_id"],row["text_similarity"],row["mbti_score"],row["location_score"],1,datetime.now()]
                feedback_df.to_csv(FEEDBACK_FILE,index=False)
                st.success("Feedback Saved")
                st.rerun()
        with col2:
            if st.button(f"👎 Reject {row['user_id']}"):
                feedback_df.loc[len(feedback_df)] = [uid,row["user_id"],row["text_similarity"],row["mbti_score"],row["location_score"],0,datetime.now()]
                feedback_df.to_csv(FEEDBACK_FILE,index=False)
                st.warning("Feedback Saved")
                st.rerun()
        st.divider()
# Analytics
elif page == "Analytics":
    st.title("Analytics Dashboard")
    st.metric("Global Model Accuracy",f"{MODEL_ACCURACY:.2%}")
    st.subheader("MBTI Distribution")
    st.bar_chart(users_df["mbti"].value_counts())
    st.subheader("Location Distribution")
    st.bar_chart(users_df["location"].value_counts())
    st.subheader("Profession Distribution")
    st.bar_chart(users_df["profession"].value_counts())
    st.subheader("Feedback Analysis")
    st.bar_chart(feedback_df["action"].value_counts())
    st.markdown("---")
    st.subheader("User-Specific Learning")
    selected_user = st.selectbox("Select User",users_df["user_id"],key="analytics_user")
    weights, acc = get_user_weights(selected_user)
    weights_df = pd.DataFrame({"Factor":["Text Similarity","MBTI","Location"],"Weight":[weights["w1"],weights["w2"],weights["w3"]]})
    st.bar_chart(weights_df.set_index("Factor"))
    st.metric("User Model Accuracy",f"{acc:.2%}")
    st.subheader("Learned Recommendation Formula")
    st.latex(rf"""Score=({weights['w1']:.2f})\times TextSimilarity+({weights['w2']:.2f})\times MBTI+({weights['w3']:.2f})\times Location""")
    baseline_acceptance = (feedback_df["action"].mean()* 100)
    trained_accuracy = (acc * 100)
    st.subheader("Performance Analysis")
    st.write(f"Historical Acceptance Rate: {baseline_acceptance:.2f}%")
    st.write(f"User Model Accuracy: {trained_accuracy:.2f}%")