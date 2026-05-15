import asyncio
import os

from agents import Agent, Runner, set_tracing_disabled
from agents.extensions.models.litellm_model import LitellmModel


# OpenAI tracing is disabled because this sample uses Amazon Bedrock via LiteLLM.
set_tracing_disabled(True)


BEDROCK_MODEL = os.getenv(
    "BEDROCK_MODEL",
    "bedrock/amazon.nova-pro-v1:0",
)

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")


helpdesk_agent = Agent(
    name="Simple Bedrock Helpdesk Agent",
    model=LitellmModel(
        model=BEDROCK_MODEL,
    ),
    instructions=(
        "あなたは社内ヘルプデスク用のAIエージェントです。"
        "以下のFAQを参考に、ユーザーの質問へ簡潔に日本語で回答してください。"
        "\n\n"
        "FAQ:\n"
        "- password: パスワードを忘れた場合は、社内ポータルのパスワードリセットページから再設定してください。\n"
        "- vpn: VPNに接続できない場合は、ネットワーク接続、認証情報、有効な証明書を確認してください。\n"
        "- github: GitHubリポジトリが表示されない場合は、Organization配下のRepository accessに対象リポジトリが含まれているか確認してください。\n"
        "- noma: NomaでGitHubリポジトリが検出されない場合は、GitHub AppがOrganizationにインストールされ、対象リポジトリがonboardされているか確認してください。\n"
        "- bedrock: Amazon Bedrockのログ確認では、CloudWatch Logsにmodel invocation logsが出力されているか確認してください。\n"
        "\n"
        "FAQにない内容は、FAQに見つからないことを明確に伝えてください。"
    ),
)


async def main() -> None:
    print(f"Using Bedrock model: {BEDROCK_MODEL}")
    print(f"Using AWS region: {AWS_REGION}")

    question = "NomaでGitHubリポジトリが検出されない場合はどうすればいい？"

    result = await Runner.run(
        helpdesk_agent,
        question,
    )

    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
