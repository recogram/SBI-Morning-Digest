import requests
from datetime import datetime
import os
from slack_sdk import WebClient

# ====== Slack設定 ======
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")   # GitHub Secretsに設定
CHANNEL = os.getenv("SLACK_CHANNEL", "#general")

client = WebClient(token=SLACK_BOT_TOKEN)

# ====== 取得元URL ======
BASE = "https://sbi.alpaca-tech.ai"

def build_urls():
    today = datetime.now().strftime("%Y-%m-%d")
    return {
        "今日の株式市況": f"{BASE}/{today}/morning",
        "ポジティブニュース": f"{BASE}/news/jp/{today}/morning/good/",
        "ネガティブニュース": f"{BASE}/news/jp/{today}/morning/bad/",
        "買いチャンス銘柄": f"{BASE}/trade_chance/jp/buy/{today}/morning",
        "売りチャンス銘柄": f"{BASE}/trade_chance/jp/sell/{today}/morning",
    }

def fetch_text(url):
    try:
        r = requests.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
        r.encoding = r.apparent_encoding
        return r.text.strip()
    except Exception as e:
        return f"(取得失敗: {e})"

def build_report():
    urls = build_urls()
    return {name: fetch_text(u) for name, u in urls.items()}

def post_to_slack(report: dict):
    today = datetime.now().strftime("%Y-%m-%d")
    lines = [f"*【{today} 株式市況レポート】*"]

    for section, text in report.items():
        lines.append(f"\n◆ {section}")
        lines.append(text)

    text = "\n".join(lines)
    client.chat_postMessage(channel=CHANNEL, text=text)

def main():
    report = build_report()
    post_to_slack(report)

if __name__ == "__main__":
    main()
