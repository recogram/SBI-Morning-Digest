import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

TOKEN = os.getenv("SLACK_BOT_TOKEN")
CHANNEL = os.getenv("SLACK_CHANNEL")

client = WebClient(token=TOKEN)

def post_market_reports(reports):
    text_lines = ["*今日の株式市況まとめ*"]

    for rep in reports:
        text_lines.append(f"\n【{rep['title']}】")
        text_lines.append(rep["summary"] if rep["summary"] else "(本文取得できず)")
        text_lines.append(f"<{rep['link']}|記事全文はこちら>")

    text = "\n".join(text_lines)
    client.chat_postMessage(channel=CHANNEL, text=text)
