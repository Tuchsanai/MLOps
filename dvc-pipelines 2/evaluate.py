
import joblib
import pandas as pd
from omegaconf import OmegaConf
from sklearn.metrics import accuracy_score, f1_score


def evaluate(config):
    print("Evaluating...")
    test_inputs = joblib.load(config.features.test_features_save_path)
    test_df = pd.read_csv(config.data.test_csv_save_path)

    test_outputs = test_df["label"].values
    class_names = test_df["sentiment"].unique().tolist()

    model = joblib.load(config.train.model_save_path)

    metric_name = config.evaluate.metric
    metric = {
        "accuracy": accuracy_score,
        "f1_score": f1_score
    }[metric_name]

    predicted_test_outputs = model.predict(test_inputs)

    result = metric(test_outputs, predicted_test_outputs)
    result_dict = {metric_name: float(result)}
    OmegaConf.save(result_dict, config.evaluate.results_save_path)


if __name__ == "__main__":
    config = OmegaConf.load("./params.yaml")
    evaluate(config)
