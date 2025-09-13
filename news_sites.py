import requests
from bs4 import BeautifulSoup

NEWS_SOURCES = {
    "株探 市況": "https://kabutan.jp/news/market/",
    "Yahoo!ファイナンス 市況": "https://finance.yahoo.co.jp/news?topic=market"
}

def fetch_and_summarize(name, url, limit=1):
    """
    各サイトから記事を取得し、見出し＋要約＋リンクを返す
    """
    try:
        resp = requests.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
        resp.encoding = resp.apparent_encoding
        soup = BeautifulSoup(resp.text, "lxml")

        # 記事リンク候補
        articles = []
        for a in soup.find_all("a", href=True, limit=5):
            text = a.get_text(strip=True)
            href = a["href"]
            if not text or len(text) < 8:
                continue
            if not href.startswith("http"):
                href = url.rstrip("/") + href
            articles.append((text, href))
        if not articles:
            return []

        results = []
        for title, link in articles[:limit]:
            # リンク先記事本文を軽く取得
            body = ""
            try:
                art_resp = requests.get(link, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
                art_resp.encoding = art_resp.apparent_encoding
                art_soup = BeautifulSoup(art_resp.text, "lxml")
                article = art_soup.find("div", class_="news_body") or art_soup.find("div", class_="article_body")
                if article:
                    paragraphs = [p.get_text(" ", strip=True) for p in article.find_all("p")][:2]
                    body = " ".join(paragraphs)
            except:
                pass
            summary_text = f"*{title}*\n{body}\n<{link}|記事を読む>"
            results.append(summary_text)
        return results
    except Exception as e:
        return [f"(取得失敗: {e})"]

def get_market_summaries():
    all_summaries = []
    for name, url in NEWS_SOURCES.items():
        all_summaries.extend(fetch_and_summarize(name, url, limit=2))  # 各サイトから2件
    return all_summaries[:5]  # 全体で最大5件
