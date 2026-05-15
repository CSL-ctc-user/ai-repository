from pathlib import Path

import joblib


MODEL_DIR = Path(__file__).resolve().parent
MODEL_PATH = MODEL_DIR / "iris_classifier.joblib"


def predict(sample: list[float]) -> dict:
    model_package = joblib.load(MODEL_PATH)

    model = model_package["model"]
    target_names = model_package["target_names"]

    prediction_index = int(model.predict([sample])[0])
    prediction_label = target_names[prediction_index]

    return {
        "sample": sample,
        "prediction_index": prediction_index,
        "prediction_label": prediction_label,
        "model_type": model_package["model_type"],
        "dataset": model_package["dataset"],
    }


if __name__ == "__main__":
    sample = [5.1, 3.5, 1.4, 0.2]
    result = predict(sample)
    print(result)
