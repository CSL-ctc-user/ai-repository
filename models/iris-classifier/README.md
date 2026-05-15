---
library_name: scikit-learn
tags:
  - machine-learning
  - model-artifact
  - classification
  - random-forest
  - joblib
  - iris
pipeline_tag: tabular-classification
---

# Iris Classifier Model Card

## Model summary

This directory contains an actual trained machine learning model artifact for Noma GitHub Models scanning validation.

## Model details

- Framework: scikit-learn
- Algorithm: RandomForestClassifier
- Model artifact: iris_classifier.joblib
- Task: classification
- Dataset: sklearn.datasets.load_iris

## Files

- train_model.py: trains the model and saves the model artifact
- predict.py: loads the model artifact and runs inference
- model_config.json: model metadata
- iris_classifier.joblib: trained model artifact

## Intended use

This model is intended for validating AI/ML asset detection in a GitHub code repository.

## Limitations

This is a small demonstration model trained on the built-in Iris dataset.

It is not intended for production use.

## AI/ML asset signals

- scikit-learn
- RandomForestClassifier
- joblib
- trained model artifact
- iris_classifier.joblib
- tabular classification
