from bs4 import BeautifulSoup
from datetime import datetime

def parse_sbi_morning(html: str) -> dict:
    soup = BeautifulSoup(html, "lxml")
    date_text = datetime.now().strftime("%Y年%m月%d日")

    sections = []
    for h in soup.find_all(["h1", "h2", "h3"]):
        title = h.get_text(" ", strip=True)
        if not title:
            continue
        body_lines = []
        for sib in h.find_all_next(limit=10):
            if sib.name in ["h1", "h2", "h3"]:
                break
            if sib.name in ["p", "li"]:
                txt = sib.get_text(" ", strip=True)
                if txt:
                    body_lines.append(txt)
        if body_lines:
            sections.append({"title": title, "bullets": body_lines[:3]})
        if len(sections) >= 5:
            break

    return {"date": date_text, "sections": sections}
