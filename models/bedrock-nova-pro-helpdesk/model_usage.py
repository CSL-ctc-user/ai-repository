import os

from agents.extensions.models.litellm_model import LitellmModel


BEDROCK_MODEL_ID = "amazon.nova-pro-v1:0"
BEDROCK_MODEL_REFERENCE = "bedrock/amazon.nova-pro-v1:0"

BEDROCK_MODEL = os.getenv(
    "BEDROCK_MODEL",
    BEDROCK_MODEL_REFERENCE,
)

model = LitellmModel(
    model=BEDROCK_MODEL,
)


def get_model_metadata() -> dict:
    return {
        "provider": "Amazon Bedrock",
        "model_id": BEDROCK_MODEL_ID,
        "model_reference": BEDROCK_MODEL_REFERENCE,
        "framework": "OpenAI Agents SDK",
        "connector": "LiteLLM",
        "usage": "Simple Bedrock Helpdesk Agent",
        "source": "simple_agent/helpdesk_agent_bedrock.py",
    }


if __name__ == "__main__":
    print(get_model_metadata())
