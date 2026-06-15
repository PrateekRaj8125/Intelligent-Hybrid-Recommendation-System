import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
nltk.download("stopwords")
nltk.download("wordnet")
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))
def clean_text(text):
    text = str(text).lower()
    text = ''.join(ch for ch in text if ch not in string.punctuation)
    words = text.split()
    words = [lemmatizer.lemmatize(word) for word in words if word not in stop_words]
    return " ".join(words)
def build_similarity_matrix(users_df):
    users_df["combined_text"] = (users_df["professional_summary"]+" "+ users_df["about_me"])
    users_df["clean_text"] = (users_df["combined_text"].apply(clean_text))
    vectorizer = TfidfVectorizer(max_features=500,ngram_range=(1,2))
    tfidf_matrix = vectorizer.fit_transform(users_df["clean_text"])
    cosine_matrix = cosine_similarity(tfidf_matrix)
    return cosine_matrix