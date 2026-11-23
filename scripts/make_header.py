"""Builds assets/header-dark.svg and assets/header-light.svg. Run: python3 scripts/make_header.py"""
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
THEMES = {
    "dark":  dict(bg="#05061a", line="#1f2a40", ink="#e8eefc", sub="#a9b6d3", cyan="#4de2ff", violet="#8b5cf6", green="#34d399", amber="#f7c873", chip="#0b1230"),
    "light": dict(bg="#f7f9ff", line="#d5dcec", ink="#0b1230", sub="#4a5675", cyan="#0a8fb0", violet="#6d3fe0", green="#0f8a5f", amber="#b7791f", chip="#ffffff"),
}
STEPS = ["request", "identity", "policy", "risk", "scope", "evidence"]
STATS = [("130", "sign-in and MFA cases", "amber"), ("164", "AI governance cases", "violet"), ("67", "machine identity cases", "green"), ("210", "approval gateway checks", "cyan")]
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, monospace"

def svg(c):
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 320" width="1200" height="320" role="img" aria-labelledby="t d">',
         '  <title id="t">Roshan Trivedi</title>',
         '  <desc id="d">Privileged access and identity for 14+ years. I test whether identity and AI controls hold, in public, with the mistakes left in. 130 sign-in and MFA cases, 164 AI governance cases, 67 machine identity cases, 210 approval gateway checks. Each request passes six checks and ends with a person deciding.</desc>',
         ('  <style>'
          '.pkt{offset-path:path("M120 246 H1080");offset-rotate:0deg;animation:pkt 4.2s cubic-bezier(.45,0,.3,1) .6s 3 both}'
          '@keyframes pkt{0%{offset-distance:0%;opacity:0}6%{opacity:1}88%{offset-distance:100%;opacity:1}100%{offset-distance:100%;opacity:0}}'
          '.st{animation:st 4.2s ease-out 3 both}'
          '@keyframes st{0%,4%{stroke-width:2.5;r:6}10%{stroke-width:4;r:8}22%,100%{stroke-width:2.5;r:6}}'
          '.pd{transform-box:fill-box;transform-origin:center;animation:pd 4.2s ease-out .6s 3 both}'
          '@keyframes pd{0%,84%{transform:scale(1);opacity:.18}92%{transform:scale(1.9);opacity:.38}100%{transform:scale(1);opacity:.18}}'
          '.chip{animation:chip .6s ease-out both}'
          '@keyframes chip{from{opacity:0;transform:translateX(12px)}}'
          '@media (prefers-reduced-motion: reduce){.pkt{display:none}.st,.pd,.chip{animation:none}}'
          '</style>'),
         f'  <rect width="1200" height="320" rx="18" fill="{c["bg"]}"/>',
         f'  <rect x="0.5" y="0.5" width="1199" height="319" rx="18" fill="none" stroke="{c["line"]}"/>',
         f'  <g font-family="{SANS}">',
         f'  <rect x="64" y="52" width="72" height="72" rx="18" fill="none" stroke="{c["cyan"]}" stroke-width="2.5"/>',
         f'  <text x="100" y="100" text-anchor="middle" font-size="30" font-weight="800" fill="{c["ink"]}" letter-spacing="1">RT</text>',
         f'  <text x="164" y="84" font-size="44" font-weight="800" fill="{c["ink"]}">Roshan Trivedi</text>',
         f'  <text x="164" y="120" font-size="21" fill="{c["sub"]}">Privileged access and identity for 14+ years. I test whether identity</text>',
         f'  <text x="164" y="148" font-size="21" fill="{c["sub"]}">and AI controls hold, in public, with the mistakes left in.</text>']
    y = 56
    for num, label, col in STATS:
        o.append(f'  <g class="chip" style="animation-delay:{0.15 + 0.12 * (y // 38)}s">')
        o.append(f'  <rect x="880" y="{y-22}" width="256" height="34" rx="10" fill="{c["chip"]}" stroke="{c["line"]}"/>')
        o.append(f'  <text x="896" y="{y}" font-size="18" font-weight="800" font-family="{MONO}" fill="{c[col]}">{num}</text>')
        o.append(f'  <text x="944" y="{y-1}" font-size="14" fill="{c["sub"]}">{label}</text>')
        o.append('  </g>')
        y += 38
    xs = [120 + i * 160 for i in range(7)]
    o.append(f'  <line x1="120" y1="246" x2="1080" y2="246" stroke="{c["line"]}" stroke-width="2"/>')
    o.append(f'  <line x1="120" y1="246" x2="920" y2="246" stroke="{c["cyan"]}" stroke-width="2" stroke-opacity="0.55"/>')
    o.append(f'  <line x1="920" y1="246" x2="1080" y2="246" stroke="{c["amber"]}" stroke-width="2"/>')
    for i, (x, s) in enumerate(zip(xs, STEPS)):
        # each check lights as the request dot reaches it (the dot crosses the rail in about 3.7s)
        o.append(f'  <circle class="st" style="animation-delay:{0.6 + 3.7 * (x - 120) / 960:.2f}s" cx="{x}" cy="246" r="6" fill="{c["bg"]}" stroke="{c["cyan"]}" stroke-width="2.5"/>')
        o.append(f'  <text x="{x}" y="280" text-anchor="middle" font-size="17" fill="{c["sub"]}" font-weight="500">{s}</text>')
    x = xs[-1]
    o += [f'  <circle class="pd" cx="{x}" cy="246" r="16" fill="{c["amber"]}" fill-opacity="0.18"/>',
          f'  <circle cx="{x}" cy="246" r="8" fill="{c["bg"]}" stroke="{c["amber"]}" stroke-width="2.5"/>',
          f'  <circle cx="{x}" cy="246" r="3.5" fill="{c["amber"]}"/>',
          f'  <text x="{x}" y="280" text-anchor="middle" font-size="17" fill="{c["amber"]}" font-weight="700">a person decides</text>',
          f'  <circle class="pkt" cx="0" cy="0" r="5.5" fill="{c["cyan"]}"/>',
          '  </g>', '</svg>', '']
    return "\n".join(o)

for name, c in THEMES.items():
    open(os.path.join(ROOT, "assets", f"header-{name}.svg"), "w").write(svg(c))
print("ok")
