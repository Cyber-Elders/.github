# SPDX-License-Identifier: Apache-2.0
"""
Render the Cyber Elders ORG social / link-preview card (1200x630) — the image
shown when github.com/Cyber-Elders is shared. Pure-Python (Pillow). On-message,
honest copy. Brand palette matches the Elder Mind product assets.

Run:  python tools/build_org_card.py     (Pillow required)
"""
from __future__ import annotations
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "profile" / "assets"

BG = (24, 22, 45)
INK = (237, 237, 245)
INDIGO_300 = (165, 180, 252)
MUTED = (156, 163, 175)
TIERS = [(34, 197, 94), (59, 130, 246), (249, 115, 22), (168, 85, 247)]
W, H, M = 1200, 630, 80

_SANS = ["/System/Library/Fonts/Helvetica.ttc", "/Library/Fonts/Arial.ttf",
         "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]
_BOLD = ["/System/Library/Fonts/Helvetica.ttc", "/Library/Fonts/Arial Bold.ttf",
         "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]


def _font(size, bold=False):
    for p in (_BOLD if bold else _SANS):
        try:
            return ImageFont.truetype(p, size, index=(1 if bold and p.endswith(".ttc") else 0))
        except OSError:
            continue
    return ImageFont.load_default()


def build():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    seg = W // len(TIERS)
    for i, c in enumerate(TIERS):
        d.rectangle([i * seg, 0, (i + 1) * seg, 10], fill=c)

    text_x = M
    mark = ASSETS / "avatar.png"
    if mark.exists():
        try:
            m = Image.open(mark).convert("RGBA").resize((200, 200))
            img.paste(m, (M, 70), m)
            text_x = M + 200 + 48
        except OSError:
            pass

    d.text((text_x, 88), "Cyber Elders", font=_font(86, bold=True), fill=INK)
    d.text((text_x, 196), "Elder Mind — agentic governance", font=_font(36), fill=INDIGO_300)

    d.text((M, 322), "A pause before your AI agents act —", font=_font(40, bold=True), fill=INK)
    d.text((M, 376), "from your machine to your organisation.", font=_font(40, bold=True), fill=INK)

    d.text((M, 452), "Local-first harness for coding agents · org-scale governance · honest about its limits.",
           font=_font(26), fill=MUTED)

    d.line([M, 548, W - M, 548], fill=(60, 56, 92), width=1)
    d.text((M, 566), "OWASP-Agentic-aware  ·  NIST-AI-RMF-aligned  ·  Apache-2.0 / CC BY 4.0",
           font=_font(22), fill=MUTED)

    out = ASSETS / "social-card.png"
    img.save(out)
    print(f"  wrote {out.relative_to(ROOT)} ({out.stat().st_size // 1024} KB, {W}x{H})")


if __name__ == "__main__":
    build()
