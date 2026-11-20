#!/usr/bin/env python3
"""Draw entry.png for news-image-20261120: a newspaper front page summing up
Friday 20 November 2026 world news. Six story panels (3x2), each with a flat
drawn illustration, a headline and one factual sub-line. No photos, no logos.
Run: python3 draw.py  (writes entry.png beside this file, 1024x1024)."""

from PIL import Image, ImageDraw, ImageFont
import math

W, H = 1024, 1024
PAPER = (247, 243, 234)
NAVY = (27, 42, 74)
GOLD = (232, 182, 76)
INK = (24, 24, 24)
MUTED = (90, 88, 80)
PANEL_BG = (255, 255, 255)
BORDER = (200, 192, 172)

FONT_DIR = "/usr/share/fonts/truetype/noto/"
F_BOLD = FONT_DIR + "NotoSans-Bold.ttf"
F_REG = FONT_DIR + "NotoSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_text(draw, text, fnt_path, size, max_w, max_lines):
    """Shrink font until text fits in max_lines at max_w. Returns (font, lines)."""
    while size > 10:
        fnt = font(fnt_path, size)
        lines = wrap(draw, text, fnt, max_w)
        if len(lines) <= max_lines:
            return fnt, lines
        size -= 1
    fnt = font(fnt_path, size)
    return fnt, wrap(draw, text, fnt, max_w)[:max_lines]


def panel(draw, x, y, w, h, tag, tag_color):
    draw.rectangle([x, y, x + w, y + h], fill=PANEL_BG, outline=BORDER, width=2)
    return x, y, w, h


def tag_chip(draw, x, y, text, color):
    fnt = font(F_BOLD, 15)
    tw = draw.textlength(text, font=fnt)
    pad = 8
    draw.rectangle([x, y, x + tw + pad * 2, y + 22], fill=color)
    draw.text((x + pad, y + 3), text, font=fnt, fill=(255, 255, 255))


def draw_cyclone(d, x, y, w, h):
    # Sky + sea + swirling storm
    d.rectangle([x, y, x + w, y + h], fill=(183, 214, 232))
    d.rectangle([x, y + h - 42, x + w, y + h], fill=(44, 110, 145))
    cx, cy = x + w // 2, y + h // 2 - 10
    for r, col in [(78, (250, 250, 250)), (60, (226, 238, 245)),
                   (42, (250, 250, 250)), (26, (200, 220, 232))]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
    d.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=(27, 42, 74))
    for ang in range(0, 360, 45):
        a = math.radians(ang)
        x1 = cx + int(30 * math.cos(a))
        y1 = cy + int(30 * math.sin(a))
        x2 = cx + int(86 * math.cos(a + 0.9))
        y2 = cy + int(86 * math.sin(a + 0.9))
        d.line([x1, y1, x2, y2], fill=(120, 150, 175), width=5)
    # rain streaks
    for i in range(14):
        rx = x + 12 + i * 22
        d.line([rx, y + h - 38, rx - 6, y + h - 18], fill=(255, 255, 255), width=2)


def draw_strike(d, x, y, w, h):
    # Street scene: three figures with placards
    d.rectangle([x, y, x + w, y + h], fill=(255, 226, 168))
    d.rectangle([x, y + h - 34, x + w, y + h], fill=(120, 120, 116))
    colors = [(196, 60, 60), (42, 110, 180), (46, 140, 90)]
    labels = ["FUTURE", "NOT WAR", "OUR DAY"]
    for i, (c, lab) in enumerate(zip(colors, labels)):
        px = x + 28 + i * 100
        # placard
        d.rectangle([px, y + 18, px + 84, y + 66], fill=(255, 255, 255),
                    outline=c, width=3)
        fnt = font(F_BOLD, 15)
        tw = d.textlength(lab, font=fnt)
        d.text((px + (84 - tw) / 2, y + 36), lab, font=fnt, fill=c)
        # stick
        d.line([px + 42, y + 66, px + 42, y + 104], fill=(90, 70, 50), width=4)
        # figure: head + body, standing on the ground strip
        d.ellipse([px + 30, y + 104, px + 54, y + 128], fill=(240, 200, 160))
        d.rectangle([px + 22, y + 130, px + 62, y + h - 34], fill=c)


def draw_eu_deal(d, x, y, w, h):
    # Signed document + pen + two colour bars (UK / EU abstract)
    d.rectangle([x, y, x + w, y + h], fill=(214, 228, 240))
    # document
    dx, dy = x + 78, y + 26
    d.rectangle([dx, dy, dx + 170, dy + 128], fill=(255, 255, 255),
                outline=(27, 42, 74), width=3)
    for i in range(4):
        d.line([dx + 16, dy + 24 + i * 20, dx + 154, dy + 24 + i * 20],
               fill=(150, 150, 150), width=3)
    # signature squiggle
    pts = [(dx + 20, dy + 108), (dx + 45, dy + 96), (dx + 70, dy + 110),
           (dx + 95, dy + 98), (dx + 120, dy + 108)]
    d.line(pts, fill=(30, 60, 160), width=3, joint="curve")
    # pen
    d.line([dx + 150, dy + 60, dx + 205, dy + 20], fill=(27, 42, 74), width=6)
    d.polygon([(dx + 205, dy + 20), (dx + 216, dy + 26), (dx + 208, dy + 34)],
              fill=(232, 182, 76))
    # colour bars: red-white-blue / blue with gold stars
    d.rectangle([x + 20, y + h - 40, x + 130, y + h - 18], fill=(200, 40, 50))
    d.rectangle([x + 20, y + h - 40, x + 130, y + h - 33], fill=(255, 255, 255))
    d.rectangle([x + 20, y + h - 25, x + 130, y + h - 18], fill=(30, 60, 160))
    d.rectangle([x + 176, y + h - 40, x + 286, y + h - 18], fill=(30, 60, 160))
    for ang in range(0, 360, 30):
        a = math.radians(ang)
        sx = x + 231 + int(9 * math.cos(a))
        sy = y + h - 29 + int(9 * math.sin(a))
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(232, 182, 76))


def draw_cop(d, x, y, w, h):
    # Globe + leaf + rising sun
    d.rectangle([x, y, x + w, y + h], fill=(196, 226, 200))
    cx, cy, r = x + w // 2, y + h // 2 + 6, 74
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(90, 160, 210))
    d.ellipse([cx - 52, cy - 58, cx + 6, cy - 6], fill=(80, 170, 90))
    d.ellipse([cx - 8, cy + 8, cx + 56, cy + 62], fill=(80, 170, 90))
    d.ellipse([cx + 18, cy - 62, cx + 58, cy - 18], fill=(80, 170, 90))
    # sun
    d.ellipse([x + w - 52, y + 14, x + w - 18, y + 48], fill=(232, 182, 76))
    # leaf
    d.ellipse([x + 18, y + 18, x + 62, y + 52], fill=(46, 140, 90))
    d.line([x + 20, y + 50, x + 60, y + 20], fill=(255, 255, 255), width=2)


def draw_kyiv(d, x, y, w, h):
    # Damaged building, smoke, drone
    d.rectangle([x, y, x + w, y + h], fill=(228, 220, 205))
    # smoke
    for i, r in enumerate([26, 20, 15]):
        d.ellipse([x + 200 + i * 8, y + 12 + i * 16, x + 200 + i * 8 + r * 2,
                   y + 12 + i * 16 + r * 2], fill=(150, 150, 150))
    # building
    bx, by = x + 46, y + 44
    d.rectangle([bx, by, bx + 200, y + h - 24], fill=(180, 160, 130),
                outline=(90, 80, 60), width=3)
    d.polygon([(bx - 8, by), (bx + 100, by - 26), (bx + 208, by)],
              fill=(120, 60, 50))
    # windows, two shattered
    for row in range(3):
        for col in range(4):
            wx = bx + 18 + col * 48
            wy = by + 22 + row * 44
            d.rectangle([wx, wy, wx + 30, wy + 28], fill=(240, 230, 200),
                        outline=(90, 80, 60), width=2)
            if (row, col) in [(0, 1), (1, 2)]:
                d.line([wx, wy, wx + 30, wy + 28], fill=(60, 50, 40), width=2)
                d.line([wx + 30, wy, wx, wy + 28], fill=(60, 50, 40), width=2)
    # drone silhouette (clear of the tag chip at top-left)
    dx, dy = x + 96, y + 16
    d.rectangle([dx, dy, dx + 34, dy + 10], fill=(40, 40, 40))
    d.ellipse([dx - 8, dy - 6, dx + 6, dy + 6], fill=(40, 40, 40))
    d.ellipse([dx + 28, dy - 6, dx + 42, dy + 6], fill=(40, 40, 40))


def draw_berlin(d, x, y, w, h):
    # Podium with microphones + shield
    d.rectangle([x, y, x + w, y + h], fill=(210, 214, 226))
    # backdrop flags (abstract colour bars)
    d.rectangle([x + 24, y + 16, x + 64, y + 92], fill=(30, 60, 160))
    d.rectangle([x + 24, y + 16, x + 64, y + 42], fill=(200, 40, 50))
    d.rectangle([x + 24, y + 42, x + 64, y + 66], fill=(255, 255, 255))
    d.rectangle([x + w - 64, y + 16, x + w - 24, y + 92], fill=(30, 60, 160))
    for ang in range(0, 360, 30):
        a = math.radians(ang)
        sx = x + w - 44 + int(12 * math.cos(a))
        sy = y + 54 + int(12 * math.sin(a))
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(232, 182, 76))
    # podium
    px, py = x + 88, y + 96
    d.polygon([(px, py), (px + 130, py), (px + 118, y + h - 16),
               (px + 12, y + h - 16)], fill=(120, 90, 60))
    # shield on podium
    sx, sy = x + w // 2, y + 118
    d.polygon([(sx - 34, sy - 14), (sx + 34, sy - 14), (sx + 34, sy + 12),
               (sx, sy + 38), (sx - 34, sy + 12)], fill=(27, 42, 74))
    fnt = font(F_BOLD, 20)
    d.text((sx - 8, sy - 6), "5", font=fnt, fill=(232, 182, 76))
    # microphones
    d.line([x + 118, y + 96, x + 104, y + 70], fill=(40, 40, 40), width=4)
    d.ellipse([x + 96, y + 58, x + 112, y + 74], fill=(40, 40, 40))
    d.line([x + 188, y + 96, x + 202, y + 70], fill=(40, 40, 40), width=4)
    d.ellipse([x + 194, y + 58, x + 210, y + 74], fill=(40, 40, 40))


STORIES = [
    dict(tag="CYCLONE", color=(44, 110, 145),
         draw=draw_cyclone,
         headline="CYCLONE AKVAN HITS ODISHA",
         sub="Landfall near Gopalpur; 100,000+ evacuated as winds reach 110 km/h"),
    dict(tag="PROTEST", color=(196, 60, 60),
         draw=draw_strike,
         headline="YOUTH STRIKE SWEEPS EUROPE",
         sub="Walkouts in 25+ countries; 300+ UK schools join 'not their wars' protest"),
    dict(tag="EUROPE", color=(30, 60, 160),
         draw=draw_eu_deal,
         headline="BRITAIN SIGNS EU RESET DEAL",
         sub="Burnham inks food and farming pact in Brussels; exit clause if a future PM quits"),
    dict(tag="CLIMATE", color=(46, 140, 90),
         draw=draw_cop,
         headline="COP31 REACHES FINAL DAY",
         sub="Antalya talks end today with fossil-fuel and finance gaps still open"),
    dict(tag="WAR", color=(120, 60, 50),
         draw=draw_kyiv,
         headline="RUSSIAN DRONES HIT KYIV EMBASSIES",
         sub="Austrian and Dutch missions damaged; one killed, cathedral windows shattered"),
    dict(tag="DIPLOMACY", color=(27, 42, 74),
         draw=draw_berlin,
         headline="RUSSIA 'COMFORTABLE' WITH ARTICLE 5 GUARANTEE",
         sub="Kushner in Berlin: Moscow open to NATO-style security for postwar Ukraine"),
]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Header band
    d.rectangle([0, 0, W, 148], fill=NAVY)
    d.rectangle([0, 148, W, 152], fill=GOLD)
    f_mast = font(F_BOLD, 62)
    mast = "THE WORLD TODAY"
    tw = d.textlength(mast, font=f_mast)
    d.text(((W - tw) / 2, 12), mast, font=f_mast, fill=(255, 255, 255))
    f_date = font(F_BOLD, 34)
    date = "FRIDAY, 20 NOVEMBER 2026"
    tw = d.textlength(date, font=f_date)
    d.text(((W - tw) / 2, 88), date, font=f_date, fill=GOLD)
    f_sub = font(F_REG, 18)
    tagline = "One day in the world  •  Six stories"
    tw = d.textlength(tagline, font=f_sub)
    d.text(((W - tw) / 2, 126), tagline, font=f_sub, fill=(200, 205, 220))

    # Grid of panels: 3 columns x 2 rows
    px = [12, 349, 686]
    py = [160, 572]
    pw, ph = 326, 400
    ill_h = 196
    for i, s in enumerate(STORIES):
        x = px[i % 3]
        y = py[i // 3]
        panel(d, x, y, pw, ph, s["tag"], s["color"])
        s["draw"](d, x + 8, y + 8, pw - 16, ill_h)
        tag_chip(d, x + 8, y + 8, s["tag"], s["color"])
        # headline
        hfnt, hlines = fit_text(d, s["headline"], F_BOLD, 27, pw - 24, 2)
        hy = y + 8 + ill_h + 14
        for line in hlines:
            d.text((x + 12, hy), line, font=hfnt, fill=INK)
            hy += hfnt.size + 4
        # sub-line
        sfnt, slines = fit_text(d, s["sub"], F_REG, 19, pw - 24, 2)
        sy = y + ph - 14 - len(slines) * (sfnt.size + 3)
        for line in slines:
            d.text((x + 12, sy), line, font=sfnt, fill=MUTED)
            sy += sfnt.size + 3

    # Footer ticker
    d.rectangle([0, 980, W, H], fill=NAVY)
    f_tick = font(F_REG, 17)
    tick = ("ALSO TODAY:  World Children's Day  •  IFFI film festival opens in Goa  •  "
            "India v New Zealand, day two")
    tw = d.textlength(tick, font=f_tick)
    d.text(((W - tw) / 2, 995), tick, font=f_tick, fill=(255, 255, 255))

    img.save("entry.png", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    main()
