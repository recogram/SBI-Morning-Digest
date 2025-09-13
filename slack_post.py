import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

TOKEN = os.getenv("SLACK_BOT_TOKEN")
CHANNEL = os.getenv("SLACK_CHANNEL", "#general")

client = WebClient(token=TOKEN)

def post_to_slack(summary: dict, source_url: str):
    if not TOKEN:
        raise RuntimeError("SLACK_BOT_TOKEN が未設定です")

    text_lines = [f"*SBI モーニング情報まとめ（{summary['date']}）*"]
    text_lines.append(f"<{source_url}|元記事はこちら>")
    for s in summary.get("sections", []):
        text_lines.append(f"\n• *{s['title']}*")
        for b in s.get("bullets", []):
            text_lines.append(f"    - {b}")

    text = "\n".join(text_lines)

    try:
        client.chat_postMessage(channel=CHANNEL, text=text)
    except SlackApiError as e:
        print(f"Slack API error: {e.response['error']}")
