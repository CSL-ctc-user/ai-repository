# Noma SCM Validation Repository

This repository contains real AI application source code imported from public sample repositories for validating Noma Source Code Management integration.

## Purpose

This repository is used to validate whether Noma can discover and enrich AI assets with source code management context.

## Included AI Source Code

- OpenAI API quickstart Python examples
- Amazon Bedrock samples
- Amazon Bedrock RAG sample using Knowledge Bases
- RAG, agent, model invocation, embeddings, and pipeline examples

## Expected Noma Context

Noma should be able to associate AI-related source code with:

- GitHub repository
- Organization
- Branch
- Commit history
- Source path
- AI model usage
- RAG implementation
- Agent/function calling implementation
- Build or supply chain context, if workflows are present

## Security Notes

Do not commit real API keys, AWS access keys, GitHub tokens, OpenAI API keys, or customer data.

Use environment variables or GitHub Secrets for credentials.
