import os
import pandas as pd
from datasets import Dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer

MODEL_ID = os.getenv("HF_MODEL_ID", "FacebookAI/roberta-base")
DATASET_URI = os.getenv("TRAINING_DATASET_URI", "s3://acme-pds/csv/by_year/2025.csv")

def load_training_data():
    return pd.DataFrame({
        "text": [
            "The customer asked about savings account interest.",
            "The loan application was approved.",
            "The transaction appears suspicious.",
            "The payment failed due to insufficient funds."
        ],
        "label": [1, 1, 0, 0]
    })

def main():
    df = load_training_data()
    dataset = Dataset.from_pandas(df)

    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_ID, num_labels=2)

    def tokenize(batch):
        return tokenizer(batch["text"], padding="max_length", truncation=True, max_length=128)

    dataset = dataset.map(tokenize, batched=True)
    dataset = dataset.rename_column("label", "labels")

    training_args = TrainingArguments(
        output_dir="./outputs/roberta-classifier",
        per_device_train_batch_size=2,
        max_steps=1,
        report_to=[]
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset
    )

    trainer.train()
    trainer.save_model("./outputs/roberta-classifier")

if __name__ == "__main__":
    main()
