"""Builds assets/header-dark.svg and assets/header-light.svg. Run: python3 scripts/make_header.py"""
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
THEMES = {
    "dark":  dict(bg="#05061a", line="#1f2a40", ink="#e8eefc", sub="#a9b6d3", cyan="#4de2ff", violet="#8b5cf6", green="#34d399", amber="#f7c873", chip="#0b1230"),
    "light": dict(bg="#f7f9ff", line="#d5dcec", ink="#0b1230", sub="#4a5675", cyan="#0a8fb0", violet="#6d3fe0", green="#0f8a5f", amber="#b7791f", chip="#ffffff"),
}
STEPS = ["request", "identity", "policy", "risk", "scope", "evidence"]
STATS = [("164", "AI governance cases", "violet"), ("46", "machine identity cases", "green"), ("210", "approval gateway checks", "cyan")]
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, monospace"

def svg(c):
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 320" width="1200" height="320" role="img" aria-labelledby="t d">',
         '  <title id="t">Roshan Trivedi</title>',
         '  <desc id="d">Privileged access and identity for 14+ years. I test whether identity and AI controls hold, in public, with the mistakes left in. 164 AI governance cases, 46 machine identity cases, 210 approval gateway checks. Each request passes six checks and ends with a person deciding.</desc>',
         f'  <rect width="1200" height="320" rx="18" fill="{c["bg"]}"/>',
         f'  <rect x="0.5" y="0.5" width="1199" height="319" rx="18" fill="none" stroke="{c["line"]}"/>',
         f'  <g font-family="{SANS}">',
         f'  <rect x="64" y="52" width="72" height="72" rx="18" fill="none" stroke="{c["cyan"]}" stroke-width="2.5"/>',
         f'  <text x="100" y="100" text-anchor="middle" font-size="30" font-weight="800" fill="{c["ink"]}" letter-spacing="1">RT</text>',
         f'  <text x="164" y="84" font-size="44" font-weight="800" fill="{c["ink"]}">Roshan Trivedi</text>',
         f'  <text x="164" y="120" font-size="21" fill="{c["sub"]}">Privileged access and identity for 14+ years. I test whether identity</text>',
         f'  <text x="164" y="148" font-size="21" fill="{c["sub"]}">and AI controls hold, in public, with the mistakes left in.</text>']
    y = 62
    for num, label, col in STATS:
        o.append(f'  <rect x="880" y="{y-22}" width="256" height="34" rx="10" fill="{c["chip"]}" stroke="{c["line"]}"/>')
        o.append(f'  <text x="896" y="{y}" font-size="18" font-weight="800" font-family="{MONO}" fill="{c[col]}">{num}</text>')
        o.append(f'  <text x="944" y="{y-1}" font-size="14" fill="{c["sub"]}">{label}</text>')
        y += 42
    xs = [120 + i * 160 for i in range(7)]
    o.append(f'  <line x1="120" y1="246" x2="1080" y2="246" stroke="{c["line"]}" stroke-width="2"/>')
    o.append(f'  <line x1="120" y1="246" x2="920" y2="246" stroke="{c["cyan"]}" stroke-width="2" stroke-opacity="0.55"/>')
    o.append(f'  <line x1="920" y1="246" x2="1080" y2="246" stroke="{c["amber"]}" stroke-width="2"/>')
    for x, s in zip(xs, STEPS):
        o.append(f'  <circle cx="{x}" cy="246" r="6" fill="{c["bg"]}" stroke="{c["cyan"]}" stroke-width="2.5"/>')
        o.append(f'  <text x="{x}" y="280" text-anchor="middle" font-size="17" fill="{c["sub"]}" font-weight="500">{s}</text>')
    x = xs[-1]
    o += [f'  <circle cx="{x}" cy="246" r="16" fill="{c["amber"]}" fill-opacity="0.18"/>',
          f'  <circle cx="{x}" cy="246" r="8" fill="{c["bg"]}" stroke="{c["amber"]}" stroke-width="2.5"/>',
          f'  <circle cx="{x}" cy="246" r="3.5" fill="{c["amber"]}"/>',
          f'  <text x="{x}" y="280" text-anchor="middle" font-size="17" fill="{c["amber"]}" font-weight="700">a person decides</text>',
          '  </g>', '</svg>', '']
    return "\n".join(o)

for name, c in THEMES.items():
    open(os.path.join(ROOT, "assets", f"header-{name}.svg"), "w").write(svg(c))
print("ok")
