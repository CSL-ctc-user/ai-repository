import asyncio
import os
from agents import Agent, Runner, function_tool


MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


FAQ_DATA = {
    "password": "パスワードを忘れた場合は、社内ポータルのパスワードリセットページから再設定してください。",
    "vpn": "VPNに接続できない場合は、ネットワーク接続、認証情報、有効な証明書を確認してください。",
    "github": "GitHubリポジトリが表示されない場合は、Organization配下のRepository accessに対象リポジトリが含まれているか確認してください。",
    "noma": "NomaでGitHubリポジトリが検出されない場合は、GitHub AppがOrganizationにインストールされ、対象リポジトリがonboardされているか確認してください。",
    "bedrock": "Amazon Bedrockのログ確認では、CloudWatch Logsにmodel invocation logsが出力されているか確認してください。",
}


@function_tool
def search_internal_faq(keyword: str) -> str:
    """
    Search a small internal FAQ knowledge base by keyword.
    """

    keyword_lower = keyword.lower()

    for key, answer in FAQ_DATA.items():
        if key in keyword_lower:
            return answer

    return (
        "該当するFAQは見つかりませんでした。"
        "質問内容を password, vpn, github, noma, bedrock のいずれかに近い内容で聞いてください。"
    )


helpdesk_agent = Agent(
    name="Simple Helpdesk Agent",
    model=MODEL_NAME,
    instructions=(
        "あなたは社内ヘルプデスク用のAIエージェントです。"
        "ユーザーの質問に対して、必要に応じて search_internal_faq ツールを使い、"
        "簡潔で分かりやすく回答してください。"
        "FAQにない内容は、FAQに見つからないことを明確に伝えてください。"
    ),
    tools=[
        search_internal_faq,
    ],
)


async def main() -> None:
    question = "NomaでGitHubリポジトリが検出されない場合はどうすればいい？"

    result = await Runner.run(
        helpdesk_agent,
        question,
    )

    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
