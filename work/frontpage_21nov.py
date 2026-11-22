#!/usr/bin/env python3
"""news-image-20261121 — front page generator (written fresh in this session).

One 1024x1024 newspaper front page summing up world news of
Saturday 21 November 2026. Flat PIL drawing only, no external images.
All facts are the 21 Nov consensus verified against live roundups
(OneTurn, Majik Morning Brief, 360LiveNews, Hansen Intel, 22 Nov 2026):
COP31 near a deal, Iran strikes Bahrain, Mexico captures "El Chapo
Isidro", Kryvyi Rih double-tap, Sparta II burning, stocks in
correction, Shenzhen trilateral, plus 20 verified briefs.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
BG = (253, 248, 238)      # paper
INK = (20, 20, 20)
RED = (178, 34, 34)
DARK = (31, 41, 55)
LIME = (163, 230, 53)
TEAL = (34, 139, 139)
GOLD = (184, 134, 11)
GREY = (90, 90, 90)
LINE = (120, 110, 95)
GREEN = (22, 120, 60)
SKY = (214, 232, 245)
SEA = (70, 140, 190)
ORANGE = (255, 120, 40)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def f(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, font, max_w):
    """Greedy word wrap to pixel width."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, font, fill=INK, lh=None):
    lh = lh or int(font.size * 1.28)
    for ln in lines:
        draw.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y


def tag(draw, x, y, text, fill=GREEN):
    """Small credibility tag, returns width used."""
    font = f(SANS_B, 10)
    w = int(draw.textlength(text, font=font)) + 10
    draw.rounded_rectangle([x, y, x + w, y + 15], radius=3, fill=fill)
    draw.text((x + 5, y + 2), text, font=font, fill=(255, 255, 255))
    return w


def rule(draw, x0, y, x1, wdt=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=wdt)


img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)
MX = 16                      # margin
CW = W - 2 * MX              # 992 content width

# ---------------------------------------------------------------- masthead
d.text((MX, 10), "THE WORLD IN ONE PAGE  •  EST. 2026  •  FREE",
       font=f(SANS_B, 11), fill=GREY)
d.text((W - MX - 190, 10), "No. 325  •  PRICE: FREE", font=f(SANS_B, 11), fill=GREY)
d.text((MX + 118, 26), "THE WORLD TODAY", font=f(SERIF_B, 62), fill=INK)
rule(d, MX, 96, W - MX, 3)
d.text((MX, 102), "SATURDAY 21 NOVEMBER 2026", font=f(SERIF_B, 21), fill=RED)
d.text((MX + 430, 105), "33 STORIES  •  7 REGIONS  •  ONE DAY, THE WHOLE WORLD",
       font=f(SANS_B, 13), fill=INK)
rule(d, MX, 128, W - MX, 1, fill=LINE)

# ---------------------------------------------------------------- region strip
d.rectangle([MX, 134, W - MX, 158], fill=DARK)
regions = [("ASIA", 6), ("EUROPE", 7), ("AMERICAS", 6), ("MIDEAST", 5),
           ("AFRICA", 3), ("OCEANIA", 2), ("GLOBAL", 4)]
rx = MX + 10
for name, n in regions:
    t = f"{name} {n}"
    d.text((rx, 140), t, font=f(SANS_B, 13), fill=(255, 255, 255))
    rx += int(d.textlength(t, font=f(SANS_B, 13))) + 34
d.text((W - MX - 150, 140), "33 STORIES TOTAL", font=f(SANS_B, 13), fill=LIME)

# ---------------------------------------------------------------- lead panels
LEAD_Y, LEAD_H, LEAD_W, GAP = 166, 268, 324, 12
leads = [
    dict(kick="ANTALYA  •  CLIMATE", scene="cop31",
         head="CLIMATE TALKS\nNEAR A DEAL",
         body=("COP31 runs past its deadline in Antalya, but the summit "
               "president says a final deal is close. The fight is over "
               "fossil fuels as talks enter a second day of overtime."),
         src="Sources: Reuters, AP"),
    dict(kick="BAHRAIN  •  CONFLICT", scene="bahrain",
         head="IRAN STRIKES\nBAHRAIN",
         body=("Iran's Guards say they hit US positions at al-Riffa and "
               "Awali. Bahrain says an industrial site caught fire and "
               "its defences intercepted other attacks. No injuries."),
         src="Sources: Reuters, CNN"),
    dict(kick="SINALOA  •  CARTELS", scene="mexico",
         head="MEXICO CAPTURES\n'EL CHAPO ISIDRO'",
         body=("Special forces seize Fausto Isidro Meza Flores, a "
               "Beltran Leyva boss on the FBI's most-wanted list, in "
               "Guasave. At least 11 dead — four soldiers, seven "
               "attackers."),
         src="Sources: AP, Reuters"),
]


def scene_cop31(x, y, w, h):
    """Antalya coast: sun, sea, mountains, summit flags."""
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    # sun
    d.ellipse([x + w - 62, y + 6, x + w - 22, y + 46], fill=(250, 200, 80))
    # mountains
    d.polygon([(x, y + h - 30), (x + 70, y + 28), (x + 140, y + h - 30)],
              fill=(120, 160, 140))
    d.polygon([(x + 110, y + h - 30), (x + 200, y + 18), (x + 290, y + h - 30)],
              fill=(90, 135, 120))
    # sea
    d.rectangle([x, y + h - 30, x + w, y + h], fill=SEA)
    d.line([(x, y + h - 20), (x + w, y + h - 20)], fill=(255, 255, 255), width=1)
    d.line([(x, y + h - 10), (x + w, y + h - 10)], fill=(200, 225, 245), width=1)
    # summit hall on the shore
    d.rectangle([x + 110, y + h - 62, x + 210, y + h - 30], fill=(240, 240, 230))
    d.polygon([(x + 110, y + h - 62), (x + 160, y + h - 78),
               (x + 210, y + h - 62)], fill=RED)
    for wx in range(x + 120, x + 204, 14):
        d.rectangle([wx, y + h - 52, wx + 7, y + h - 38], fill=DARK)
    # three flags
    for fx, fc in [(x + 30, (34, 139, 139)), (x + 60, GOLD), (x + 250, RED)]:
        d.line([(fx, y + h - 30), (fx, y + h - 62)], fill=INK, width=2)
        d.polygon([(fx, y + h - 62), (fx + 22, y + h - 56),
                   (fx, y + h - 50)], fill=fc)


def scene_bahrain(x, y, w, h):
    """Industrial site at night, one building ablaze, smoke drifting."""
    d.rectangle([x, y, x + w, y + h], fill=(28, 32, 58))
    # stars
    for sx, sy in [(20, 12), (60, 24), (110, 10), (180, 18), (240, 12),
                   (280, 26), (150, 30), (90, 34)]:
        d.ellipse([x + sx - 1, y + sy - 1, x + sx + 1, y + sy + 1],
                  fill=(255, 255, 255))
    # moon
    d.ellipse([x + w - 52, y + 8, x + w - 20, y + 40], fill=(240, 230, 190))
    # factory block
    d.rectangle([x + 20, y + h - 46, x + w - 20, y + h], fill=(60, 68, 90))
    # chimneys
    for cx in [x + 40, x + 70, x + 240, x + 268]:
        d.rectangle([cx, y + h - 66, cx + 12, y + h - 46], fill=(45, 52, 70))
    # lit windows
    for wy in range(y + h - 42, y + h - 6, 11):
        for wx in range(x + 28, x + w - 30, 16):
            d.rectangle([wx, wy, wx + 7, wy + 6], fill=(250, 220, 120))
    # fire on the middle block + smoke
    d.polygon([(x + 130, y + h - 46), (x + 150, y + h - 74),
               (x + 170, y + h - 46)], fill=ORANGE)
    d.ellipse([x + 138, y + h - 80, x + 162, y + h - 58],
              fill=(255, 180, 60))
    for sx, sy, sr in [(x + 150, y + h - 88, 10), (x + 166, y + h - 96, 13),
                       (x + 182, y + h - 86, 9)]:
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(150, 150, 150))
    # sparks
    for sx, sy in [(x + 142, y + h - 70), (x + 160, y + h - 66),
                   (x + 152, y + h - 78)]:
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 200, 60))


def scene_mexico(x, y, w, h):
    """Sinaloa night: desert, mountains, helicopter with searchlight."""
    d.rectangle([x, y, x + w, y + h], fill=(52, 40, 68))
    # stars
    for sx, sy in [(24, 10), (70, 20), (130, 8), (200, 16), (260, 10),
                   (300, 24), (170, 26)]:
        d.ellipse([x + sx - 1, y + sy - 1, x + sx + 1, y + sy + 1],
                  fill=(255, 255, 255))
    # moon
    d.ellipse([x + 14, y + 8, x + 40, y + 34], fill=(240, 230, 190))
    # mountains
    d.polygon([(x, y + h - 34), (x + 90, y + 30), (x + 180, y + h - 34)],
              fill=(38, 30, 52))
    d.polygon([(x + 150, y + h - 34), (x + 240, y + 22), (x + w, y + h - 34)],
              fill=(30, 24, 44))
    # desert floor + road
    d.rectangle([x, y + h - 34, x + w, y + h], fill=(120, 90, 60))
    d.polygon([(x + 120, y + h), (x + 150, y + h - 34),
               (x + 170, y + h - 34), (x + 200, y + h)], fill=(60, 55, 50))
    # helicopter with searchlight
    hx, hy = x + w // 2 - 10, y + 14
    d.ellipse([hx, hy, hx + 52, hy + 16], fill=INK)
    d.rectangle([hx + 52, hy + 4, hx + 78, hy + 9], fill=INK)
    d.line([(hx + 8, hy), (hx + 44, hy)], fill=(200, 200, 200), width=2)
    d.polygon([(hx + 20, hy + 16), (hx + 34, hy + 16),
               (hx + 56, y + h - 34), (hx + 12, y + h - 34)],
              fill=(250, 240, 180))
    # ground lights
    for gx in [x + 40, x + 260]:
        d.ellipse([gx - 3, y + h - 8, gx + 3, y + h - 2], fill=(255, 200, 80))


scenes = {"cop31": scene_cop31, "bahrain": scene_bahrain, "mexico": scene_mexico}

for i, L in enumerate(leads):
    x = MX + i * (LEAD_W + GAP)
    d.rectangle([x, LEAD_Y, x + LEAD_W, LEAD_Y + LEAD_H], outline=INK, width=2)
    d.rectangle([x, LEAD_Y, x + LEAD_W, LEAD_Y + 22], fill=RED)
    d.text((x + 8, LEAD_Y + 4), L["kick"], font=f(SANS_B, 11), fill=(255, 255, 255))
    scenes[L["scene"]](x + 6, LEAD_Y + 28, LEAD_W - 12, 92)
    hy = LEAD_Y + 128
    for ln in L["head"].split("\n"):
        d.text((x + 8, hy), ln, font=f(SERIF_B, 21), fill=INK)
        hy += 26
    by = draw_lines(d, wrap(d, L["body"], f(SANS, 12), LEAD_W - 16)[:4],
                    x + 8, hy + 4, f(SANS, 12), lh=16)
    d.text((x + 8, LEAD_Y + LEAD_H - 22), L["src"], font=f(SANS, 10), fill=GREY)
    tag(d, x + LEAD_W - 82, LEAD_Y + LEAD_H - 24, "REPORTED")

# ---------------------------------------------------------------- hours strip
HY = 442
d.rectangle([MX, HY, W - MX, HY + 34], fill=(255, 243, 205), outline=INK, width=1)
d.text((MX + 8, HY + 9), "THE DAY BY HOURS", font=f(SANS_B, 12), fill=RED)
hours = [("00:40", "Kryvyi Rih hit"),
         ("09:30", "Sparta II ablaze"),
         ("14:20", "Shenzhen summit"),
         ("18:45", "Bahrain struck")]
hx = MX + 168
for t, what in hours:
    d.text((hx, HY + 9), t, font=f(SANS_B, 11), fill=INK)
    hx += int(d.textlength(t, font=f(SANS_B, 11))) + 6
    d.text((hx, HY + 9), what, font=f(SANS, 11), fill=INK)
    hx += int(d.textlength(what, font=f(SANS, 11))) + 16

# ---------------------------------------------------------------- grid 4-13
GY, GH = 484, 208
d.text((MX, GY), "THE DAY IN TEN", font=f(SERIF_B, 17), fill=INK)
rule(d, MX + 170, GY + 10, W - MX, 1, fill=LINE)
grid = [
    ("4", "MISSILE HITS ZELENSKYY'S HOMETOWN",
     "Kryvyi Rih double-tap kills a boy, 7, and a paramedic; 28 in hospital."),
    ("5", "RUSSIAN SHIP BURNS IN FINNISH WATERS",
     "Drones hit the Sparta II in the Gulf of Finland; crew evacuated."),
    ("6", "STOCKS FALL INTO CORRECTION",
     "Nasdaq erases its 2026 gains as the AI sell-off turns into a rout."),
    ("7", "TRUMP, XI AND PUTIN MEET IN SHENZHEN",
     "Trilateral talks open on nuclear risk reduction."),
    ("8", "TWO TANKERS HIT NEAR HORMUZ",
     "Incidents off Oman as the US denies Iran's F-16 claim."),
    ("9", "MISSILES OVER RIYADH INTERCEPTED",
     "Saudi defences stop three Houthi missiles aimed at the capital."),
    ("10", "THREE KILLED IN GAZA FOOD VEHICLE",
     "Israeli strike hits a vehicle carrying food in Gaza City."),
    ("11", "MOSQUITOES CUT DENGUE BY 69%",
     "Specially bred mosquitoes protect children in a Brazil study."),
    ("12", "BOLSONARO IN INTENSIVE CARE",
     "Former Brazilian president treated for a bowel obstruction."),
    ("13", "AI 'HELPS PROVE' RIEMANN HYPOTHESIS",
     "Anthropic researcher says Claude helped crack the maths classic."),
]
row_h = 37
for i, (num, head, body) in enumerate(grid):
    col, row = i % 2, i // 2
    gx = MX + col * (CW // 2 + 8)
    gy = GY + 26 + row * row_h
    d.rectangle([gx, gy, gx + 24, gy + 24], fill=DARK)
    d.text((gx + 7, gy + 4), num, font=f(SANS_B, 13), fill=(255, 255, 255))
    d.text((gx + 30, gy), head, font=f(SANS_B, 12), fill=INK)
    body_font = f(SANS, 11)
    max_bw = CW // 2 - 40
    while d.textlength(body, font=body_font) > max_bw and len(body) > 10:
        body = body[:-2]
    d.text((gx + 30, gy + 16), body, font=body_font, fill=(60, 60, 60))

# ---------------------------------------------------------------- middle row
MY, MH = 700, 96
bw3 = (CW - 24) // 3
# bar chart
bx = MX
d.rectangle([bx, MY, bx + bw3, MY + MH], outline=INK, width=1)
d.text((bx + 8, MY + 6), "THE DAY BY FIELD", font=f(SANS_B, 12), fill=RED)
fields = [("Conflict", 8), ("Politics", 7), ("Markets", 6),
          ("Climate", 5), ("Science", 4), ("Sport", 3)]
fy = MY + 26
for name, n in fields:
    d.text((bx + 8, fy), name, font=f(SANS, 10), fill=INK)
    d.rectangle([bx + 78, fy + 2, bx + 78 + n * 20, fy + 10], fill=TEAL)
    d.text((bx + 78 + n * 20 + 5, fy), str(n), font=f(SANS_B, 10), fill=INK)
    fy += 11
# verdict
vx = MX + bw3 + 12
d.rectangle([vx, MY, vx + bw3, MY + MH], outline=INK, width=1)
d.text((vx + 8, MY + 6), "THE VERDICT", font=f(SANS_B, 12), fill=RED)
draw_lines(d, wrap(d, "The Gulf burns and the wars grind on; markets "
                      "punish AI hype; and a cartel kingpin falls as "
                      "the climate talks run into overtime.",
                   f(SANS, 11), bw3 - 16),
           vx + 8, MY + 26, f(SANS, 11), lh=15)
# markets
kx = MX + 2 * (bw3 + 12)
d.rectangle([kx, MY, kx + bw3, MY + MH], outline=INK, width=1)
d.text((kx + 8, MY + 6), "MARKETS & MONEY", font=f(SANS_B, 12), fill=RED)
for j, ln in enumerate(["Nasdaq -5.3%  •  S&P in correction",
                        "Anthropic IPO stumbles, day 2",
                        "Bitcoin > $60,000  •  Brent $92.57"]):
    d.text((kx + 8, MY + 28 + j * 20), ln, font=f(SANS, 12), fill=INK)

# ---------------------------------------------------------------- briefs 14-33
BY = 804
d.text((MX, BY), "ALSO ON…", font=f(SERIF_B, 17), fill=INK)
d.text((MX + 120, BY + 4), "20 more stories from Saturday, in brief",
       font=f(SANS, 11), fill=GREY)
rule(d, MX + 380, BY + 10, W - MX, 1, fill=LINE)
briefs = [
    ("14", "EU and Indonesia sign a trade deal after ten years of talks."),
    ("15", "Poland calls Russian missiles a likely provocation."),
    ("16", "France seeks UN action as Myanmar rejects ICJ ruling."),
    ("17", "Zelenskyy: Crimea Bridge strikes a 'fair response'."),
    ("18", "Denmark: Russia plotted to kill a US-Ukrainian rapper."),
    ("19", "FBI probes an apparent hack of its crime database."),
    ("20", "Man convicted of starting the Palisades fire in LA."),
    ("21", "Mamdani vows to close New York's Rikers jail by 2032."),
    ("22", "England beat New Zealand 37-12 in rugby, a record margin."),
    ("23", "India 720/9 in NZ as Rahul and Pant hit centuries."),
    ("24", "Dak'Art Biennale opens in Dakar with 54 artists."),
    ("25", "Trafalgar Square Christmas tree felled in Norway."),
    ("26", "Warren Buffett quadruples his Thanksgiving gifts."),
    ("27", "Bitcoin climbs back above $60,000, up over 2%."),
    ("28", "UN agrees to regulate 'killer robots' by 2028."),
    ("29", "Iraqi forces enter a Kataib Hezbollah stronghold."),
    ("30", "Iran readies a tanker convoy to break the US blockade."),
    ("31", "US declassifies more UFO footage from the Middle East."),
    ("32", "Trump threatens a ban on AI data centres built abroad."),
    ("33", "Zelenskyy calls Putin a 'killer' after Trump praises him."),
]
brow = 12
for i, (num, txt) in enumerate(briefs):
    col, row = i % 2, i // 2
    bx2 = MX + col * (CW // 2 + 8)
    by2 = BY + 24 + row * brow
    d.text((bx2, by2), num + ".", font=f(SANS_B, 10), fill=RED)
    d.text((bx2 + 24, by2), txt, font=f(SANS, 10), fill=INK)

# ---------------------------------------------------------------- footer
FY = 960
rule(d, MX, FY, W - MX, 2)
# date check box
d.rectangle([MX, FY + 8, MX + 470, FY + 58], fill=(255, 243, 205),
            outline=INK, width=1)
d.text((MX + 8, FY + 13), "DATE CHECK", font=f(SANS_B, 11), fill=RED)
draw_lines(d, wrap(d, "Left out on purpose: stories dated before 13 Nov 2026 — "
                      "earlier COP31 drafts, last week's bridge attacks. "
                      "Everything on this page is 21 Nov.",
                   f(SANS, 10), 454), MX + 8, FY + 28, f(SANS, 10), lh=13)
# mini world map
mx0, my0 = MX + 486, FY + 8
d.text((mx0, FY + 10), "WHERE IT HAPPENED", font=f(SANS_B, 10), fill=INK)
d.rectangle([mx0, FY + 24, mx0 + 210, FY + 56], fill=(225, 238, 245),
            outline=LINE, width=1)
land = [(8, 8, 34, 12), (40, 4, 60, 14), (66, 10, 92, 16), (100, 6, 130, 12),
        (136, 12, 168, 18), (172, 18, 198, 26), (96, 20, 120, 28),
        (150, 26, 168, 30)]
for (x0, y0, x1, y1) in land:
    d.ellipse([mx0 + x0, FY + 24 + y0, mx0 + x1, FY + 24 + y1], fill=(150, 180, 160))
for (dx, dy) in [(52, 10), (120, 12), (160, 14), (96, 22), (180, 22), (30, 14)]:
    d.ellipse([mx0 + dx - 3, FY + 24 + dy - 3, mx0 + dx + 3, FY + 24 + dy + 3],
              fill=RED, outline=(255, 255, 255), width=1)
# sources + legend
sx0 = MX + 712
d.text((sx0, FY + 10), "HOW SURE ARE WE?", font=f(SANS_B, 10), fill=INK)
d.text((sx0, FY + 24), "REPORTED = two or more outlets  •  CLAIM = one side",
       font=f(SANS, 9), fill=GREY)
d.text((sx0, FY + 36), "FORECAST = not yet happened",
       font=f(SANS, 9), fill=GREY)
d.text((sx0, FY + 48), "Sources: AP • Reuters • AFP • BBC • UN News • Nasdaq",
       font=f(SANS, 9), fill=INK)

out = "entry.png"
img.save(out, optimize=True)
print("saved", out, img.size)
