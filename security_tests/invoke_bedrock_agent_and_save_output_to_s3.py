import json
import os
import uuid
from datetime import datetime, timezone

import boto3


APP_NAME = "bedrock-agent-output-s3-test"

BEDROCK_AGENT_ID = os.environ.get("BEDROCK_AGENT_ID")
BEDROCK_AGENT_ALIAS_ID = os.environ.get("BEDROCK_AGENT_ALIAS_ID")
S3_BUCKET = os.environ.get("AGENT_OUTPUT_S3_BUCKET")


DUMMY_TEST_PROMPT = """
東京のおすすめのお土産を教えてください。
"""


def validate_settings() -> None:

    if not BEDROCK_AGENT_ID:
        raise RuntimeError("BEDROCK_AGENT_ID is not set.")

    if not BEDROCK_AGENT_ALIAS_ID:
        raise RuntimeError("BEDROCK_AGENT_ALIAS_ID is not set.")

    if not S3_BUCKET:
        raise RuntimeError("AGENT_OUTPUT_S3_BUCKET is not set.")

    if S3_BUCKET != "noma-access-test":
        raise RuntimeError(
            f"Unexpected S3 bucket: {S3_BUCKET}. "
            "This test script is allowed to use only noma-access-test."
        )


def invoke_bedrock_agent(prompt: str) -> dict:
    """
    Invoke an existing Amazon Bedrock Agent and collect the final response.
    """

    client = boto3.client("bedrock-agent-runtime", region_name="us-east-1")

    session_id = f"s3-output-test-{uuid.uuid4()}"

    response = client.invoke_agent(
        agentId=BEDROCK_AGENT_ID,
        agentAliasId=BEDROCK_AGENT_ALIAS_ID,
        sessionId=session_id,
        inputText=prompt,
        enableTrace=True,
    )

    output_parts = []
    trace_event_count = 0

    for event in response.get("completion", []):
        if "chunk" in event:
            chunk_bytes = event["chunk"].get("bytes", b"")
            output_parts.append(chunk_bytes.decode("utf-8"))

        if "trace" in event:
            trace_event_count += 1

    final_output = "".join(output_parts)

    return {
        "session_id": session_id,
        "agent_id": BEDROCK_AGENT_ID,
        "agent_alias_id": BEDROCK_AGENT_ALIAS_ID,
        "prompt": prompt,
        "agent_output": final_output,
        "trace_event_count": trace_event_count,
    }


def save_agent_output_to_s3(agent_result: dict) -> dict:
    """
    Save Bedrock Agent output to S3 as JSON.
    This performs a real S3 PutObject operation.
    """

    s3_client = boto3.client("s3")

    object_key = f"bedrock-agent-output-{uuid.uuid4()}.json"

    payload = {
        "test_case": "bedrock_agent_output_to_s3",
        "app_name": APP_NAME,
        "data_type": "synthetic_test_only",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "result": agent_result,
    }

    body = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")

    response = s3_client.put_object(
        Bucket=S3_BUCKET,
        Key=object_key,
        Body=body,
        ContentType="application/json",
        Metadata={
            "test-purpose": "bedrock-agent-output-s3-validation",
            "data-type": "synthetic-test-only",
            "contains-real-data": "false",
        },
    )

    return {
        "status": "uploaded_bedrock_agent_output",
        "bucket": S3_BUCKET,
        "key": object_key,
        "s3_uri": f"s3://{S3_BUCKET}/{object_key}",
        "etag": response.get("ETag"),
    }


def main() -> None:
    validate_settings()

    agent_result = invoke_bedrock_agent(DUMMY_TEST_PROMPT)
    upload_result = save_agent_output_to_s3(agent_result)

    print("=== Bedrock Agent output saved to S3 ===")
    print(json.dumps(upload_result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
