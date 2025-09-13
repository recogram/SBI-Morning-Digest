from bs4 import BeautifulSoup
from datetime import datetime

def parse_sbi_morning(html: str) -> dict:
    soup = BeautifulSoup(html, "lxml")
    date_text = datetime.now().strftime("%Y年%m月%d日")

    sections = []
    # SBI特有の「見出し＋本文」構造を拾う
    for block in soup.select("div.mtext, div.main-text, p"):
        text = block.get_text(" ", strip=True)
        if not text:
            continue
        # 見出しっぽい部分（太字やhタグ）を分ける
        if len(text) < 30:  # 短めの文を見出しとみなす
            sections.append({"title": text, "bullets": []})
        else:
            if not sections:
                sections.append({"title": "マーケット情報", "bullets": []})
            sections[-1]["bullets"].append(text)

    # 上位数件だけに絞る
    for s in sections:
        s["bullets"] = s["bullets"][:3]

    return {"date": date_text, "sections": sections[:5]}
