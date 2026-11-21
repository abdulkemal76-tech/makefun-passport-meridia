#!/usr/bin/env python3
"""make.fun: The Passport Page of a Country That Isn't There.

Draws an invented passport spread for the Republic of Meridia
(a seafaring island nation) with PIL: a data page with a portrait
and machine-readable strip, and a visas page with arrival and
departure stamps from neighbouring countries plus a seafarer
endorsement. Deterministic, stdlib + Pillow only, no network.
Writes /output/entry.png (1024x1024, under 1 MiB).
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

NAVY = (31, 58, 77)
NAVY_SOFT = (58, 92, 116)
GOLD = (176, 141, 60)
PAGE = (237, 241, 244)
PAGE_EDGE = (210, 220, 228)
INK = (28, 45, 60)
GREY = (110, 126, 140)
BLUE = (43, 95, 163)
GREEN = (46, 125, 79)
PURPLE = (106, 76, 147)
RED = (163, 51, 39)
SKIN = (232, 185, 143)
SKIN_DARK = (214, 164, 122)
HAIR = (74, 50, 38)
JACKET = (38, 64, 92)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    try:
        return ImageFont.truetype(os.path.join(FONT_DIR, name), size)
    except OSError:
        return ImageFont.load_default()


F_TITLE = lambda s: font("DejaVuSans-Bold.ttf", s)  # noqa: E731
F_BODY = lambda s: font("DejaVuSans.ttf", s)  # noqa: E731
F_BOLD = lambda s: font("DejaVuSans-Bold.ttf", s)  # noqa: E731
F_MONO = lambda s: font("DejaVuSansMono.ttf", s)  # noqa: E731
F_SERIF_IT = lambda s: font("DejaVuSerif-Italic.ttf", s)  # noqa: E731


def guilloche(d, x0, y0, x1, y1, color, step=7, amp=3):
    """Faint wavy security lines across a page."""
    for yy in range(y0 + 14, y1 - 6, 26):
        pts = []
        for xx in range(x0 + 6, x1 - 4, step):
            pts.append((xx, yy + amp * math.sin((xx - x0) / 26.0)))
        d.line(pts, fill=color, width=1)


def emblem(d, cx, cy, r):
    """Coat of arms: ring, eight-point star, waves."""
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=GOLD, width=3)
    d.ellipse([cx - r + 6, cy - r + 6, cx + r - 6, cy + r - 6],
              outline=GOLD, width=1)
    for k in range(8):
        a = math.radians(k * 45)
        x1 = cx + int((r - 12) * math.cos(a))
        y1 = cy + int((r - 12) * math.sin(a))
        x2 = cx + int((r - 4) * math.cos(a + 0.28))
        y2 = cy + int((r - 4) * math.sin(a + 0.28))
        x3 = cx + int((r - 4) * math.cos(a - 0.28))
        y3 = cy + int((r - 4) * math.sin(a - 0.28))
        d.polygon([(cx, cy), (x1, y1), (x2, y2)], fill=GOLD)
        d.polygon([(cx, cy), (x1, y1), (x3, y3)], fill=GOLD)
    for k, yy in enumerate((cy + 10, cy + 16)):
        d.arc([cx - 16, yy - 6, cx + 16, yy + 6], 200, 340,
              fill=NAVY_SOFT, width=2)


def portrait(d, x0, y0, w, h):
    """Stylised official portrait: island woman, flat illustration."""
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(178, 193, 204))
    d.rectangle([x0, y0, x0 + w, y0 + h], outline=NAVY, width=2)
    cx = x0 + w // 2
    # shoulders / jacket
    d.pieslice([x0, y0 + h - 78, x0 + w, y0 + h + 30],
               180, 360, fill=JACKET)
    d.rectangle([x0, y0 + h - 26, x0 + w, y0 + h], fill=JACKET)
    # shirt + collar
    d.polygon([(cx - 14, y0 + h - 46), (cx, y0 + h - 26),
               (cx + 14, y0 + h - 46), (cx + 26, y0 + h - 60),
               (cx - 26, y0 + h - 60)], fill=(240, 240, 235))
    # neck
    d.rectangle([cx - 11, y0 + 96, cx + 11, y0 + 118], fill=SKIN_DARK)
    # hair back (bob)
    d.ellipse([cx - 36, y0 + 8, cx + 36, y0 + 104], fill=HAIR)
    # face
    d.ellipse([cx - 30, y0 + 22, cx + 30, y0 + 102], fill=SKIN)
    # hair fringe
    d.pieslice([cx - 32, y0 + 8, cx + 32, y0 + 66], 180, 360, fill=HAIR)
    d.polygon([(cx - 32, y0 + 44), (cx - 26, y0 + 18),
               (cx - 12, y0 + 38), (cx, y0 + 16),
               (cx + 12, y0 + 38), (cx + 26, y0 + 18),
               (cx + 32, y0 + 44), (cx + 30, y0 + 60),
               (cx + 18, y0 + 44), (cx, y0 + 52),
               (cx - 18, y0 + 44), (cx - 30, y0 + 60)], fill=HAIR)
    # brows, eyes, nose, mouth
    d.line([(cx - 20, y0 + 56), (cx - 8, y0 + 54)], fill=HAIR, width=2)
    d.line([(cx + 8, y0 + 54), (cx + 20, y0 + 56)], fill=HAIR, width=2)
    d.ellipse([cx - 18, y0 + 60, cx - 11, y0 + 65], fill=(30, 30, 30))
    d.ellipse([cx + 11, y0 + 60, cx + 18, y0 + 65], fill=(30, 30, 30))
    d.line([(cx, y0 + 66), (cx - 2, y0 + 80), (cx + 3, y0 + 81)],
           fill=SKIN_DARK, width=2)
    d.line([(cx - 8, y0 + 88), (cx + 8, y0 + 88)], fill=(150, 70, 60),
           width=2)
    # cheek shading
    d.ellipse([cx - 28, y0 + 72, cx - 16, y0 + 80], fill=(236, 172, 128))
    d.ellipse([cx + 16, y0 + 72, cx + 28, y0 + 80], fill=(236, 172, 128))


def field(d, x, y, label, value, vsize=17):
    d.text((x, y), label, font=F_BODY(11), fill=GREY)
    d.text((x, y + 14), value, font=F_BOLD(vsize), fill=INK)


def stamp(img, cx, cy, angle, color, lines, w=240, h=92):
    """A rotated rectangular border stamp pasted onto the spread."""
    layer = Image.new("RGBA", (w + 80, h + 80), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.rounded_rectangle([40, 40, 40 + w, 40 + h], radius=6,
                         outline=color + (255,), width=3)
    ld.line([40, 40 + 30, 40 + w, 40 + 30], fill=color + (255,), width=2)
    ld.text((40 + w // 2, 40 + 6), lines[0], font=F_BOLD(15),
            fill=color + (255,), anchor="mt")
    yy = 40 + 36
    for ln in lines[1:]:
        ld.text((40 + w // 2, yy), ln, font=F_BODY(12),
                fill=color + (255,), anchor="mt")
        yy += 17
    layer = layer.rotate(angle, resample=Image.BICUBIC, expand=False)
    img.paste(layer, (cx - (w + 80) // 2, cy - (h + 80) // 2), layer)


def round_stamp(d, cx, cy, r, color):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=3)
    d.ellipse([cx - r + 8, cy - r + 8, cx + r - 8, cy + r - 8],
              outline=color, width=1)
    d.text((cx, cy - 30), "DEPARTED", font=F_BOLD(13), fill=color,
           anchor="mt")
    d.text((cx, cy - 12), "PORT MERIDIA", font=F_BOLD(12), fill=color,
           anchor="mt")
    d.text((cx, cy + 6), "02 JUN 2025", font=F_BODY(13), fill=color,
           anchor="mt")
    d.text((cx, cy + 22), "*", font=F_BOLD(16), fill=color, anchor="mt")


def draw_spread():
    img = Image.new("RGB", (W, H), (58, 66, 74))
    d = ImageDraw.Draw(img)
    # desk shadow
    d.rectangle([24, 44, 1000, 980], fill=(40, 46, 52))
    # pages
    d.rectangle([32, 52, 500, 972], fill=PAGE)
    d.rectangle([524, 52, 992, 972], fill=PAGE)
    d.rectangle([500, 52, 524, 972], fill=(120, 130, 140))
    d.rectangle([32, 52, 500, 972], outline=PAGE_EDGE, width=2)
    d.rectangle([524, 52, 992, 972], outline=PAGE_EDGE, width=2)
    guilloche(d, 32, 52, 500, 972, (213, 222, 229))
    guilloche(d, 524, 52, 992, 972, (213, 222, 229))

    # ---------- LEFT PAGE: data page ----------
    emblem(d, 266, 108, 34)
    d.text((266, 152), "REPUBLIC OF MERIDIA", font=F_BOLD(25), fill=NAVY,
           anchor="mt")
    d.text((266, 182), "PASSPORT  \u2022  P  \u2022  MDI", font=F_BODY(13),
           fill=NAVY_SOFT, anchor="mt")
    d.line([52, 208, 480, 208], fill=GOLD, width=2)

    portrait(d, 60, 226, 140, 175)
    d.text((60, 408), "PHOTOGRAPH", font=F_BODY(10), fill=GREY)
    field(d, 222, 226, "TYPE", "P")
    field(d, 296, 226, "CODE", "MDI")
    field(d, 368, 226, "PASSPORT No.", "MD4829137", vsize=14)
    field(d, 222, 276, "SURNAME / NOM", "VOSS")
    field(d, 222, 326, "GIVEN NAMES / PR\u00c9NOMS", "ELENA MARA")
    field(d, 222, 376, "NATIONALITY / NATIONALIT\u00c9", "MERIDIAN")
    field(d, 60, 452, "DATE OF BIRTH / N\u00c9E LE", "14 MAR 1988")
    field(d, 300, 452, "SEX / SEXE", "F")
    field(d, 60, 502, "PLACE OF BIRTH / LIEU DE NAISSANCE",
          "PORT MERIDIA")
    field(d, 60, 552, "DATE OF ISSUE / D\u00c9LIVR\u00c9 LE", "02 JUN 2025")
    field(d, 300, 552, "DATE OF EXPIRY / EXPIRE LE", "02 JUN 2035")
    field(d, 60, 602, "AUTHORITY / AUTORIT\u00c9",
          "MERIDIAN PASSPORT OFFICE")
    d.text((60, 668), "HOLDER'S SIGNATURE / SIGNATURE DU TITULAIRE",
           font=F_BODY(11), fill=GREY)
    d.text((64, 686), "Elena Voss", font=F_SERIF_IT(24), fill=INK)
    d.line([60, 716, 320, 716], fill=INK, width=1)

    # machine-readable zone
    d.rectangle([52, 800, 480, 880], fill=(226, 232, 237))
    d.text((266, 812), "P<MDIVOSS<<ELENA<MARA<<<<<<<<<<<<<<<<<<<<<<<",
           font=F_MONO(14), fill=INK, anchor="mt")
    d.text((266, 836), "MD4829137<5MDI8803142F3506021<<<<<<<<<<<<<<02",
           font=F_MONO(14), fill=INK, anchor="mt")
    d.text((266, 892), "P<MDI  \u2022  MD4829137  \u2022  MERIDIA",
           font=F_BODY(11), fill=GREY, anchor="mt")

    # ---------- RIGHT PAGE: visas & stamps ----------
    d.text((758, 76), "VISAS", font=F_BOLD(24), fill=NAVY, anchor="mt")
    d.text((758, 106), "VISAS  \u2022  VISTOS", font=F_BODY(12),
           fill=NAVY_SOFT, anchor="mt")
    d.line([544, 132, 972, 132], fill=GOLD, width=2)

    stamp(img, 700, 210, -6, BLUE,
          ["SARN  \u2022  ARRIVAL", "UNITED ISLES OF SARN",
           "18 AUG 2025  \u2022  HARBOUR GATE 3"])
    stamp(img, 856, 300, 5, BLUE,
          ["SARN  \u2022  DEPARTURE", "UNITED ISLES OF SARN",
           "02 SEP 2025  \u2022  HARBOUR GATE 3"])
    stamp(img, 700, 420, 4, GREEN,
          ["VEYNE  \u2022  ARRIVAL", "DUCHY OF VEYNE",
           "11 MAR 2026  \u2022  NORTH FERRY"])
    stamp(img, 856, 510, -5, GREEN,
          ["VEYNE  \u2022  DEPARTURE", "DUCHY OF VEYNE",
           "28 MAR 2026  \u2022  NORTH FERRY"])
    stamp(img, 700, 620, -3, PURPLE,
          ["KESTREL  \u2022  ARRIVAL", "KESTREL REPUBLIC",
           "05 OCT 2026  \u2022  EAST PIER"])
    round_stamp(d, 872, 640, 62, RED)

    # seafarer endorsement: the telling detail
    d.rounded_rectangle([544, 730, 972, 902], radius=8,
                        outline=RED, width=2)
    d.text((758, 744), "ENDORSEMENT  \u2022  MENTION", font=F_BOLD(13),
           fill=RED, anchor="mt")
    d.text((758, 768),
           "SEAFARER: HOLDER IS LICENSED FOR CREW TRAVEL",
           font=F_BOLD(13), fill=INK, anchor="mt")
    d.text((758, 788),
           "ABOARD MERIDIAN-FLAGGED VESSELS ONLY.",
           font=F_BOLD(13), fill=INK, anchor="mt")
    d.text((758, 814),
           "NOT VALID FOR TRAVEL TO THE NORTHERN REACHES.",
           font=F_BODY(13), fill=INK, anchor="mt")
    d.text((758, 838),
           "FEE PAID: 40 MERIDIAN CROWNS  \u2022  STAMP DUTY 2 CR",
           font=F_BODY(12), fill=GREY, anchor="mt")
    d.text((758, 862),
           "TIDE-WAITS FOR NO ONE. - MERIDIAN HARBOUR CODE",
           font=F_SERIF_IT(12), fill=NAVY_SOFT, anchor="mt")

    d.text((512, 992), "REPUBLIC OF MERIDIA \u2014 INVENTED DOCUMENT",
           font=F_BODY(11), fill=(150, 160, 170), anchor="mt")
    return img


def main():
    os.makedirs("/output", exist_ok=True)
    img = draw_spread()
    img.save("/output/entry.png", format="PNG", optimize=True)
    print("saved /output/entry.png",
          os.path.getsize("/output/entry.png"), "bytes")


if __name__ == "__main__":
    main()
