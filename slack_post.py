import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
CHANNEL = os.getenv("SLACK_CHANNEL", "#general")

client = WebClient(token=SLACK_BOT_TOKEN)

def post_to_slack(report: dict):
    lines = ["*今日の株式市況まとめ*"]

    for section in ["今日の株式市況", "前日の米国市場", "業種・個別株動向", "新興株・IPO"]:
        if section in report:
            lines.append(f"\n*{section}*")
            lines.append(report[section])

    if "ロイター補足" in report:
        lines.append("\n*補足*")
        lines.append(report["ロイター補足"])

    # 出典リンク
    links = []
    if "株探リンク" in report:
        links.append(f"<{report['株探リンク']}|株探全文>")
    if "Yahooリンク" in report:
        links.append(f"<{report['Yahooリンク']}|Yahoo全文>")
    if "ロイターリンク" in report:
        links.append(f"<{report['ロイターリンク']}|ロイター全文>")

    if links:
        lines.append("\n参照: " + " / ".join(links))

    text = "\n".join(lines)

    try:
        client.chat_postMessage(channel=CHANNEL, text=text)
    except SlackApiError as e:
        print(f"Slack API error: {e.response['error']}")
