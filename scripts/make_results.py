"""Builds assets/results-dark.svg and assets/results-light.svg: one mark per lab case.

Short green mark: the result matched the guess I wrote down first. Tall red mark: the guess was wrong.
Hollow mark: the case was not run. The marks differ in height as well as colour, so the figure reads
without colour too. Data: the site's case catalogue.

Run: python3 scripts/make_results.py                     (reads the live catalogue)
     python3 scripts/make_results.py path/to/catalogue.json
"""
import json, os, sys, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = "https://roshantrivedi.co.in/data/catalogue.json"
if len(sys.argv) > 1:
    cat = json.load(open(sys.argv[1], encoding="utf-8"))
else:
    req = urllib.request.Request(URL, headers={"User-Agent": "profile-readme-updater"})
    cat = json.loads(urllib.request.urlopen(req, timeout=30).read())

THEMES = {
    "dark":  dict(bg="#05061a", line="#1f2a40", ink="#e8eefc", sub="#a9b6d3", ok="#34d399", bad="#fb7185", off="#8393aa"),
    "light": dict(bg="#f7f9ff", line="#d5dcec", ink="#0b1230", sub="#4a5675", ok="#047857", bad="#be123c", off="#5b6a80"),
}
LABS = [("ca", "Sign-in and MFA"), ("nhi", "Machine identity"), ("agl", "AI governance")]
KIND = {"As guessed": "ok", "Guess was wrong": "bad", "Not run here": "off"}
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, monospace"
W, H = 1200, 270
X0, X1 = 230, 940          # where the marks run
SHORT, TALL = 12, 30


def rows():
    out = []
    for lab, name in LABS:
        kinds = [KIND[c["guess"]] for c in cat["cases"] if c["lab"] == lab]
        out.append((name, kinds))
    return out


def svg(c):
    data = rows()
    total = sum(len(k) for _, k in data)
    wrong = sum(k.count("bad") for _, k in data)
    desc = "; ".join(f"{n}: {len(k)} cases, {k.count('bad')} guesses wrong" for n, k in data)
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t d">',
         f'  <title id="t">Every lab case, and where my guess was wrong</title>',
         f'  <desc id="d">One mark per case, {total} in all, {wrong} wrong guesses. {desc}.</desc>',
         f'  <rect width="{W}" height="{H}" rx="18" fill="{c["bg"]}"/>',
         f'  <rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="18" fill="none" stroke="{c["line"]}"/>',
         f'  <g font-family="{SANS}">',
         f'  <text x="48" y="52" font-size="20" font-weight="700" fill="{c["ink"]}">Every case, and where my guess was wrong</text>']
    y = 104
    for name, kinds in data:
        pitch = (X1 - X0) / len(kinds)
        w = max(1.2, min(4, pitch * 0.62))
        o.append(f'  <text x="48" y="{y}" font-size="17" fill="{c["sub"]}">{name}</text>')
        for i, k in enumerate(kinds):
            x = X0 + i * pitch
            if k == "bad":
                o.append(f'  <rect x="{x:.1f}" y="{y - TALL + 4}" width="{w:.1f}" height="{TALL}" rx="1" fill="{c["bad"]}"/>')
            elif k == "ok":
                o.append(f'  <rect x="{x:.1f}" y="{y - SHORT + 4}" width="{w:.1f}" height="{SHORT}" rx="1" fill="{c["ok"]}"/>')
            else:
                o.append(f'  <rect x="{x + .4:.1f}" y="{y - SHORT + 4.4}" width="{max(.8, w - .8):.1f}" height="{SHORT - .8}" rx="1" fill="none" stroke="{c["off"]}" stroke-width=".8"/>')
        o.append(f'  <text x="{W - 48}" y="{y}" text-anchor="end" font-size="15" font-family="{MONO}" fill="{c["sub"]}">{len(kinds)} cases · {kinds.count("bad")} wrong</text>')
        y += 46
    ly = H - 26
    o += [f'  <rect x="48" y="{ly - 10}" width="4" height="{SHORT}" rx="1" fill="{c["ok"]}"/>',
          f'  <text x="60" y="{ly}" font-size="14" fill="{c["sub"]}">matched the guess written first</text>',
          f'  <rect x="300" y="{ly - 18}" width="4" height="20" rx="1" fill="{c["bad"]}"/>',
          f'  <text x="312" y="{ly}" font-size="14" fill="{c["sub"]}">guess was wrong</text>',
          f'  <rect x="460" y="{ly - 10}" width="4" height="{SHORT - 1}" rx="1" fill="none" stroke="{c["off"]}" stroke-width=".8"/>',
          f'  <text x="472" y="{ly}" font-size="14" fill="{c["sub"]}">not run</text>',
          '  </g>', '</svg>']
    return "\n".join(o) + "\n"


for name, c in THEMES.items():
    path = os.path.join(ROOT, "assets", f"results-{name}.svg")
    open(path, "w", encoding="utf-8").write(svg(c))
    print("wrote", os.path.relpath(path, ROOT))
