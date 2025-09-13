import requests
from bs4 import BeautifulSoup

KABUTAN_URL = "https://kabutan.jp/news/market/"
YAHOO_URL   = "https://finance.yahoo.co.jp/news?topic=market"

def fetch_article(url, base="https://kabutan.jp"):
    resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
    resp.encoding = resp.apparent_encoding
    soup = BeautifulSoup(resp.text, "lxml")
    body = soup.find("div", class_="news_body") or soup.find("div", class_="article_body")
    if not body:
        return None
    text = []
    for p in body.find_all("p"):
        txt = p.get_text(" ", strip=True)
        if txt:
            text.append(txt)
    return " ".join(text[:5])  # 最初の数段落を要約に使う

def fetch_kabutan_report():
    resp = requests.get(KABUTAN_URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
    resp.encoding = resp.apparent_encoding
    soup = BeautifulSoup(resp.text, "lxml")
    link = soup.select_one("div.news_list a")
    if not link:
        return None
    href = link["href"]
    if not href.startswith("http"):
        href = "https://kabutan.jp" + href
    summary = fetch_article(href)
    return {"title": "株探 市況", "summary": summary, "link": href}

def fetch_yahoo_report():
    resp = requests.get(YAHOO_URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
    resp.encoding = resp.apparent_encoding
    soup = BeautifulSoup(resp.text, "lxml")
    link = soup.select_one("a.sc-1nwfx8d-0")  # Yahooニュース本文リンク
    if not link:
        return None
    href = link["href"]
    if not href.startswith("http"):
        href = "https://finance.yahoo.co.jp" + href
    summary = fetch_article(href, base="https://finance.yahoo.co.jp")
    return {"title": "Yahoo!ファイナンス 市況", "summary": summary, "link": href}

def get_combined_market_report():
    reports = []
    kabu = fetch_kabutan_report()
    if kabu: reports.append(kabu)
    yahoo = fetch_yahoo_report()
    if yahoo: reports.append(yahoo)
    return reports
