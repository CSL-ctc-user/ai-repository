from pathlib import Path
import json

import torch
from torch.utils.data import Dataset, DataLoader
from transformers import AutoTokenizer, AutoModelForSequenceClassification


BASE_MODEL_ID = "google/bert_uncased_L-2_H-128_A-2"
TOKENIZER_ID = "bert-base-uncased"

REPO_ROOT = Path(__file__).resolve().parents[1]
MODEL_DIR = REPO_ROOT / "models" / "hf-text-classifier"

LABELS = {
    0: "general_helpdesk",
    1: "ai_security",
}

ID2LABEL = {idx: label for idx, label in LABELS.items()}
LABEL2ID = {label: idx for idx, label in LABELS.items()}


TRAINING_SAMPLES = [
    {
        "text": "password reset request for internal portal",
        "label": "general_helpdesk",
    },
    {
        "text": "vpn connection troubleshooting and certificate check",
        "label": "general_helpdesk",
    },
    {
        "text": "github repository access issue for organization",
        "label": "general_helpdesk",
    },
    {
        "text": "noma security should discover ai ml assets in github repositories",
        "label": "ai_security",
    },
    {
        "text": "hugging face model download and ai model inventory detection",
        "label": "ai_security",
    },
    {
        "text": "amazon bedrock model invocation and ai agent monitoring",
        "label": "ai_security",
    },
    {
        "text": "machine learning model artifact saved with pytorch and transformers",
        "label": "ai_security",
    },
    {
        "text": "notebook pipeline job and model card for ai asset scanning",
        "label": "ai_security",
    },
]


class TextClassificationDataset(Dataset):
    def __init__(self, samples, tokenizer, max_length: int = 96):
        self.samples = samples
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, index):
        item = self.samples[index]
        encoding = self.tokenizer(
            item["text"],
            truncation=True,
            padding="max_length",
            max_length=self.max_length,
            return_tensors="pt",
        )

        label_id = LABEL2ID[item["label"]]

        result = {
            "input_ids": encoding["input_ids"].squeeze(0),
            "attention_mask": encoding["attention_mask"].squeeze(0),
            "labels": torch.tensor(label_id, dtype=torch.long),
        }

        if "token_type_ids" in encoding:
            result["token_type_ids"] = encoding["token_type_ids"].squeeze(0)

        return result


def main() -> None:
    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Downloading tokenizer from Hugging Face: {TOKENIZER_ID}")
    tokenizer = AutoTokenizer.from_pretrained(TOKENIZER_ID)

    print(f"Downloading base model from Hugging Face: {BASE_MODEL_ID}")
    model = AutoModelForSequenceClassification.from_pretrained(
        BASE_MODEL_ID,
        num_labels=len(LABELS),
        id2label=ID2LABEL,
        label2id=LABEL2ID,
    )

    dataset = TextClassificationDataset(TRAINING_SAMPLES, tokenizer)
    dataloader = DataLoader(dataset, batch_size=2, shuffle=True)

    optimizer = torch.optim.AdamW(model.parameters(), lr=5e-5)

    model.train()

    for epoch in range(3):
        total_loss = 0.0

        for batch in dataloader:
            optimizer.zero_grad()

            outputs = model(**batch)
            loss = outputs.loss

            loss.backward()
            optimizer.step()

            total_loss += float(loss.item())

        average_loss = total_loss / len(dataloader)
        print(f"epoch={epoch + 1}, average_loss={average_loss:.4f}")

    print(f"Saving fine-tuned model to: {MODEL_DIR}")
    model.save_pretrained(MODEL_DIR)
    tokenizer.save_pretrained(MODEL_DIR)

    metadata = {
        "asset_type": "model",
        "name": "hf-text-classifier",
        "base_model": BASE_MODEL_ID,
        "tokenizer": TOKENIZER_ID,
        "framework": "PyTorch",
        "library": "Hugging Face Transformers",
        "task": "text-classification",
        "labels": LABELS,
        "training_samples": len(TRAINING_SAMPLES),
        "source_file": "data_science/hf_text_classifier_training.py",
        "model_directory": "models/hf-text-classifier",
        "detection_signals": [
            "Hugging Face",
            "PyTorch",
            "Transformers",
            "AutoTokenizer",
            "AutoModelForSequenceClassification",
            "from_pretrained",
            "save_pretrained",
            "text-classification",
            "model artifact",
        ],
    }

    metadata_path = MODEL_DIR / "training_metadata.json"
    metadata_path.write_text(
        json.dumps(metadata, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print(f"Saved metadata: {metadata_path}")
    print("Training complete.")


if __name__ == "__main__":
    main()

