import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

TOKEN = os.getenv("SLACK_BOT_TOKEN")
CHANNEL = os.getenv("SLACK_CHANNEL")

client = WebClient(token=TOKEN)

def post_to_slack(summary: dict, source_url: str):
    text_lines = [f"*SBI モーニング情報まとめ（{summary['date']}）*"]
    text_lines.append(f"<{source_url}|SBI元記事はこちら>")

    # SBI要約
    for s in summary.get("sections", []):
        text_lines.append(f"\n• *{s['title']}*")
        for b in s.get("bullets", []):
            text_lines.append(f"    - {b}")

    # 市況ニュースまとめ
    if "market_summaries" in summary:
        text_lines.append("\n*今日の株式市況まとめ*")
        for s in summary["market_summaries"]:
            text_lines.append(s)

    text = "\n".join(text_lines)
    client.chat_postMessage(channel=CHANNEL, text=text)
