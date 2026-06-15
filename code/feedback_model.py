from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
def learn_weights(feedback_df):
    if len(feedback_df) < 20:
        return ({"w1": 0.50,"w2": 0.30,"w3": 0.20},0.0)
    X = feedback_df[["text_score","mbti_score","location_score"]]
    y = feedback_df["action"]
    X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.25,random_state=42)
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)
    coefficients = abs(model.coef_[0])
    learned = coefficients / coefficients.sum()
    weights = {"w1": float(learned[0]),"w2": float(learned[1]),"w3": float(learned[2])}
    accuracy = accuracy_score(y_test,model.predict(X_test))
    return weights, accuracy