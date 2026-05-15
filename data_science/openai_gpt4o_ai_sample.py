"""
openai_gpt4o_ai_sample.py

Purpose:
This file is a sample AI application script for GitHub inventory detection.
It demonstrates usage of OpenAI GPT-4o in an AI assistant scenario.

Important:
- Do not store API keys in this file.
- Use environment variables such as OPENAI_API_KEY.
"""

from openai import OpenAI


# AI model metadata
MODEL_PROVIDER = "OpenAI"
MODEL_NAME = "gpt-4o"

# AI application metadata
APPLICATION_NAME = "OpenAI GPT-4o Sample AI Assistant"
APPLICATION_CATEGORY = "AI assistant"
USE_CASE = "AI model usage detection test for GitHub repository inventory"


def build_messages(user_question: str):
    """
    Build messages for a sample AI assistant.
    """
    return [
        {
            "role": "system",
            "content": (
                "You are a helpful AI assistant. "
                "You answer questions clearly and safely."
            ),
        },
        {
            "role": "user",
            "content": user_question,
        },
    ]


def generate_answer(user_question: str):
    """
    Example function showing how this application would call OpenAI GPT-4o.

    This function requires OPENAI_API_KEY to be set as an environment variable.
    Do not hardcode API keys in source code.
    """
    client = OpenAI()

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=build_messages(user_question),
        temperature=0.2,
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    print("Application:", APPLICATION_NAME)
    print("Provider:", MODEL_PROVIDER)
    print("Model:", MODEL_NAME)

    # Uncomment only when OPENAI_API_KEY is configured locally.
    # print(generate_answer("What is generative AI?"))