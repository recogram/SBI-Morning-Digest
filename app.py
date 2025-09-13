import os, time, requests
from dotenv import load_dotenv
from parser import parse_sbi_morning
from slack_post import post_to_slack

load_dotenv()

TARGET_URL = os.getenv("TARGET_URL", "https://site1.sbisec.co.jp/ETGate/?_ControlID=WPLETmgR001Control&_PageID=WPLETmgR001Mdtl20&_DataStoreID=DSWPLETmgR001Control&_ActionID=DefaultAID&burl=iris_morningInfo&cat1=market&cat2=morningInfo&dir=tl1-minfo%7Ctl2-stmkt%7Ctl3-dcmt&file=index.html&getFlg=on")
TIMEOUT = int(os.getenv("TIMEOUT", "25"))

def fetch_page(url: str) -> str:
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, headers=headers, timeout=TIMEOUT)
    resp.raise_for_status()
    return resp.text

def main():
    html = fetch_page(TARGET_URL)
    summary = parse_sbi_morning(html)
    post_to_slack(summary, TARGET_URL)

if __name__ == "__main__":
    main()
