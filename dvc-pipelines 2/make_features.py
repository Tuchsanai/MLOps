
import pandas as pd
from omegaconf import OmegaConf
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import joblib


def make_features(config):
    print("Making features...")
    train_df = pd.read_csv(config.data.train_csv_save_path)
    test_df = pd.read_csv(config.data.test_csv_save_path)

    vectorizer_name = config.features.vectorizer
    vectorizer = {
        "count-vectorizer": CountVectorizer,
        "tfidf-vectorizer": TfidfVectorizer
    }[vectorizer_name](stop_words="english")

    train_inputs = vectorizer.fit_transform(train_df["review"])
    test_inputs = vectorizer.transform(test_df["review"])

    joblib.dump(train_inputs, config.features.train_features_save_path)
    joblib.dump(test_inputs, config.features.test_features_save_path)


if __name__ == "__main__":
    config = OmegaConf.load("./params.yaml")
    make_features(config)
