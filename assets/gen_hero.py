#!/usr/bin/env python3
"""Sinh toan bo asset SVG cho GitHub profile README.

Chay:  python3 assets/gen_hero.py
Xuat:  hero.svg  footer.svg  thread.svg

Ky thuat: CSS @keyframes nam BEN TRONG file .svg -- day la thu duy nhat
GitHub khong loc bo (script/style/canvas deu bi sanitizer cat).
Kiem chung: snake.svg tren profile dung dung cach nay, 49 @keyframes, 0 <script>.
"""
import math
from pathlib import Path

W, H = 1000, 260

# ── Bang mau suit Spider-Man co dien (user chon) ──────────────────────────
RED = "#df1f2d"     # do chinh
RED_D = "#b11313"   # do dam - vien, ke mang
BLU_D = "#2b3784"   # xanh dam
BLU_L = "#447bbe"   # xanh nhat
WHT = "#ffffff"
# Nen suy ra tu BLU_D giam sang, de giu nguyen ho mau
BG0, BG1 = "#0a0e22", "#131a44"

RADII = [36, 66, 102, 146, 198, 258]
N_STRAND = 9
SAG = 0.94          # do vong cua soi ngang, cang nho cang cong
R_MAX = 300

FONT = "Impact,Haettenschweiler,'Arial Narrow Bold','Franklin Gothic Bold',sans-serif"
MONO = "'SFMono-Regular',Consolas,'Liberation Mono',monospace"


# ── Mang nhen ─────────────────────────────────────────────────────────────
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
            f'<path class="w" d="{d}" pathLength="1" stroke="{BLU_L}" stroke-width="1.2"'
            f' opacity=".55" style="animation-delay:{delay + i * .05:.2f}s"/>'
        )
    for i, d in enumerate(rings):
        out.append(
            f'<path class="w" d="{d}" pathLength="1" stroke="{WHT}" stroke-width=".85"'
            f' opacity=".3" style="animation-delay:{delay + .3 + (i // (N_STRAND - 1)) * .12:.2f}s"/>'
        )
    out.append("</g>")
    return "".join(out)


# ── Con nhen: dung dang bieu tuong nguc Spider-Man, khong phai nhen hoat hinh ──
def spider_body(scale: float = 1.0, col: str = RED, shade: str = RED_D) -> str:
    """Nhen kieu emblem: chan dai, gap goc nhon, than thon -- doc ra ngay."""
    legs = []
    # (y goc chan, y dau goi, x dau goi, x mut, y mut)
    joints = [
        (-7.0, -25.0, 12.0, 25.0, -14.0),
        (-3.0, -19.0, 15.0, 30.0, -3.0),
        (1.5, -10.0, 16.0, 30.0, 10.0),
        (5.5, -1.0, 14.0, 24.0, 22.0),
    ]
    for sx in (-1, 1):
        for y0, ky, kx, ex, ey in joints:
            legs.append(
                f'<path d="M{sx * 2.5} {y0}'
                f'Q{sx * kx * .55:.1f} {ky:.1f} {sx * kx:.1f} {ky + 3:.1f}'
                f'Q{sx * (kx + ex) / 2:.1f} {(ky + ey) / 2 + 3:.1f} {sx * ex:.1f} {ey:.1f}"/>'
            )
    return (
        f'<g transform="scale({scale})">'
        f'<g stroke="{col}" stroke-width="2.6" fill="none" stroke-linecap="round"'
        f' stroke-linejoin="round">{"".join(legs)}</g>'
        # than: dau tron + nguc + bung thon nhon
        f'<circle cy="-11" r="4.4" fill="{col}"/>'
        f'<ellipse cy="-4" rx="5.4" ry="6" fill="{col}"/>'
        f'<path d="M0 1C4.6 1 6.4 7 6.4 12C6.4 18 3.4 24 0 24C-3.4 24 -6.4 18 -6.4 12C-6.4 7 -4.6 1 0 1Z" fill="{col}"/>'
        f'<path d="M0 3C2.2 6 2.4 15 0 21C-2.4 15 -2.2 6 0 3Z" fill="{shade}" opacity=".55"/>'
        f"</g>"
    )


def spider_hanging(x: float, y: float) -> str:
    return (
        f'<g><line x1="{x}" y1="0" x2="{x}" y2="{y}" stroke="{WHT}"'
        f' stroke-width="1" opacity=".5"/>'
        f'<g class="bob" transform="translate({x},{y})">{spider_body(.95)}</g></g>'
    )


# ── HERO ──────────────────────────────────────────────────────────────────
SX, SY = 876, 74
HERO_CSS = f"""
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

.bob{{animation:bob 4.2s ease-in-out infinite}}
@keyframes bob{{0%,100%{{transform:translate({SX}px,{SY}px)}}
  50%{{transform:translate({SX}px,{SY + 16}px)}}}}

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

hero = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Bui Mau Van - AI Engineer">
<title>Bui Mau Van - AI Engineer</title>
<defs>
<radialGradient id="bg" cx="50%" cy="18%" r="95%">
<stop offset="0%" stop-color="{BG1}"/><stop offset="100%" stop-color="{BG0}"/>
</radialGradient>
<pattern id="pA" width="13" height="13" patternUnits="userSpaceOnUse">
<circle cx="3" cy="3" r="2.1" fill="{RED}"/></pattern>
<pattern id="pB" width="13" height="13" patternUnits="userSpaceOnUse">
<circle cx="9.5" cy="8" r="1.7" fill="{BLU_L}"/></pattern>
<radialGradient id="vig" cx="50%" cy="52%" r="62%">
<stop offset="0%" stop-color="{BG0}" stop-opacity=".84"/>
<stop offset="55%" stop-color="{BG0}" stop-opacity=".4"/>
<stop offset="100%" stop-color="{BG0}" stop-opacity="0"/></radialGradient>
<style>{HERO_CSS}</style>
</defs>

<rect width="{W}" height="{H}" fill="url(#bg)"/>
<g class="dotA" opacity=".17"><rect x="-40" y="-40" width="{W+80}" height="{H+80}" fill="url(#pA)"/></g>
<g class="dotB" opacity=".15"><rect x="-40" y="-40" width="{W+80}" height="{H+80}" fill="url(#pB)"/></g>

{web_group("translate(0,0)", 0.0)}
{web_group(f"translate({W},{H}) rotate(180)", 0.25)}

<rect width="{W}" height="{H}" fill="url(#vig)"/>
{spider_hanging(SX, SY)}

<g class="title" text-anchor="middle">
<text x="500" y="150" font-family="{FONT}" font-size="76" fill="none" stroke="{BG0}" stroke-width="13" stroke-linejoin="round" letter-spacing="3" opacity=".92">BUI MAU VAN</text>
<g class="ca-m"><text x="500" y="150" font-family="{FONT}" font-size="76" fill="{RED}" letter-spacing="3">BUI MAU VAN</text></g>
<g class="ca-c"><text x="500" y="150" font-family="{FONT}" font-size="76" fill="{BLU_L}" letter-spacing="3">BUI MAU VAN</text></g>
<text x="500" y="150" font-family="{FONT}" font-size="76" fill="{WHT}" letter-spacing="3">BUI MAU VAN</text>
</g>

<text class="kick" x="500" y="72" text-anchor="middle" font-family="{MONO}" font-size="13" fill="{BLU_L}" letter-spacing="7" opacity=".9">PTIT &#183; HANOI &#183; VIETNAM</text>
<g class="sub" text-anchor="middle"><text x="500" y="188" font-family="{FONT}" font-size="27" fill="none" stroke="{BG0}" stroke-width="7" stroke-linejoin="round" letter-spacing="6" opacity=".92">AI ENGINEER</text><text x="500" y="188" font-family="{FONT}" font-size="27" fill="{RED}" letter-spacing="6">AI ENGINEER</text></g>
<text class="tags" x="500" y="219" text-anchor="middle" font-family="{MONO}" font-size="12.5" fill="{WHT}" letter-spacing="3.4" opacity=".62">LLM &#183; RAG &#183; MULTI-AGENT &#183; SPEECH AI</text>

<g class="sweep"><rect width="{W}" height="2.5" fill="{RED}" opacity=".65"/>
<rect y="2.5" width="{W}" height="1" fill="{BLU_L}" opacity=".5"/></g>
</svg>"""


# ── THREAD: to nhen doc, dung lam vach ngan giua cac muc ──────────────────
# Ban dau ve luon song + hat do to -> user che "nhu soi day". To nhen that la
# soi CANG THANG, manh nhu toc. Sua: thang, 1px, mo dan hai dau, bo hat.
TW, TH = 40, 96
THREAD_CSS = """
.t{stroke-dasharray:1;stroke-dashoffset:1;animation:draw 1.3s ease-out forwards}
@keyframes draw{to{stroke-dashoffset:0}}
.dew{animation:dfade .5s ease-out both;animation-delay:1s}
@keyframes dfade{from{opacity:0}}
@media (prefers-reduced-motion:reduce){*{animation:none!important}
  .t{stroke-dashoffset:0}}
"""
# Mot not duy nhat. Ba hat xau chuoi lai doc ra thanh "chuoi vong", khong phai to nhen.
_dew = f'<circle class="dew" cx="20" cy="{TH // 2}" r=".8" fill="{BLU_L}" opacity=".5"/>'
thread = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {TW} {TH}" width="{TW}" height="{TH}" role="img" aria-label="">
<defs>
<linearGradient id="tg" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="0" y2="{TH}">
<stop offset="0%" stop-color="{BLU_L}" stop-opacity="0"/>
<stop offset="22%" stop-color="{BLU_L}" stop-opacity=".6"/>
<stop offset="78%" stop-color="{BLU_L}" stop-opacity=".6"/>
<stop offset="100%" stop-color="{BLU_L}" stop-opacity="0"/></linearGradient>
<style>{THREAD_CSS}</style></defs>
<line class="t" pathLength="1" x1="20" y1="0" x2="20" y2="{TH}" stroke="url(#tg)" stroke-width="1"/>
{_dew}
</svg>"""


# ── FOOTER ────────────────────────────────────────────────────────────────
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
<circle cx="3" cy="3" r="2" fill="{RED}"/></pattern>
<style>{FOOTER_CSS}</style>
</defs>
<rect width="{W}" height="{FH}" fill="url(#fbg)"/>
<rect width="{W}" height="{FH}" fill="url(#fp)" opacity=".1"/>
<rect width="{W}" height="2.5" fill="{RED}"/>
<rect y="2.5" width="{W}" height="1.2" fill="{BLU_L}" opacity=".8"/>
{web_group(f"translate(0,{FH}) scale(.5,-.5)", 0.0)}
{web_group(f"translate({W},{FH}) scale(-.5,-.5)", 0.2)}
<line x1="0" y1="44" x2="{W}" y2="44" stroke="{WHT}" stroke-width=".9" opacity=".3"/>
<g class="crawl" transform="translate(500,44)">{spider_body(.8)}</g>
<text class="ft" x="500" y="86" text-anchor="middle" font-family="{MONO}" font-size="12.5" fill="{BLU_L}" letter-spacing="5.5" opacity=".9">THANKS FOR SWINGING BY</text>
<text class="ft" x="500" y="106" text-anchor="middle" font-family="{MONO}" font-size="10.5" fill="{WHT}" letter-spacing="2.6" opacity=".38">WITH GREAT COMPUTE COMES GREAT RESPONSIBILITY</text>
</svg>"""


FILES = {"hero.svg": hero, "footer.svg": footer, "thread.svg": thread}

for name, doc in FILES.items():
    p = Path(__file__).with_name(name)
    p.write_text(doc, encoding="utf-8")
    print(f"{name:13} {len(doc):>7,} bytes")


def _check() -> None:
    """ponytail: kiem tra toi thieu -- SVG hop le va khong dinh thu GitHub loc."""
    import xml.etree.ElementTree as ET

    per_web = N_STRAND + len(RADII) * (N_STRAND - 1)
    for name, doc in FILES.items():
        ET.fromstring(doc)                                # parse duoc = XML hop le
        assert "<script" not in doc, f"{name}: GitHub se loc bo <script>"
        assert "@keyframes" in doc, f"{name}: mat animation"
        assert "prefers-reduced-motion" in doc, f"{name}: thieu guard reduced-motion"
    for name in ("hero.svg", "footer.svg"):
        assert FILES[name].count('class="w"') == 2 * per_web, f"{name}: thieu soi to"
    print("check: OK")


if __name__ == "__main__":
    _check()
