#!/usr/bin/env python3
import re
import sys
from pathlib import Path
import requests
from bs4 import BeautifulSoup

USERNAME = "snehasachdeva10"
PROFILE_URL = f"https://www.hackerrank.com/{USERNAME}"

def fetch_profile(url):
    headers = {
        "User-Agent": "github-action-hackerrank-readme-updater/1.0"
    }
    resp = requests.get(url, headers=headers, timeout=20)
    resp.raise_for_status()
    return resp.text

def extract_numbers(text):
    solved = None
    rank = None
    badges = None

    # Search for “solved” / “problems solved”
    solved_match = re.search(r'(\d[\d,]*)\s+(?:problems?\s+)?solv', text, re.I)
    if solved_match:
        solved = solved_match.group(1).replace(",", "")

    # Search for “Rank” or “Ranking”
    rank_match = re.search(r'(?:Rank(?:ing)?[:\s#]*)(\d[\d,]*)', text, re.I)
    if rank_match:
        rank = rank_match.group(1).replace(",", "")

    # Search for “badges”
    badges_match = re.search(r'(\d+)\s+badg', text, re.I)
    if badges_match:
        badges = badges_match.group(1)

    return solved or "0", rank or "N/A", badges or "0"

def parse_profile_html(html):
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(" ", strip=True)
    solved, rank, badges = extract_numbers(text)
    return solved, rank, badges

def update_readme(template_path, out_path, username, solved, rank, badges):
    tpl = Path(template_path).read_text(encoding="utf-8")
    content = tpl.replace("{{HR_USERNAME}}", username)
    content = content.replace("{{HR_SOLVED}}", str(solved))
    content = content.replace("{{HR_RANK}}", str(rank))
    content = content.replace("{{HR_BADGES}}", str(badges))
    Path(out_path).write_text(content, encoding="utf-8")
    print(f"Wrote {out_path}")

def main():
    if len(sys.argv) > 1:
        # Optionally override username from CLI
        global USERNAME, PROFILE_URL
        USERNAME = sys.argv[1]
        PROFILE_URL = f"https://www.hackerrank.com/{USERNAME}"

    print("Fetching", PROFILE_URL)
    html = fetch_profile(PROFILE_URL)
    solved, rank, badges = parse_profile_html(html)
    print("Parsed values → Solved:", solved, "Rank:", rank, "Badges:", badges)
    update_readme("README.md.template", "README.md", USERNAME, solved, rank, badges)

if __name__ == "__main__":
    main()
