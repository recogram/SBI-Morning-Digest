import requests
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0"}

def fetch_article(url, selector):
    """記事本文を取得"""
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        r.encoding = r.apparent_encoding
        soup = BeautifulSoup(r.text, "lxml")
        body = soup.select_one(selector)
        if not body:
            return []
        paras = [p.get_text(" ", strip=True) for p in body.find_all("p") if p.get_text(strip=True)]
        return paras
    except Exception as e:
        return [f"(取得失敗: {e})"]

# --- 株探 ---
KABUTAN_URL = "https://kabutan.jp/news/market/"

def fetch_kabutan():
    r = requests.get(KABUTAN_URL, headers=HEADERS, timeout=15)
    r.encoding = r.apparent_encoding
    soup = BeautifulSoup(r.text, "lxml")
    link = soup.select_one("div.news_list a")
    if not link: 
        return {}
    href = link["href"]
    if not href.startswith("http"):
        href = "https://kabutan.jp" + href
    paras = fetch_article(href, "div.news_body")
    return {
        "今日の株式市況": " ".join(paras[0:4]),
        "業種・個別株動向": " ".join(paras[4:8]),
        "新興株・IPO": " ".join(paras[8:12]),
        "link": href
    }

# --- Yahooファイナンス ---
YAHOO_URL = "https://finance.yahoo.co.jp/news?topic=market"

def fetch_yahoo():
    r = requests.get(YAHOO_URL, headers=HEADERS, timeout=15)
    r.encoding = r.apparent_encoding
    soup = BeautifulSoup(r.text, "lxml")
    link = soup.select_one("a.sc-1nwfx8d-0")
    if not link: 
        return {}
    href = link["href"]
    if not href.startswith("http"):
        href = "https://finance.yahoo.co.jp" + href
    paras = fetch_article(href, "div.article_body")
    return {"前日の米国市場": " ".join(paras[0:4]), "link": href}

# --- ロイター ---
REUTERS_URL = "https://jp.reuters.com/markets/japan/"

def fetch_reuters():
    r = requests.get(REUTERS_URL, headers=HEADERS, timeout=15)
    r.encoding = r.apparent_encoding
    soup = BeautifulSoup(r.text, "lxml")
    link = soup.select_one("a[href*='/article/']")
    if not link: 
        return {}
    href = link["href"]
    if not href.startswith("http"):
        href = "https://jp.reuters.com" + href
    paras = fetch_article(href, "div.article-body__content")
    return {"補足": " ".join(paras[0:3]), "link": href}

def build_market_report():
    kabu = fetch_kabutan()
    yahoo = fetch_yahoo()
    reuters = fetch_reuters()

    report = {}
    if kabu:
        report.update({k: v for k, v in kabu.items() if k != "link"})
        report["株探リンク"] = kabu.get("link")
    if yahoo:
        report.update({k: v for k, v in yahoo.items() if k != "link"})
        report["Yahooリンク"] = yahoo.get("link")
    if reuters:
        report["ロイター補足"] = reuters.get("補足")
        report["ロイターリンク"] = reuters.get("link")

    # TODO: 個別株材料ニュース（株探ニュース等から追加）

    return report
