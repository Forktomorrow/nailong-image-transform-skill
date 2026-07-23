#!/usr/bin/env python3
"""Create fast, model-free SVG previews from existing Nailong assets.

This is deliberately geometric: it demonstrates placement, scale, rotation,
and clipping without claiming to repaint the source image.
"""
from __future__ import annotations
import base64
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs/assets/procedural"
ASSET = ROOT / "docs/assets/nailong-ui"
OUT.mkdir(parents=True, exist_ok=True)

def data_uri(path: Path) -> str:
    mime = "image/webp" if path.suffix == ".webp" else "image/png"
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode()

stand = data_uri(ASSET / "stand.png")
leap = data_uri(ASSET / "leap.png")
shy = data_uri(ASSET / "shy.png")
board = data_uri(ASSET / "reference-board.webp")

def write(name: str, body: str, w=1200, h=800):
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
<rect width="100%" height="100%" fill="#fff9df"/>{body}</svg>'''
    (OUT / name).write_text(svg)

write("path-fit.svg", f'''<rect x="38" y="38" width="1124" height="724" rx="36" fill="#17202b"/>
<path d="M180 610 C230 180 420 160 515 430 S790 690 840 300 S1020 150 1080 220" fill="none" stroke="#254051" stroke-width="140" stroke-linecap="round"/>
<path d="M180 610 C230 180 420 160 515 430 S790 690 840 300 S1020 150 1080 220" fill="none" stroke="#f3c94b" stroke-width="112" stroke-linecap="round"/>
<image href="{leap}" x="120" y="510" width="180" height="205" transform="rotate(-38 210 610)"/>
<image href="{stand}" x="400" y="265" width="155" height="165" transform="rotate(18 478 347)"/>
<image href="{shy}" x="720" y="520" width="150" height="160" transform="rotate(-28 795 600)"/>
<image href="{stand}" x="950" y="125" width="145" height="155" transform="rotate(35 1022 202)"/>
<text x="70" y="110" fill="#fff9df" font-family="sans-serif" font-size="30">程序拟合 · 长路径 / 大中小多尺度</text>''')

write("irregular-fit.svg", f'''<rect x="42" y="42" width="1116" height="716" rx="34" fill="#d8edf0"/>
<path d="M180 600 L240 210 L470 150 L610 260 L820 180 L1020 350 L910 640 L620 690 L430 560 Z" fill="#79aeb2" opacity=".75"/>
<path d="M280 560 C255 430 285 300 420 245 C530 200 610 300 700 260 C820 205 940 310 900 450 C870 570 730 590 620 520 C500 445 390 660 280 560Z" fill="#f4c94e" stroke="#6d4b1f" stroke-width="8"/>
<image href="{stand}" x="310" y="250" width="170" height="180" transform="rotate(-18 395 340)"/>
<image href="{shy}" x="520" y="420" width="130" height="140" transform="rotate(28 585 490)"/>
<image href="{leap}" x="730" y="280" width="160" height="180" transform="rotate(30 810 370)"/>
<text x="75" y="105" fill="#17383d" font-family="sans-serif" font-size="30">程序拟合 · 不规则轮廓 / 残余区域递归填充</text>''')

write("ui-fit.svg", f'''<rect x="50" y="50" width="1100" height="700" rx="32" fill="#f7f2e8" stroke="#1d2429" stroke-width="4"/>
<rect x="90" y="145" width="1015" height="2" fill="#d5cdbd"/>
<text x="90" y="110" fill="#1d2429" font-family="sans-serif" font-size="36" font-weight="700">奶龙化控件 · 无模型快速预览</text>
<rect x="110" y="210" width="350" height="350" rx="28" fill="#ffe071"/>
<image href="{board}" x="145" y="245" width="280" height="280" preserveAspectRatio="xMidYMid meet"/>
<rect x="540" y="235" width="450" height="86" rx="43" fill="#f2c94c"/>
<image href="{stand}" x="700" y="176" width="150" height="160"/>
<rect x="540" y="370" width="450" height="86" rx="43" fill="#26333d"/>
<image href="{leap}" x="700" y="305" width="150" height="170" transform="rotate(-5 775 390)"/>
<text x="540" y="550" fill="#5a625f" font-family="sans-serif" font-size="24">结构、比例、动作由几何规则控制</text>''')

print(f"wrote previews to {OUT}")
