# Simple Helpdesk Agent

This is a simple AI agent built with the OpenAI Agents SDK.

## Purpose

This agent is used for Noma Source Code Management validation.

It demonstrates a minimal but real AI agent implementation with:

- Agent definition
- Instructions
- Model configuration
- Function tool
- Runner execution

## Agent

- Name: Simple Helpdesk Agent
- Framework: OpenAI Agents SDK
- Default model: gpt-4o-mini

## Tool

- search_internal_faq

## Run

Set your OpenAI API key in PowerShell:

$env:OPENAI_API_KEY = "sk-..."

Install dependencies:

pip install -r requirements-simple-agent.txt

Run:

python .\simple_agent\helpdesk_agent.py

Do not commit real API keys.
