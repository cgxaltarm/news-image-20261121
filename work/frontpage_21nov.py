#!/usr/bin/env python3
"""Draw the front page for Saturday 21 November 2026.

Renders THE WORLD TODAY as a dense newspaper front page: a masthead,
three illustrated lead stories, a by-hours ticker, ten stories in brief,
a field bar chart, a verdict, markets, twenty more briefs, and a footer
with a date check and a locator map. Everything is drawn with Pillow —
no photos, no downloaded images.

Output: entry.png in the repository root, 1024x1024.
"""

import os
import random
from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BASE)
OUT_PATH = os.path.join(ROOT, "entry.png")

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (20, 20, 20)
RED = (169, 50, 38)
NAVY = (31, 42, 68)
TEAL = (39, 120, 110)
GREEN = (46, 130, 60)
PALE = (250, 244, 214)
GREY = (90, 90, 90)
RULE = (60, 60, 60)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Split text into lines that fit max_w pixels."""
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


def para(draw, x, y, text, fnt, max_w, leading, fill=INK, cap=None):
    """Draw wrapped text; return the y just below the last line."""
    lines = wrap(draw, text, fnt, max_w)
    if cap is not None:
        lines = lines[:cap]
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def headline(draw, x, y, text, fnt, max_w, leading):
    """Draw a headline, uppercased, wrapped; return y below it."""
    return para(draw, x, y, text.upper(), fnt, max_w, leading)


def scene_antalya(draw, x, y, w, h):
    """Antalya summit: mountains, a white hall with a red roof, the sea."""
    draw.rectangle([x, y, x + w, y + h], fill=(178, 214, 235))
    draw.ellipse([x + w - 52, y + 8, x + w - 14, y + 46], fill=(245, 200, 90))
    draw.polygon([(x, y + h), (x + 60, y + 18), (x + 130, y + h)], fill=(110, 150, 110))
    draw.polygon([(x + 90, y + h), (x + 190, y + 8), (x + w, y + h)], fill=(80, 125, 95))
    draw.rectangle([x + 95, y + 52, x + 205, y + 88], fill=(245, 245, 240))
    draw.polygon([(x + 88, y + 54), (x + 150, y + 30), (x + 212, y + 54)], fill=(178, 50, 40))
    for i in range(5):
        draw.rectangle([x + 105 + i * 20, y + 62, x + 113 + i * 20, y + 80], fill=(40, 60, 90))
    draw.line([x + 70, y + 40, x + 70, y + 88], fill=(60, 60, 60), width=2)
    draw.polygon([(x + 70, y + 40), (x + 92, y + 46), (x + 70, y + 52)], fill=(39, 120, 110))
    draw.line([x + w - 60, y + 40, x + w - 60, y + 88], fill=(60, 60, 60), width=2)
    draw.polygon([(x + w - 60, y + 40), (x + w - 38, y + 46), (x + w - 60, y + 52)], fill=(178, 50, 40))
    for i, col in enumerate([(70, 130, 170), (50, 115, 155), (70, 130, 170)]):
        draw.rectangle([x, y + h - 24 + i * 8, x + w, y + h - 16 + i * 8], fill=col)


def scene_bahrain(draw, x, y, w, h):
    """Bahrain at night: a lit skyline, an explosion, smoke."""
    draw.rectangle([x, y, x + w, y + h], fill=(18, 24, 48))
    draw.ellipse([x + w - 48, y + 8, x + w - 18, y + 38], fill=(240, 230, 190))
    rnd = random.Random(7)
    bx = x + 6
    while bx < x + w - 30:
        bw = rnd.randint(26, 44)
        bh = rnd.randint(34, 66)
        draw.rectangle([bx, y + h - bh, bx + bw, y + h], fill=(38, 44, 66))
        for wy in range(y + h - bh + 6, y + h - 4, 9):
            for wx in range(bx + 4, bx + bw - 4, 9):
                if rnd.random() < 0.6:
                    draw.rectangle([wx, wy, wx + 4, wy + 5], fill=(245, 210, 110))
        bx += bw + 4
    cx, cy = x + w // 2, y + 34
    for r, col in [(26, (245, 130, 40)), (18, (255, 180, 60)), (10, (255, 220, 120))]:
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
    draw.ellipse([cx - 6, cy - 26, cx + 14, cy - 12], fill=(120, 120, 120))
    draw.ellipse([cx + 8, cy - 30, cx + 26, cy - 16], fill=(100, 100, 100))


def scene_sinaloa(draw, x, y, w, h):
    """Sinaloa at night: mountains, a moon, a saucer with a light beam."""
    draw.rectangle([x, y, x + w, y + h], fill=(38, 28, 66))
    draw.ellipse([x + 14, y + 10, x + 44, y + 40], fill=(235, 225, 190))
    draw.polygon([(x, y + h), (x + 90, y + 40), (x + 190, y + h)], fill=(52, 44, 78))
    draw.polygon([(x + 130, y + h), (x + 230, y + 30), (x + w, y + h)], fill=(44, 36, 68))
    draw.rectangle([x, y + h - 22, x + w, y + h], fill=(70, 52, 40))
    sx, sy = x + w - 78, y + 26
    draw.polygon([(sx - 26, sy + 34), (sx + 26, sy + 34), (sx + 6, sy + 78), (sx - 6, sy + 78)], fill=(240, 230, 160))
    draw.ellipse([sx - 34, sy - 6, sx + 34, sy + 12], fill=(200, 200, 210))
    draw.ellipse([sx - 12, sy - 14, sx + 12, sy + 2], fill=(120, 140, 170))
    for dx, dy in [(30, 70), (90, 84), (180, 76), (240, 66)]:
        draw.ellipse([x + dx, y + dy, x + dx + 4, y + dy + 4], fill=(245, 220, 120))


def lead(draw, x, y, w, tag, art, head, body, sources):
    """One lead story column. Returns the y below the column."""
    f_tag = font(SANS_B, 12)
    f_head = font(SERIF_B, 26)
    f_body = font(SANS, 13)
    f_src = font(SANS, 10)
    f_badge = font(SANS_B, 10)
    draw.rectangle([x, y, x + w, y + 22], fill=RED)
    draw.text((x + 8, y + 4), tag, font=f_tag, fill=(255, 255, 255))
    y += 22
    art(draw, x, y, w, 104)
    y += 104
    y = headline(draw, x, y + 6, head, f_head, w, 30)
    y = para(draw, x, y + 4, body, f_body, w, 17, cap=5)
    draw.text((x, y + 6), sources, font=f_src, fill=GREY)
    badge = "REPORTED"
    bw = draw.textlength(badge, font=f_badge) + 12
    draw.rounded_rectangle([x + w - bw, y + 3, x + w, y + 19], radius=3, fill=GREEN)
    draw.text((x + w - bw + 6, y + 5), badge, font=f_badge, fill=(255, 255, 255))
    return y + 22


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 16

    # --- top line ---
    f_top = font(SANS_B, 11)
    d.text((mx, 8), "THE WORLD IN ONE PAGE  •  EST. 2026  •  FREE", font=f_top, fill=INK)
    right = "No. 325  •  PRICE: FREE"
    d.text((W - mx - d.textlength(right, font=f_top), 8), right, font=f_top, fill=INK)

    # --- masthead ---
    f_mast = font(SERIF_B, 66)
    title = "THE WORLD TODAY"
    d.text(((W - d.textlength(title, font=f_mast)) / 2, 26), title, font=f_mast, fill=INK)
    d.line([(mx, 100), (W - mx, 100)], fill=INK, width=4)

    # --- dateline ---
    f_date = font(SERIF_B, 20)
    f_sub = font(SANS_B, 12)
    d.text((mx, 108), "SATURDAY 21 NOVEMBER 2026", font=f_date, fill=RED)
    sub = "33 STORIES  •  7 REGIONS  •  ONE DAY, THE WHOLE WORLD"
    d.text((W - mx - d.textlength(sub, font=f_sub), 112), sub, font=f_sub, fill=INK)

    # --- region bar ---
    d.rectangle([mx, 136, W - mx, 158], fill=NAVY)
    f_reg = font(SANS_B, 12)
    d.text((mx + 8, 141), "ASIA 6      EUROPE 7      AMERICAS 6      MIDEAST 5      AFRICA 3      OCEANIA 2      GLOBAL 4",
           font=f_reg, fill=(255, 255, 255))
    tot = "33 STORIES TOTAL"
    d.text((W - mx - 8 - d.textlength(tot, font=f_reg), 141), tot, font=f_reg, fill=(140, 220, 120))

    # --- three leads ---
    col_w = 320
    gap = 16
    x0 = mx
    leads = [
        ("ANTALYA  •  CLIMATE", scene_antalya, "Climate talks near a deal",
         "COP31 runs past its deadline in Antalya, but the summit president says a final deal is close. The fight is over fossil fuels as talks enter a second day of overtime.",
         "Sources: Reuters, AP"),
        ("BAHRAIN  •  CONFLICT", scene_bahrain, "Iran strikes Bahrain",
         "Iran's Guards say they hit US positions at al-Riffa and Awali. Bahrain says an industrial site caught fire and its defences intercepted other attacks. No injuries.",
         "Sources: Reuters, CNN"),
        ("SINALOA  •  CARTELS", scene_sinaloa, "Mexico captures 'El Chapo Isidro'",
         "Special forces seize Fausto Isidro Meza Flores, a Beltran Leyva boss on the FBI's most-wanted list, in Guasave. At least 11 dead — four soldiers, seven attackers.",
         "Sources: AP, Reuters"),
    ]
    lead_bottom = 0
    for i, (tag, art, head, body, src) in enumerate(leads):
        bottom = lead(d, x0 + i * (col_w + gap), 164, col_w, tag, art, head, body, src)
        lead_bottom = max(lead_bottom, bottom)

    # --- by-hours ticker ---
    ty = lead_bottom + 2
    d.rectangle([mx, ty, W - mx, ty + 24], fill=PALE)
    d.rectangle([mx, ty, W - mx, ty + 24], outline=RULE, width=1)
    f_tick = font(SANS, 12)
    f_tick_b = font(SANS_B, 12)
    d.text((mx + 8, ty + 5), "THE DAY BY HOURS", font=f_tick_b, fill=RED)
    items = [("00:40", "Kryvyi Rih hit"), ("09:30", "Sparta II ablaze"),
             ("14:20", "Shenzhen summit"), ("18:45", "Bahrain struck")]
    tx = mx + 170
    for t, label in items:
        d.text((tx, ty + 5), t, font=f_tick_b, fill=INK)
        tx += d.textlength(t, font=f_tick_b) + 6
        d.text((tx, ty + 5), label, font=f_tick, fill=INK)
        tx += d.textlength(label, font=f_tick) + 34

    # --- the day in ten ---
    y = ty + 30
    f_sec = font(SERIF_B, 20)
    d.text((mx, y), "THE DAY IN TEN", font=f_sec, fill=INK)
    d.line([(mx, y + 26), (W - mx, y + 26)], fill=INK, width=2)
    y += 32
    ten = [
        (4, "MISSILE HITS ZELENSKYY'S HOMETOWN", "Kryvyi Rih double-tap kills a boy, 7, and a paramedic; 28 in hospital."),
        (5, "RUSSIAN SHIP BURNS IN FINNISH WATERS", "Drones hit the Sparta II in the Gulf of Finland; crew evacuated."),
        (6, "STOCKS FALL INTO CORRECTION", "Nasdaq erases its 2026 gains as the AI sell-off turns into a rout."),
        (7, "TRUMP, XI AND PUTIN MEET IN SHENZHEN", "Trilateral talks open on nuclear risk reduction."),
        (8, "TWO TANKERS HIT NEAR HORMUZ", "Incidents off Oman as the US denies Iran's F-16 claim."),
        (9, "MISSILES OVER RIYADH INTERCEPTED", "Saudi defences stop three Houthi missiles aimed at the capital."),
        (10, "THREE KILLED IN GAZA FOOD VEHICLE", "Israeli strike hits a vehicle carrying food in Gaza City."),
        (11, "MOSQUITOES CUT DENGUE BY 69%", "Specially bred mosquitoes protect children in a Brazil study."),
        (12, "BOLSONARO IN INTENSIVE CARE", "Former Brazilian president treated for bowel obstruction."),
        (13, "AI 'HELPS PROVE' RIEMANN HYPOTHESIS", "Anthropic researcher says Claude helped crack the maths classic."),
    ]
    f_num = font(SANS_B, 13)
    f_th = font(SANS_B, 13)
    f_tb = font(SANS, 11)
    col2_x = mx + 500
    for i, (num, head, body) in enumerate(ten):
        cx = mx if i < 5 else col2_x
        cy = y + (i % 5) * 35
        d.rectangle([cx, cy, cx + 24, cy + 24], fill=NAVY)
        label = str(num)
        d.text((cx + 12 - d.textlength(label, font=f_num) / 2, cy + 4), label, font=f_num, fill=(255, 255, 255))
        d.text((cx + 30, cy + 1), head, font=f_th, fill=INK)
        para(d, cx + 30, cy + 17, body, f_tb, 440, 13)
    y += 5 * 35 + 6

    # --- three boxes: field chart / verdict / markets ---
    box_y = y
    box_h = 92
    box_w = 320
    f_bh = font(SANS_B, 13)
    f_bb = font(SANS, 12)
    d.rectangle([mx, box_y, mx + box_w, box_y + box_h], outline=RULE, width=1)
    d.text((mx + 8, box_y + 6), "THE DAY BY FIELD", font=f_bh, fill=RED)
    fields = [("Conflict", 8), ("Politics", 7), ("Markets", 6),
              ("Climate", 5), ("Science", 4), ("Sport", 3)]
    fy = box_y + 22
    for name, val in fields:
        d.text((mx + 8, fy), name, font=f_bb, fill=INK)
        d.rectangle([mx + 66, fy + 2, mx + 66 + val * 26, fy + 11], fill=TEAL)
        d.text((mx + 66 + val * 26 + 5, fy), str(val), font=f_bb, fill=INK)
        fy += 11
    vx = mx + box_w + gap
    d.rectangle([vx, box_y, vx + box_w, box_y + box_h], outline=RULE, width=1)
    d.text((vx + 8, box_y + 6), "THE VERDICT", font=f_bh, fill=RED)
    para(d, vx + 8, box_y + 26, "The Gulf burns and the wars grind on; markets punish AI hype, and a cartel kingpin falls as the climate talks run into overtime.",
         f_bb, box_w - 16, 15)
    kx = vx + box_w + gap
    d.rectangle([kx, box_y, kx + box_w, box_y + box_h], outline=RULE, width=1)
    d.text((kx + 8, box_y + 6), "MARKETS & MONEY", font=f_bh, fill=RED)
    for j, line in enumerate(["Nasdaq -5.3%  •  S&P in correction",
                              "Anthropic IPO stumbles, day 2",
                              "Bitcoin > $60,000  •  Brent $92.57"]):
        d.text((kx + 8, box_y + 28 + j * 18), line, font=f_bb, fill=INK)

    # --- also on: briefs 14-33 ---
    y = box_y + box_h + 6
    d.text((mx, y), "ALSO ON...", font=f_sec, fill=INK)
    d.text((mx + 130, y + 5), "20 more stories from Saturday, in brief", font=font(SANS, 12), fill=INK)
    d.line([(mx + 400, y + 12), (W - mx, y + 12)], fill=RULE, width=1)
    y += 30
    briefs = [
        "EU and Indonesia sign a trade deal after ten years of talks.",
        "Poland calls Russian missiles a likely provocation.",
        "France seeks UN action as Myanmar rejects ICJ ruling.",
        "Zelenskyy: Crimea Bridge strikes a 'fair response'.",
        "Denmark: Russia plotted to kill a US-Ukrainian rapper.",
        "FBI probes an apparent hack of its crime database.",
        "Man convicted of starting the Palisades fire in LA.",
        "Mamdani vows to close New York's Rikers jail by 2032.",
        "England beat New Zealand 37-12 in rugby, a record margin.",
        "India 720/9 in NZ as Rahul and Pant hit centuries.",
        "Dak'Art Biennale opens in Dakar with 54 artists.",
        "Trafalgar Square Christmas tree felled in Norway.",
        "Warren Buffett quadruples his Thanksgiving gifts.",
        "Bitcoin climbs back above $60,000, up over 2%.",
        "UN agrees to regulate 'killer robots' by 2028.",
        "Iraqi forces enter a Kataib Hezbollah stronghold.",
        "Iran readies a tanker convoy to break the US blockade.",
        "US declassifies more UFO footage from the Middle East.",
        "Trump threatens a ban on AI data centres built abroad.",
        "Zelenskyy calls Putin a 'killer' after Trump praises him.",
    ]
    f_br = font(SANS, 11)
    f_br_b = font(SANS_B, 11)
    for i, text in enumerate(briefs):
        bx = mx if i < 10 else mx + 500
        by = y + (i % 10) * 14
        num = str(14 + i) + "."
        d.text((bx, by), num, font=f_br_b, fill=RED)
        d.text((bx + 26, by), text, font=f_br, fill=INK)
    y += 10 * 14 + 4

    # --- footer ---
    d.line([(mx, y), (W - mx, y)], fill=INK, width=2)
    y += 6
    f_fh = font(SANS_B, 11)
    f_fb = font(SANS, 10)
    d.text((mx, y), "DATE CHECK", font=f_fh, fill=RED)
    para(d, mx, y + 15, "Left out on purpose: stories dated before 13 Nov 2026 — earlier COP31 drafts, last week's bridge attacks. Everything on this page is 21 Nov.",
         f_fb, 460, 12, cap=3)
    map_x = mx + 480
    d.text((map_x, y), "WHERE IT HAPPENED", font=f_fh, fill=INK)
    d.rectangle([map_x, y + 15, map_x + 190, y + 42], fill=(200, 220, 235), outline=RULE, width=1)
    for gx, gy, gw, gh in [(8, 6, 34, 12), (52, 4, 44, 14), (110, 8, 40, 12), (150, 14, 26, 10)]:
        d.ellipse([map_x + gx, y + 15 + gy, map_x + gx + gw, y + 15 + gy + gh], fill=(150, 190, 140))
    for dx, dy in [(30, 22), (70, 18), (120, 26), (160, 20)]:
        d.ellipse([map_x + dx - 2, y + 15 + dy - 2, map_x + dx + 2, y + 15 + dy + 2], fill=RED)
    hx = map_x + 210
    d.text((hx, y), "HOW ARE WE?", font=f_fh, fill=INK)
    para(d, hx, y + 15, "REPORTED = two or more outlets  •  CLAIM = one side  •  FORECAST = not yet happened",
         f_fb, 280, 12, cap=2)
    d.text((hx, y + 40), "Sources: AP  •  Reuters  •  AFP  •  BBC  •  UN News  •  Nasdaq", font=f_fb, fill=INK)

    img.save(OUT_PATH, "PNG")
    print("wrote %s (%d bytes)" % (OUT_PATH, os.path.getsize(OUT_PATH)))


if __name__ == "__main__":
    main()
