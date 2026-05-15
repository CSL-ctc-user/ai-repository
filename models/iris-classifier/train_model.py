from pathlib import Path

import joblib
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split


MODEL_DIR = Path(__file__).resolve().parent
MODEL_PATH = MODEL_DIR / "iris_classifier.joblib"


def main() -> None:
    iris = load_iris()

    X = iris.data
    y = iris.target

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
    )

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)

    print("Model type: RandomForestClassifier")
    print(f"Dataset: Iris")
    print(f"Accuracy: {accuracy:.4f}")
    print("Classification report:")
    print(classification_report(y_test, y_pred, target_names=iris.target_names))

    model_package = {
        "model": model,
        "model_type": "RandomForestClassifier",
        "dataset": "sklearn.datasets.load_iris",
        "feature_names": iris.feature_names,
        "target_names": iris.target_names.tolist(),
        "accuracy": accuracy,
    }

    joblib.dump(model_package, MODEL_PATH)

    print(f"Saved model artifact: {MODEL_PATH}")


if __name__ == "__main__":
    main()
