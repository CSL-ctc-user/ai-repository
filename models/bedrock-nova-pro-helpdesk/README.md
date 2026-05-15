---
library_name: openai-agents
tags:
  - ai-agent
  - amazon-bedrock
  - litellm
  - openai-agents-sdk
  - helpdesk-agent
  - model-usage
model_provider: Amazon Bedrock
model_id: amazon.nova-pro-v1:0
model_reference: bedrock/amazon.nova-pro-v1:0
pipeline_tag: text-generation
---

# Bedrock Nova Pro Helpdesk Agent Model Card

## Model summary

This model card documents the model usage for a simple helpdesk AI agent implemented in this repository.

## Model provider

- Provider: Amazon Bedrock
- Model ID: amazon.nova-pro-v1:0
- Model reference used in code: bedrock/amazon.nova-pro-v1:0

## Application

- Application name: Simple Bedrock Helpdesk Agent
- Source file: simple_agent/helpdesk_agent_bedrock.py
- Framework: OpenAI Agents SDK
- Model connector: LiteLLM

## Intended use

This model is used for a simple internal helpdesk-style AI agent validation scenario.

The agent answers questions about:

- GitHub repository detection
- Noma connector onboarding
- VPN troubleshooting
- Password reset guidance
- Amazon Bedrock logging checks

## Limitations

This repository does not contain proprietary model weights.

The model is referenced as a managed Amazon Bedrock foundation model.

## AI/ML asset signals

- Amazon Bedrock
- amazon.nova-pro-v1:0
- bedrock/amazon.nova-pro-v1:0
- OpenAI Agents SDK
- LiteLLM
- Agent
- Runner
- LitellmModel
