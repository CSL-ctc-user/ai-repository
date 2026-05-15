from pathlib import Path

from transformers import pipeline


REPO_ROOT = Path(__file__).resolve().parents[1]
MODEL_DIR = REPO_ROOT / "models" / "hf-text-classifier"


def main() -> None:
    classifier = pipeline(
        task="text-classification",
        model=str(MODEL_DIR),
        tokenizer=str(MODEL_DIR),
    )

    samples = [
        "Noma should discover Hugging Face model artifacts in GitHub repositories.",
        "User cannot connect to VPN and needs help.",
        "This repository contains PyTorch Transformers model training code.",
    ]

    for sample in samples:
        result = classifier(sample)
        print({"text": sample, "prediction": result})


if __name__ == "__main__":
    main()
