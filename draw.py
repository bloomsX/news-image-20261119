#!/usr/bin/env python3
"""Draw the 19 November 2026 world-news front page (1024x1024 PNG).

Stories (all verified against multiple outlets reporting on 19 Nov 2026):
 1. Trump, Xi and Putin hold their first three-way talks in Shenzhen (APEC).
 2. Crimean Bridge hit again - third strike in a week; traffic halted.
 3. Iran hits US bases in Kuwait and Bahrain after a US strike on Qeshm Island.
 4. Anthropic begins trading on Nasdaq: record $81.3bn IPO at $83 a share.
 5. M5.7 quake hits Kumamoto, Japan - no tsunami; bullet trains halted.
Strip: Markets slide as the Fed points to more hikes; Scotland reach first World Cup in 28 years.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "/home/hatch/workspace/makefun/news-image-20261119/repo/entry.png"

PAPER = (248, 244, 233)
INK = (20, 33, 61)
RED = (180, 35, 24)
GOLD = (176, 120, 31)
GREY = (90, 96, 110)
PANEL = (255, 255, 255)
BORDER = (20, 33, 61)
TEAL = (14, 116, 144)

F_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
F_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
F_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Wrap text to fit max_w pixels; returns list of lines."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def spaced(text, n=1):
    """Fake letter-spacing with thin spaces."""
    return (" " * n).join(list(text))


def draw_icon_circles(d, cx, cy):
    """Three circles: US (blue), CN (red), RU (gold) with initials."""
    cols = [(29, 78, 137), (180, 35, 24), (176, 120, 31)]
    labs = ["US", "CN", "RU"]
    r = 34
    xs = [cx - 78, cx, cx + 78]
    ys = [cy - 26, cy + 26, cy - 26]
    f = font(F_BOLD, 26)
    for x, y, c, lab in zip(xs, ys, cols, labs):
        d.ellipse([x - r, y - r, x + r, y + r], fill=c, outline=INK, width=2)
        tw = d.textlength(lab, font=f)
        d.text((x - tw / 2, y - 18), lab, font=f, fill=(255, 255, 255))


def draw_icon_bridge(d, x, y, s=1.0):
    """A bridge arc with a blast burst above it."""
    d.arc([x, y, x + 90, y + 46], start=180, end=360, fill=INK, width=4)
    for i in range(5):
        bx = x + 10 + i * 18
        d.line([bx, y + 22, bx, y + 44], fill=INK, width=3)
    d.line([x - 6, y + 44, x + 96, y + 44], fill=INK, width=4)
    cx, cy, r = x + 45, y - 8, 16
    pts = []
    for i in range(16):
        ang = math.pi * i / 8
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=(245, 158, 11), outline=(180, 35, 24))


def draw_icon_burst(d, x, y):
    """Spiky burst (explosion) over two wave lines."""
    cx, cy, r = x + 30, y + 18, 22
    pts = []
    for i in range(20):
        ang = math.pi * i / 10
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=(245, 158, 11), outline=(180, 35, 24))
    for yy in (y + 52, y + 64):
        d.arc([x, yy - 8, x + 60, yy + 8], start=200, end=340, fill=TEAL, width=3)


def draw_icon_bars(d, x, y):
    """Three rising bars with an arrow."""
    heights = [22, 36, 52]
    for i, h in enumerate(heights):
        bx = x + i * 20
        d.rectangle([bx, y + 52 - h, bx + 14, y + 52], fill=(14, 116, 144))
    d.line([x - 4, y + 2, x + 58, y - 12], fill=RED, width=4)
    d.polygon([(x + 58, y - 12), (x + 46, y - 12), (x + 58, y + 0)], fill=RED)


def draw_icon_quake(d, x, y):
    """Seismograph zigzag over cracked ground."""
    pts = [(x, y + 20), (x + 10, y + 20), (x + 14, y + 8), (x + 20, y + 32),
           (x + 26, y + 4), (x + 32, y + 36), (x + 38, y + 12), (x + 44, y + 28),
           (x + 50, y + 20), (x + 62, y + 20)]
    d.line(pts, fill=RED, width=3, joint="curve")
    d.line([x, y + 52, x + 62, y + 52], fill=INK, width=4)
    d.line([x + 14, y + 52, x + 10, y + 64], fill=INK, width=3)
    d.line([x + 34, y + 52, x + 40, y + 66], fill=INK, width=3)
    d.line([x + 50, y + 52, x + 46, y + 62], fill=INK, width=3)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 36  # margin
    CW = W - 2 * M  # content width = 952

    # ---- Header ----
    y = 26
    f_top = font(F_BOLD, 19)
    top = spaced("WORLD NEWS  •  ONE DAY IN PICTURES", 1)
    tw = d.textlength(top, font=f_top)
    d.text(((W - tw) / 2, y), top, font=f_top, fill=GREY)
    y += 30
    f_date = font(F_SERIF, 52)
    date = "THURSDAY 19 NOVEMBER 2026"
    tw = d.textlength(date, font=f_date)
    d.text(((W - tw) / 2, y), date, font=f_date, fill=INK)
    y += 74
    d.rectangle([M, y, W - M, y + 4], fill=RED)
    d.rectangle([M, y + 8, W - M, y + 10], fill=INK)
    y += 22

    # ---- Lead panel: Shenzhen summit ----
    lead_top = y
    lead_h = 216
    d.rectangle([M, lead_top, W - M, lead_top + lead_h], fill=PANEL, outline=BORDER, width=2)
    lx = M + 22
    ly = lead_top + 16
    f_kick = font(F_BOLD, 18)
    d.text((lx, ly), "THE BIG STORY  —  SHENZHEN, CHINA", font=f_kick, fill=RED)
    f_head = font(F_BOLD, 37)
    head_lines = wrap(d, "Trump, Xi and Putin meet in Shenzhen", f_head, 640)
    hy = ly + 30
    for ln in head_lines:
        d.text((lx, hy), ln, font=f_head, fill=INK)
        hy += 44
    f_sum = font(F_REG, 20)
    sum_lines = wrap(
        d,
        "First-ever three-way talks on the sidelines of the APEC summit — "
        "nuclear arms and the Iran war on the agenda.",
        f_sum, 640,
    )
    sy = hy + 6
    for ln in sum_lines:
        d.text((lx, sy), ln, font=f_sum, fill=(40, 48, 66))
        sy += 27
    draw_icon_circles(d, W - M - 130, lead_top + 108)
    y = lead_top + lead_h + 14

    # ---- 2x2 grid ----
    stories = [
        ("UKRAINE", "Crimean Bridge hit again",
         "Third strike on the crossing in a week; traffic halted while damage is assessed.",
         "bridge"),
        ("MIDDLE EAST", "Iran hits U.S. bases in the Gulf",
         "Drones strike Kuwait and Bahrain after a U.S. raid on Qeshm Island; defences intercept them.",
         "burst"),
        ("MARKETS", "Anthropic's $81.3bn record IPO",
         "Biggest IPO of all time; shares start trading on Nasdaq under ticker ANT at $83, valued near $1.5 trillion.",
         "bars"),
        ("DISASTER", "Japan M5.7 quake hits Kumamoto",
         "Early-morning tremor, no tsunami; bullet trains halted and 5,600 passengers affected.",
         "quake"),
    ]
    gw, gh, gap = 464, 216, 24
    for i, (kick, head, summ, icon) in enumerate(stories):
        px = M + (i % 2) * (gw + gap)
        py = y + (i // 2) * (gh + gap)
        d.rectangle([px, py, px + gw, py + gh], fill=PANEL, outline=BORDER, width=2)
        tx = px + 18
        ty = py + 14
        d.text((tx, ty), kick, font=f_kick, fill=RED)
        f_h2 = font(F_BOLD, 27)
        hl = wrap(d, head, f_h2, gw - 36 - 100)
        hy2 = ty + 28
        for ln in hl:
            d.text((tx, hy2), ln, font=f_h2, fill=INK)
            hy2 += 33
        f_s2 = font(F_REG, 19)
        sl = wrap(d, summ, f_s2, gw - 36)
        sy2 = hy2 + 8
        for ln in sl:
            d.text((tx, sy2), ln, font=f_s2, fill=(40, 48, 66))
            sy2 += 25
        ix, iy = px + gw - 108, py + 16
        if icon == "bridge":
            draw_icon_bridge(d, ix, iy)
        elif icon == "burst":
            draw_icon_burst(d, ix, iy)
        elif icon == "bars":
            draw_icon_bars(d, ix, iy)
        else:
            draw_icon_quake(d, ix, iy)
    y = y + 2 * gh + gap + 14

    # ---- Also today strip ----
    f_k2 = font(F_BOLD, 18)
    d.text((M, y), "ALSO TODAY", font=f_k2, fill=RED)
    y += 28
    f_a = font(F_REG, 19)
    items = [
        "Markets slide as the Fed points to more hikes — Bitcoin $63,479 and gold $3,726.",
        "Scotland reach first World Cup in 28 years — McTominay's overhead kick seals it against Denmark in Glasgow.",
    ]
    for it in items:
        lines = wrap(d, "•  " + it, f_a, CW)
        for ln in lines:
            d.text((M, y), ln, font=f_a, fill=INK)
            y += 25
        y += 2

    # ---- Footer ----
    d.rectangle([M, H - 48, W - M, H - 46], fill=BORDER)
    f_f = font(F_REG, 15)
    foot = "Reported 19 Nov 2026 — Reuters · BBC · One Turn · TBS News · NHK · Iboro Finance"
    tw = d.textlength(foot, font=f_f)
    d.text(((W - tw) / 2, H - 34), foot, font=f_f, fill=GREY)

    img.save(OUT, "PNG", optimize=True)
    print("saved", OUT)


if __name__ == "__main__":
    main()
