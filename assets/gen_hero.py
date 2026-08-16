#!/usr/bin/env python3
"""Sinh banner Spider-Verse cho GitHub profile README.

Chay:  python3 assets/gen_hero.py
Xuat:  assets/hero.svg

Ky thuat: CSS @keyframes nam BEN TRONG file .svg -- day la thu duy nhat
GitHub khong loc bo (script/style/canvas deu bi sanitizer cat).
Kiem chung: snake.svg tren profile dung dung cach nay, 49 @keyframes, 0 <script>.
"""
import math
from pathlib import Path

W, H = 1000, 260

# Bang mau Spider-Verse: loi in an co y (halftone + chromatic aberration)
BG0, BG1 = "#0d0221", "#1b0736"
MAG, CYA, RED, WHT = "#ff1973", "#00ffe7", "#e23636", "#ffffff"

# Ban kinh phai vua trong chieu cao banner (260) thi moi doc ra hinh mang nhen.
# Truoc dung 485 -> chi thay mot lat cat, nhin nhu duong cong ngau nhien.
RADII = [36, 66, 102, 146, 198, 258]
N_STRAND = 9
SAG = 0.94          # do vong cua soi ngang, cang nho cang cong (0.87 -> phong nhu canh hoa)
R_MAX = 300


def web(a0: float, a1: float) -> tuple[list[str], list[str]]:
    """Mang nhen goc: tra ve (soi toa tron, soi ngang vong cung)."""
    angs = [math.radians(a0 + (a1 - a0) * i / (N_STRAND - 1)) for i in range(N_STRAND)]
    spokes = [f"M0 0L{R_MAX * math.cos(a):.1f} {R_MAX * math.sin(a):.1f}" for a in angs]

    rings = []
    for r in RADII:
        for a, b in zip(angs, angs[1:]):
            mid = (a + b) / 2
            rings.append(
                f"M{r * math.cos(a):.1f} {r * math.sin(a):.1f}"
                f"Q{r * SAG * math.cos(mid):.1f} {r * SAG * math.sin(mid):.1f} "
                f"{r * math.cos(b):.1f} {r * math.sin(b):.1f}"
            )
    return spokes, rings


def web_group(transform: str, delay: float) -> str:
    spokes, rings = web(2, 88)
    out = [f'<g transform="{transform}" stroke-linecap="round" fill="none">']
    for i, d in enumerate(spokes):
        out.append(
            f'<path class="w" d="{d}" pathLength="1" stroke="{CYA}" stroke-width="1.15"'
            f' opacity=".5" style="animation-delay:{delay + i * .05:.2f}s"/>'
        )
    for i, d in enumerate(rings):
        out.append(
            f'<path class="w" d="{d}" pathLength="1" stroke="{WHT}" stroke-width=".85"'
            f' opacity=".34" style="animation-delay:{delay + .3 + (i // (N_STRAND - 1)) * .12:.2f}s"/>'
        )
    out.append("</g>")
    return "".join(out)


def spider_body() -> str:
    """Chi ve con nhen, khong kem day to -- de hero va footer dung chung."""
    legs = []
    for sx in (-1, 1):
        for i, (qx, qy, ex, ey) in enumerate(
            [(12, -11, 17, -3), (14, -4, 19, 4), (14, 3, 18, 12), (12, 10, 15, 18)]
        ):
            legs.append(
                f'<path d="M{sx * 3} {-4 + i * 3}Q{sx * qx} {qy} {sx * ex} {ey}"/>'
            )
    return (
        f'<g stroke="{WHT}" stroke-width="1.6" fill="none" opacity=".9"'
        f' stroke-linecap="round">{"".join(legs)}</g>'
        f'<ellipse rx="5.5" ry="7.5" fill="{RED}"/>'
        f'<circle cy="-8.5" r="4.2" fill="{RED}"/>'
        f'<circle cx="-1.8" cy="-9.5" r="1.5" fill="{WHT}"/>'
        f'<circle cx="1.8" cy="-9.5" r="1.5" fill="{WHT}"/>'
    )


def spider(x: float, y: float) -> str:
    """Nhen treo day to, dong dua."""
    return (
        f'<g><line x1="{x}" y1="0" x2="{x}" y2="{y}" stroke="{WHT}"'
        f' stroke-width=".9" opacity=".45"/>'
        f'<g class="bob" transform="translate({x},{y})">{spider_body()}</g></g>'
    )


CSS = f"""
.w{{stroke-dasharray:1;stroke-dashoffset:1;animation:draw 1.5s ease-out forwards}}
@keyframes draw{{to{{stroke-dashoffset:0}}}}

.title{{animation:pop 1s cubic-bezier(.2,1.3,.4,1) both;animation-delay:.45s;
  transform-origin:500px 132px}}
@keyframes pop{{0%{{opacity:0;transform:scale(.82) translateY(20px)}}
  70%{{opacity:1;transform:scale(1.05) translateY(0)}}
  100%{{opacity:1;transform:scale(1) translateY(0)}}}}

.ca-m{{animation:cam 5s steps(1,end) infinite;animation-delay:1.4s}}
.ca-c{{animation:cac 5s steps(1,end) infinite;animation-delay:1.4s}}
@keyframes cam{{0%,100%{{transform:translate(-3px,0)}}17%{{transform:translate(-8px,1px)}}
  19%{{transform:translate(-2px,-1px)}}54%{{transform:translate(-6px,0)}}
  56%{{transform:translate(-3px,1px)}}}}
@keyframes cac{{0%,100%{{transform:translate(3px,0)}}17%{{transform:translate(8px,-1px)}}
  19%{{transform:translate(2px,1px)}}54%{{transform:translate(6px,0)}}
  56%{{transform:translate(3px,-1px)}}}}

.dotA{{animation:drift 14s ease-in-out infinite}}
.dotB{{animation:drift2 18s ease-in-out infinite}}
@keyframes drift{{0%,100%{{transform:translate(0,0)}}50%{{transform:translate(-14px,-9px)}}}}
@keyframes drift2{{0%,100%{{transform:translate(0,0)}}50%{{transform:translate(11px,7px)}}}}

.bob{{animation:bob 3.6s ease-in-out infinite}}
@keyframes bob{{0%,100%{{transform:translate({{X}}px,{{Y}}px)}}
  50%{{transform:translate({{X}}px,{{Y2}}px)}}}}

.sweep{{animation:sweep 7s linear infinite;animation-delay:2s}}
@keyframes sweep{{0%{{transform:translateY(-40px);opacity:0}}5%{{opacity:.5}}
  11%{{opacity:0}}100%{{transform:translateY(300px);opacity:0}}}}

.sub{{animation:fade 1s ease-out both;animation-delay:1.05s}}
.tags{{animation:fade 1s ease-out both;animation-delay:1.3s}}
.kick{{animation:fade 1s ease-out both;animation-delay:.85s}}
@keyframes fade{{from{{opacity:0;transform:translateY(9px)}}to{{opacity:1;transform:translateY(0)}}}}

@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}
  .w{{stroke-dashoffset:0}}}}
"""

SX, SY = 872, 92
CSS = CSS.replace("{X}", str(SX)).replace("{Y}", str(SY)).replace("{Y2}", str(SY + 12))

FONT = "Impact,Haettenschweiler,'Arial Narrow Bold','Franklin Gothic Bold',sans-serif"
MONO = "'SFMono-Regular',Consolas,'Liberation Mono',monospace"

svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Bui Mau Van - AI Engineer">
<title>Bui Mau Van - AI Engineer</title>
<defs>
<radialGradient id="bg" cx="50%" cy="18%" r="95%">
<stop offset="0%" stop-color="{BG1}"/><stop offset="100%" stop-color="{BG0}"/>
</radialGradient>
<pattern id="pA" width="13" height="13" patternUnits="userSpaceOnUse">
<circle cx="3" cy="3" r="2.1" fill="{MAG}"/></pattern>
<pattern id="pB" width="13" height="13" patternUnits="userSpaceOnUse">
<circle cx="9.5" cy="8" r="1.7" fill="{CYA}"/></pattern>
<radialGradient id="vig" cx="50%" cy="52%" r="62%">
<stop offset="0%" stop-color="{BG0}" stop-opacity=".82"/>
<stop offset="55%" stop-color="{BG0}" stop-opacity=".38"/>
<stop offset="100%" stop-color="{BG0}" stop-opacity="0"/></radialGradient>
<style>{CSS}</style>
</defs>

<rect width="{W}" height="{H}" fill="url(#bg)"/>

<g class="dotA" opacity=".16"><rect x="-40" y="-40" width="{W+80}" height="{H+80}" fill="url(#pA)"/></g>
<g class="dotB" opacity=".13"><rect x="-40" y="-40" width="{W+80}" height="{H+80}" fill="url(#pB)"/></g>

{web_group("translate(0,0)", 0.0)}
{web_group(f"translate({W},{H}) rotate(180)", 0.25)}

<rect width="{W}" height="{H}" fill="url(#vig)"/>

{spider(SX, SY)}

<g class="title" text-anchor="middle">
<text x="500" y="150" font-family="{FONT}" font-size="76" fill="none" stroke="{BG0}" stroke-width="13" stroke-linejoin="round" letter-spacing="3" opacity=".92">BUI MAU VAN</text>
<g class="ca-m"><text x="500" y="150" font-family="{FONT}" font-size="76" fill="{MAG}" letter-spacing="3">BUI MAU VAN</text></g>
<g class="ca-c"><text x="500" y="150" font-family="{FONT}" font-size="76" fill="{CYA}" letter-spacing="3">BUI MAU VAN</text></g>
<text x="500" y="150" font-family="{FONT}" font-size="76" fill="{WHT}" letter-spacing="3">BUI MAU VAN</text>
</g>

<text class="kick" x="500" y="72" text-anchor="middle" font-family="{MONO}" font-size="13" fill="{CYA}" letter-spacing="7" opacity=".8">PTIT &#183; HANOI &#183; VIETNAM</text>
<g class="sub" text-anchor="middle"><text x="500" y="188" font-family="{FONT}" font-size="27" fill="none" stroke="{BG0}" stroke-width="7" stroke-linejoin="round" letter-spacing="6" opacity=".92">AI ENGINEER</text><text x="500" y="188" font-family="{FONT}" font-size="27" fill="{MAG}" letter-spacing="6">AI ENGINEER</text></g>
<text class="tags" x="500" y="219" text-anchor="middle" font-family="{MONO}" font-size="12.5" fill="{WHT}" letter-spacing="3.4" opacity=".62">LLM &#183; RAG &#183; MULTI-AGENT &#183; SPEECH AI</text>

<g class="sweep"><rect width="{W}" height="2.5" fill="{CYA}" opacity=".6"/>
<rect y="2.5" width="{W}" height="1" fill="{MAG}" opacity=".45"/></g>
</svg>"""

# ---------------------------------------------------------------- footer
FH = 120
FOOTER_CSS = f"""
.w{{stroke-dasharray:1;stroke-dashoffset:1;animation:draw 1.4s ease-out forwards}}
@keyframes draw{{to{{stroke-dashoffset:0}}}}
.crawl{{animation:crawl 22s linear infinite}}
@keyframes crawl{{0%{{transform:translate(-30px,44px)}}
  100%{{transform:translate(1030px,44px)}}}}
.ft{{animation:fade 1s ease-out both;animation-delay:.6s}}
@keyframes fade{{from{{opacity:0;transform:translateY(8px)}}
  to{{opacity:1;transform:translateY(0)}}}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}
  .w{{stroke-dashoffset:0}}}}
"""

footer = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {FH}" width="{W}" height="{FH}" role="img" aria-label="Thanks for swinging by">
<title>Thanks for swinging by</title>
<defs>
<linearGradient id="fbg" x1="0" y1="0" x2="0" y2="1">
<stop offset="0%" stop-color="{BG0}"/><stop offset="100%" stop-color="{BG1}"/>
</linearGradient>
<pattern id="fp" width="13" height="13" patternUnits="userSpaceOnUse">
<circle cx="3" cy="3" r="2" fill="{MAG}"/></pattern>
<style>{FOOTER_CSS}</style>
</defs>
<rect width="{W}" height="{FH}" fill="url(#fbg)"/>
<rect width="{W}" height="{FH}" fill="url(#fp)" opacity=".12"/>
<rect width="{W}" height="2.5" fill="{MAG}"/>
<rect y="2.5" width="{W}" height="1.2" fill="{CYA}" opacity=".7"/>
{web_group(f"translate(0,{FH}) scale(.5,-.5)", 0.0)}
{web_group(f"translate({W},{FH}) scale(-.5,-.5)", 0.2)}
<line x1="0" y1="44" x2="{W}" y2="44" stroke="{WHT}" stroke-width=".9" opacity=".3"/>
<g class="crawl" transform="translate(500,44)">{spider_body()}</g>
<text class="ft" x="500" y="86" text-anchor="middle" font-family="{MONO}" font-size="12.5" fill="{CYA}" letter-spacing="5.5" opacity=".8">THANKS FOR SWINGING BY</text>
<text class="ft" x="500" y="106" text-anchor="middle" font-family="{MONO}" font-size="10.5" fill="{WHT}" letter-spacing="2.6" opacity=".38">WITH GREAT COMPUTE COMES GREAT RESPONSIBILITY</text>
</svg>"""

for name, doc in (("hero.svg", svg), ("footer.svg", footer)):
    p = Path(__file__).with_name(name)
    p.write_text(doc, encoding="utf-8")
    print(f"{p.name:12} {len(doc):>7,} bytes")


def _check() -> None:
    """ponytail: kiem tra toi thieu -- SVG hop le va khong dinh thu GitHub loc."""
    import xml.etree.ElementTree as ET

    per_web = N_STRAND + len(RADII) * (N_STRAND - 1)
    for name, doc in (("hero", svg), ("footer", footer)):
        ET.fromstring(doc)                                # parse duoc = XML hop le
        assert "<script" not in doc, f"{name}: GitHub se loc bo <script>"
        assert "@keyframes" in doc, f"{name}: mat animation"
        assert doc.count('class="w"') == 2 * per_web, f"{name}: thieu soi to"
    print("check: OK")


if __name__ == "__main__":
    _check()
