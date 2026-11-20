#!/usr/bin/env python3
"""Draw the world news of Thursday 19 November 2026 as a one-page
newspaper front page, 1024x1024 PNG.

Pure Pillow: flat spot illustrations drawn with polygons, arcs and
ellipses, copy set in DejaVu. Run: python3 render.py
Writes entry.png beside this script.

Stories (each verified against live reporting on the morning of
19 Nov 2026, Reuters / Kyiv Independent / IMD / AP / CNBC):
  1. Trump, Xi Jinping and Vladimir Putin hold their first trilateral
     summit in Shenzhen, on the APEC sidelines.
  2. Anthropic starts trading on Nasdaq (ANT) after pricing its $83
     IPO at $81.3bn, the largest debut ever.
  3. Grand Theft Auto VI launches worldwide at midnight local time,
     13 years after GTA V, rated 99 on Metacritic.
  4. Ukraine strikes the Crimea bridge a third time this week, just
     after midnight on 19 November.
  5. Severe Cyclonic Storm Akvan closes on India's east coast; seven
     Andhra Pradesh districts are on red alert.
  6. Israel's Gaza ground operation enters a second day, crossing the
     ceasefire "yellow line" in central Gaza.
"""
import os

from PIL import Image, ImageDraw, ImageFont

SIDE = 1024
EDGE = 34
SPAN = SIDE - 2 * EDGE
TARGET = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

# --- colours --------------------------------------------------------------
SHEET = (250, 246, 238)
PENCIL = (22, 22, 22)
CRIMSON = (172, 48, 36)
FADED = (112, 106, 96)
HAIRLINE = (205, 197, 180)
NIGHT = (24, 38, 58)
DUSK = (58, 68, 110)
TANGERINE = (242, 140, 60)
SEAFOAM = (214, 232, 228)
TEAL = (36, 110, 96)
OCEAN = (30, 84, 118)
SANDY = (233, 216, 180)
LEMON = (240, 196, 60)
CLOUDW = (252, 252, 252)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"


def load(face, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, face), size)


def serif(size):
    return load("DejaVuSerif-Bold.ttf", size)


def bold(size):
    return load("DejaVuSans-Bold.ttf", size)


def plain(size):
    return load("DejaVuSans.ttf", size)


class FrontPage:
    """A 1024x1024 sheet with helpers for wrapped copy and rules."""

    def __init__(self):
        self.sheet = Image.new("RGB", (SIDE, SIDE), SHEET)
        self.brush = ImageDraw.Draw(self.sheet)

    def text_w(self, s, fnt):
        return self.brush.textlength(s, font=fnt)

    def wrap(self, s, fnt, limit):
        lines, cur = [], ""
        for word in s.split():
            trial = (cur + " " + word).strip()
            if self.text_w(trial, fnt) <= limit or not cur:
                cur = trial
            else:
                lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
        return lines

    def para(self, x, y, s, fnt, limit, step, colour=PENCIL):
        for line in self.wrap(s, fnt, limit):
            self.brush.text((x, y), line, font=fnt, fill=colour)
            y += step
        return y

    def banner(self, x, y, lines, size, step=None):
        fnt = bold(size)
        step = step or int(size * 1.1)
        for line in lines:
            self.brush.text((x, y), line, font=fnt, fill=PENCIL)
            y += step
        return y

    def tag(self, x, y, s, size=18):
        self.brush.text((x, y), s.upper(), font=bold(size), fill=CRIMSON)
        return y + size + 9

    def hline(self, y, x0=EDGE, x1=SIDE - EDGE, colour=PENCIL, w=2):
        self.brush.line([(x0, y), (x1, y)], fill=colour, width=w)

    def vline(self, x, y0, y1, colour=HAIRLINE, w=1):
        self.brush.line([(x, y0), (x, y1)], fill=colour, width=w)

    def save(self):
        self.sheet.save(TARGET, "PNG")
        print("wrote", TARGET, os.path.getsize(TARGET), "bytes")


page = FrontPage()
d = page.brush

# --- masthead --------------------------------------------------------------
mast = "THE WORLD TODAY"
mf = serif(58)
d.text(((SIDE - page.text_w(mast, mf)) / 2, 24), mast, font=mf, fill=PENCIL)
d.rectangle([EDGE, 96, SIDE - EDGE, 100], fill=CRIMSON)
page.hline(108, colour=PENCIL, w=1)
dateline = "THURSDAY 19 NOVEMBER 2026  ·  THE WORLD IN ONE PAGE"
df = bold(19)
d.text(((SIDE - page.text_w(dateline, df)) / 2, 118), dateline, font=df,
       fill=PENCIL)
page.hline(146, colour=HAIRLINE, w=1)


# --- spot art --------------------------------------------------------------
def art_summit(x, y, w, h):
    """Three flags over a summit table, Shenzhen skyline at dusk."""
    d.rectangle([x, y, x + w, y + h], fill=NIGHT)
    # tower silhouettes
    base = y + h - 34
    for bx, bw, bh in [(10, 30, 60), (46, 22, 88), (74, 36, 52), (116, 26, 76),
                       (148, 30, 48), (184, 24, 66), (214, 32, 58),
                       (252, 26, 80), (284, 30, 54), (320, 24, 70)]:
        d.rectangle([x + bx, base - bh, x + bx + bw, base], fill=(44, 58, 84))
        for wy in range(base - bh + 8, base - 6, 14):
            d.rectangle([x + bx + 6, wy, x + bx + 10, wy + 6], fill=LEMON)
    # red carpet
    d.rectangle([x, base, x + w, y + h], fill=(122, 30, 28))
    # three flag poles with flags: USA, China, Russia
    d.line([(x + 52, y + 16), (x + 52, base - 40)], fill=(200, 200, 200),
           width=3)
    d.line([(x + w // 2, y + 16), (x + w // 2, base - 40)],
           fill=(200, 200, 200), width=3)
    d.line([(x + w - 52, y + 16), (x + w - 52, base - 40)],
           fill=(200, 200, 200), width=3)
    # USA: red-white stripes with a blue canton
    for i in range(5):
        d.rectangle([x + 52, y + 18 + i * 6, x + 108, y + 24 + i * 6],
                    fill=(200, 40, 40) if i % 2 == 0 else CLOUDW)
    d.rectangle([x + 52, y + 18, x + 74, y + 36], fill=(40, 60, 140))
    # China: red field, gold stars
    d.rectangle([x + w // 2, y + 18, x + w // 2 + 56, y + 48],
                fill=(200, 40, 40))
    d.ellipse([x + w // 2 + 8, y + 25, x + w // 2 + 16, y + 33], fill=LEMON)
    for sx, sy in [(x + w // 2 + 24, y + 22), (x + w // 2 + 30, y + 28),
                   (x + w // 2 + 24, y + 36), (x + w // 2 + 16, y + 40)]:
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=LEMON)
    # Russia: white-blue-red horizontal bands
    d.rectangle([x + w - 52, y + 18, x + w + 4, y + 28], fill=CLOUDW)
    d.rectangle([x + w - 52, y + 28, x + w + 4, y + 38], fill=(40, 80, 160))
    d.rectangle([x + w - 52, y + 38, x + w + 4, y + 48], fill=(200, 40, 40))
    # summit table
    d.polygon([(x + 70, base - 34), (x + w - 70, base - 34),
               (x + w - 52, base), (x + 52, base)], fill=(96, 64, 40))
    d.rectangle([x + 70, base - 40, x + w - 70, base - 34], fill=(140, 100, 62))
    # three seats (heads above the table)
    for hx in (x + 110, x + w // 2, x + w - 110):
        d.ellipse([hx - 13, base - 66, hx + 13, base - 40], fill=(232, 200, 170))
        d.rectangle([hx - 20, base - 42, hx + 20, base - 34], fill=PENCIL)


def art_market(x, y, w, h):
    """A debut-day chart: rising line, bars, and the $83 print."""
    d.rectangle([x, y, x + w, y + h], fill=SEAFOAM)
    for gy in range(y + 16, y + h - 10, 22):
        d.line([(x + 8, gy), (x + w - 8, gy)], fill=(190, 210, 204), width=1)
    # bars
    base = y + h - 10
    for i, bh in enumerate([16, 26, 22, 38, 52]):
        d.rectangle([x + 12 + i * 26, base - bh, x + 30 + i * 26, base],
                    fill=TEAL)
    # rising line with arrowhead
    pts = [(x + 14, y + h - 34), (x + 52, y + h - 52), (x + 88, y + h - 44),
           (x + 124, y + h - 66), (x + w - 14, y + 22)]
    d.line(pts, fill=CRIMSON, width=4)
    d.polygon([(x + w - 14, y + 14), (x + w - 26, y + 24), (x + w - 6, y + 28)],
              fill=CRIMSON)
    d.text((x + 12, y + 10), "$83", font=bold(30), fill=PENCIL)


def art_vice(x, y, w, h):
    """Vice City at dusk: pink sun, palms, neon skyline."""
    d.rectangle([x, y, x + w, y + h], fill=(66, 40, 96))
    d.ellipse([x + w // 2 - 34, y + 12, x + w // 2 + 34, y + 80],
              fill=(250, 120, 150))
    d.rectangle([x, y + h - 30, x + w, y + h], fill=(20, 24, 52))
    base = y + h - 30
    for bx, bw, bh in [(8, 26, 44), (40, 20, 64), (66, 30, 38), (102, 22, 56),
                       (130, 28, 42)]:
        d.rectangle([x + bx, base - bh, x + bx + bw, base], fill=(16, 16, 40))
        for wy in range(base - bh + 7, base - 5, 12):
            d.rectangle([x + bx + 5, wy, x + bx + 9, wy + 5],
                        fill=(0, 220, 200))
    # palm silhouettes
    for px, py in [(x + w - 30, base - 46), (x + 18, base - 40)]:
        d.line([(px, py + 34), (px, py)], fill=(10, 40, 20), width=4)
        for ang in (-50, -20, 10, 40):
            import math
            ex = px + int(22 * math.cos(math.radians(ang - 90)))
            ey = py + int(22 * math.sin(math.radians(ang - 90)))
            d.line([(px, py), (ex, ey)], fill=(10, 40, 20), width=3)


def art_bridge(x, y, w, h):
    """The Kerch bridge with its road span dropped into the strait."""
    d.rectangle([x, y, x + w, y + h], fill=(178, 205, 220))
    d.rectangle([x, y + h - 24, x + w, y + h], fill=OCEAN)
    # deck, split in two by the gap
    dy = y + 30
    d.rectangle([x, dy, x + 96, dy + 12], fill=(120, 118, 110))
    d.rectangle([x + w - 96, dy, x + w, dy + 12], fill=(120, 118, 110))
    # fallen span in the water, tilted
    d.polygon([(x + 104, y + h - 20), (x + 196, y + h - 26),
               (x + 200, y + h - 14), (x + 108, y + h - 8)], fill=(90, 88, 82))
    # support pillars
    for px in (x + 26, x + 66, x + w - 66, x + w - 26):
        d.rectangle([px - 4, dy + 12, px + 4, y + h - 24], fill=(100, 98, 92))
    # arch stubs
    d.arc([x + 8, dy - 34, x + 96, dy + 14], 180, 360, fill=(90, 88, 82),
          width=5)
    d.arc([x + w - 96, dy - 34, x + w - 8, dy + 14], 180, 360,
          fill=(90, 88, 82), width=5)
    # smoke over the gap
    for sx, sy, sr in [(x + w // 2 - 12, y + 26, 10), (x + w // 2 + 8, y + 18, 13),
                       (x + w // 2 + 2, y + 34, 8)]:
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(120, 120, 120))
    # ripples
    for rx in range(12, w - 12, 30):
        d.arc([x + rx, y + h - 26, x + rx + 18, y + h - 16], 0, 180,
              fill=(200, 220, 230), width=2)


def art_storm(x, y, w, h):
    """Spiral bands over a coastline: Akvan closing on the coast."""
    d.rectangle([x, y, x + w, y + h], fill=(28, 52, 72))
    # coastline: land on the left, sea on the right
    d.polygon([(x, y), (x + 78, y), (x + 52, y + h), (x, y + h)], fill=SANDY)
    d.line([(x + 78, y), (x + 52, y + h)], fill=(255, 255, 255), width=2)
    # spiral bands
    cx, cy = x + w // 2 + 30, y + h // 2 - 4
    for r, col in [(46, (225, 230, 235)), (35, (170, 192, 204)),
                   (24, (130, 162, 178)), (13, (245, 245, 245))]:
        d.arc([cx - r, cy - r, cx + r, cy + r], 30, 320, fill=col, width=6)
    d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=CLOUDW)
    # rain over the coast
    for rx in range(6, 60, 12):
        d.line([(x + rx, y + h - 30), (x + rx - 4, y + h - 16)],
               fill=(150, 180, 200), width=2)
    # red-alert marker on the coast
    tx, ty = x + 62, y + 16
    d.polygon([(tx, ty), (tx + 22, ty + 26), (tx - 22, ty + 26)], fill=CRIMSON)
    d.text((tx - 3, ty + 7), "!", font=bold(16), fill=CLOUDW)


def art_line(x, y, w, h):
    """A ceasefire line on a map: tanks on one side, tents on the other."""
    d.rectangle([x, y, x + w, y + h], fill=(238, 230, 214))
    # the yellow line, dashed
    ly = y + h // 2
    for dx in range(0, w, 18):
        d.line([(x + dx, ly), (x + dx + 10, ly)], fill=LEMON, width=5)
    # tanks above the line
    for tx in (x + 30, x + 120, x + 210):
        d.rectangle([tx, ly - 24, tx + 46, ly - 12], fill=(84, 96, 70))
        d.rectangle([tx + 10, ly - 32, tx + 36, ly - 24], fill=(70, 82, 58))
        d.line([(tx + 36, ly - 28), (tx + 58, ly - 28)], fill=(70, 82, 58),
               width=4)
        d.ellipse([tx + 6, ly - 10, tx + 14, ly - 4], fill=PENCIL)
        d.ellipse([tx + 32, ly - 10, tx + 40, ly - 4], fill=PENCIL)
    # tents below the line
    for tx in (x + 40, x + 130, x + 220):
        d.polygon([(tx, ly + 34), (tx + 26, ly + 8), (tx + 52, ly + 34)],
                  fill=(200, 190, 170))
        d.line([(tx + 26, ly + 8), (tx + 26, ly + 34)], fill=(120, 110, 95),
               width=2)


# --- lead story: the Shenzhen trilateral ----------------------------------
ly = 158
page.tag(EDGE, ly, "Shenzhen · The Summit")
hy = page.banner(EDGE, ly + 30, ["TRUMP, XI &", "PUTIN MEET IN", "SHENZHEN"], 43)
art_summit(EDGE + 566, ly + 30, 390, 268)
page.para(EDGE, hy + 6,
          "The presidents of the United States, China and Russia sit down "
          "together for the first time, on the APEC sidelines — nuclear "
          "arms, Ukraine and the war in the Gulf on the table. Putin calls "
          "the meeting a chance for “big potential benefit”.",
          plain(20), 536, 26)
page.hline(458, colour=HAIRLINE, w=1)

# --- second row: Anthropic + GTA VI ---------------------------------------
ry = 474
half = (SPAN - 24) // 2
page.tag(EDGE, ry, "Markets · Tech")
page.banner(EDGE, ry + 28, ["ANTHROPIC'S", "$81BN DEBUT"], 28)
page.para(EDGE, ry + 96,
          "Claude's maker prices its shares at $83 in the largest debut "
          "ever — near $1.5tn — and starts trading on Nasdaq today as ANT.",
          plain(17), 300, 22)
art_market(EDGE + 308, ry + 90, 158, 122)

gx = EDGE + half + 24
page.vline(gx - 12, ry, ry + 190)
page.tag(gx, ry, "Culture · Gaming")
page.banner(gx, ry + 28, ["GTA VI ARRIVES", "AT LAST"], 28)
page.para(gx, ry + 96,
          "Rockstar's epic returns to Vice City after 13 years, unlocking "
          "at midnight worldwide. Rated 99 on Metacritic; 16 million "
          "copies pre-bought.",
          plain(17), 300, 22)
art_vice(gx + 308, ry + 90, 158, 122)
page.hline(688, colour=HAIRLINE, w=1)

# --- bottom row: three short stories --------------------------------------
by = 704
bw = (SPAN - 48) // 3
c1, c2, c3 = EDGE, EDGE + bw + 24, EDGE + 2 * bw + 48

page.tag(c1, by, "War · Ukraine", 15)
page.banner(c1, by + 24, ["KERCH BRIDGE", "HIT AGAIN"], 23, 26)
art_bridge(c1, by + 82, bw, 74)
page.para(c1, by + 166,
          "Ukraine strikes the Crimea bridge a third time this week, just "
          "after midnight — days after an attack collapsed a road span.",
          plain(17), bw, 22)

page.vline(c2 - 12, by, by + 258)
page.tag(c2, by, "Weather · India", 15)
page.banner(c2, by + 24, ["AKVAN BEARS", "DOWN"], 23, 26)
art_storm(c2, by + 82, bw, 74)
page.para(c2, by + 166,
          "The severe cyclone closes on India's east coast. Seven Andhra "
          "districts are on red alert; landfall is due around noon Friday.",
          plain(17), bw, 22)

page.vline(c3 - 12, by, by + 258)
page.tag(c3, by, "Middle East", 15)
page.banner(c3, by + 24, ["GAZA PUSH", "ENTERS DAY TWO"], 23, 26)
art_line(c3, by + 82, bw, 74)
page.para(c3, by + 166,
          "Israeli tanks push past the “yellow line” in central Gaza for a "
          "second day, in the first ground operation since the ceasefire.",
          plain(17), bw, 22)

# --- footer ----------------------------------------------------------------
page.hline(by + 258, colour=PENCIL, w=2)
foot = "Thursday 19 November 2026 — the day's world news in one page."
ff = plain(16)
d.text(((SIDE - page.text_w(foot, ff)) / 2, by + 268), foot, font=ff,
       fill=FADED)

if __name__ == "__main__":
    page.save()
