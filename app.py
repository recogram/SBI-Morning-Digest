import os
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from slack_sdk import WebClient

# ====== Slack設定 ======
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
CHANNEL = os.getenv("SLACK_CHANNEL", "#general")
client = WebClient(token=SLACK_BOT_TOKEN)

HEADERS = {"User-Agent": "Mozilla/5.0"}
BASE = "https://sbi.alpaca-tech.ai"

# --- 市況 ---
def fetch_market_summary(url):
    r = requests.get(url, headers=HEADERS, timeout=15)
    r.encoding = r.apparent_encoding
    soup = BeautifulSoup(r.text, "lxml")

    items = []
    for block in soup.select("div.market-condition__summary__about"):
        title = block.select_one("h5 span")
        bullets = [li.get_text(strip=True) for li in block.select("ul li span")]
        text = block.select_one("p")
        items.append({
            "title": title.get_text(strip=True) if title else "",
            "bullets": bullets,
            "text": text.get_text(" ", strip=True) if text else ""
        })
    return items

# --- ポジ/ネガ材料ニュース ---
def fetch_materials(url):
    r = requests.get(url, headers=HEADERS, timeout=15)
    r.encoding = r.apparent_encoding
    soup = BeautifulSoup(r.text, "lxml")

    news = []
    for item in soup.select("div.material__news p"):
        news.append(item.get_text(strip=True))
    return news[:5]

# --- 銘柄シグナル（買い/売りチャンス） ---
def fetch_signals(url):
    r = requests.get(url, headers=HEADERS, timeout=15)
    r.encoding = r.apparent_encoding
    soup = BeautifulSoup(r.text, "lxml")

    stocks = []
    for item in soup.select("div.signal__rankings h4"):
        stocks.append(item.get_text(strip=True))
    return stocks[:5]

# --- 全体レポート作成 ---
def build_report():
    today = datetime.now().strftime("%Y-%m-%d")
    urls = {
        "市況": f"{BASE}/{today}/morning",
        "ポジティブ": f"{BASE}/news/jp/{today}/morning/good/",
        "ネガティブ": f"{BASE}/news/jp/{today}/morning/bad/",
        "買い": f"{BASE}/trade_chance/jp/buy/{today}/morning",
        "売り": f"{BASE}/trade_chance/jp/sell/{today}/morning",
    }

    return {
        "市況": fetch_market_summary(urls["市況"]),
        "ポジティブ": fetch_materials(urls["ポジティブ"]),
        "ネガティブ": fetch_materials(urls["ネガティブ"]),
        "買い": fetch_signals(urls["買い"]),
        "売り": fetch_signals(urls["売り"]),
    }

# --- Slack投稿 ---
def post_to_slack(report: dict):
    today = datetime.now().strftime("%Y-%m-%d")
    lines = [f"*【{today} 株式市況レポート】*"]

    # 市況
    lines.append("\n◆ 今日の株式市況")
    for item in report["市況"]:
        lines.append(f"[{item['title']}]")
        for b in item["bullets"]:
            lines.append(f"- {b}")
        lines.append(f"→ {item['text']}")

    # ポジティブ
    lines.append("\n◆ ポジティブニュース")
    for n in report["ポジティブ"]:
        lines.append(f"- {n}")

    # ネガティブ
    lines.append("\n◆ ネガティブニュース")
    for n in report["ネガティブ"]:
        lines.append(f"- {n}")

    # 買い
    lines.append("\n◆ 買いチャンス銘柄")
    for s in report["買い"]:
        lines.append(f"- {s}")

    # 売り
    lines.append("\n◆ 売りチャンス銘柄")
    for s in report["売り"]:
        lines.append(f"- {s}")

    text = "\n".join(lines)
    client.chat_postMessage(channel=CHANNEL, text=text)

def main():
    report = build_report()
    post_to_slack(report)

if __name__ == "__main__":
    main()
