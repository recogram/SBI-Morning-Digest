from market_report import build_market_report
from slack_post import post_to_slack

def main():
    report = build_market_report()
    post_to_slack(report)

if __name__ == "__main__":
    main()
