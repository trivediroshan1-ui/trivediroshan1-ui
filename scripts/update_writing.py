"""Refreshes the "Latest writing" list in README.md from the site's feed.
Run: python3 scripts/update_writing.py   (standard library only)"""
import os, re, urllib.request, xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime

FEED = "https://roshantrivedi.co.in/feed.xml"
README = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "README.md")
COUNT = 5

req = urllib.request.Request(FEED, headers={"User-Agent": "profile-readme-updater"})
root = ET.fromstring(urllib.request.urlopen(req, timeout=30).read())
lines = []
for item in root.iter("item"):
    title = (item.findtext("title") or "").strip()
    link = (item.findtext("link") or "").strip()
    date = parsedate_to_datetime(item.findtext("pubDate")).strftime("%d %b %Y")
    if title and link:
        sep = "&" if "?" in link else "?"
        lines.append(f"- [{title}]({link}{sep}utm_source=github&utm_medium=profile)<br><sub>{date}</sub>")
    if len(lines) == COUNT:
        break
if not lines:
    raise SystemExit("feed had no items; README left as it was")

text = open(README, encoding="utf-8").read()
new = re.sub(r"(<!-- writing:start -->\n).*?(\n<!-- writing:end -->)",
             lambda m: m.group(1) + "\n".join(lines) + m.group(2), text, flags=re.S)
if new != text:
    open(README, "w", encoding="utf-8").write(new)
    print("README updated")
else:
    print("no change")
