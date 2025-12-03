import pickle

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score
import pandas as pd


def main():
    # Load data
    df = pd.read_csv("emails.csv")
    df["text"] = df["subject"].fillna("") + " " + df["body"].fillna("")

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        df["text"], df["label"], test_size=0.2, random_state=42, stratify=df["label"]
    )

    # Vectorizer with ngrams and max features
    vectorizer = TfidfVectorizer(stop_words="english", max_features=8000, ngram_range=(1, 2))
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    # Linear SVM
    model = LinearSVC()
    model.fit(X_train_vec, y_train)

    preds = model.predict(X_test_vec)
    acc = accuracy_score(y_test, preds)
    print(f"Accuracy: {acc*100:.2f}%")

    # Save artifacts
    with open("model.pkl", "wb") as f:
        pickle.dump(model, f)

    with open("vectorizer.pkl", "wb") as f:
        pickle.dump(vectorizer, f)

    print("Saved model.pkl and vectorizer.pkl")


if __name__ == "__main__":
    main()
