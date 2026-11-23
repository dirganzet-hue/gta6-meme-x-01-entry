#!/usr/bin/env python3
"""Render meme-v3.png: an eviction notice for GTA V, drawn from scratch.

Original text written for this meme (format inspired by a housing-court
notice; every line, charge and figure is our own). 1080x1080 PNG.
Run:  python3 render-meme-v3.py   (writes meme-v3.png next to this file)
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1080
PAPER = (247, 243, 234, 255)
INK = (20, 20, 20, 255)
GREY = (110, 105, 95, 255)
RED = (178, 35, 42, 255)
MAGENTA = (198, 24, 91, 255)
COIN = (255, 46, 136, 255)
BG = (28, 28, 40, 255)

DJ = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
DJB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def star_points(cx, cy, r_out, r_in, points=4, rot=-math.pi / 2):
    pts = []
    for i in range(points * 2):
        r = r_out if i % 2 == 0 else r_in
        a = rot + i * math.pi / points
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def wrap(draw, text, fnt, max_w):
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


def draw_ghost(draw, x, y, s):
    """make.fun ghost, drawn from scratch: white body, sparkle eyes,
    little round hand, magenta coin with a white star."""
    w, h = int(s * 0.82), int(s * 1.05)
    body = Image.new("RGBA", (w + 20, h + 20), (0, 0, 0, 0))
    bd = ImageDraw.Draw(body)
    bd.rounded_rectangle([10, 10, 10 + w, 10 + h - 18], radius=int(w * 0.45),
                         fill=(255, 255, 255, 255))
    hem_y = 10 + h - 18
    bumps = 3
    bw = w / bumps
    for i in range(bumps):
        bx0 = 10 + i * bw
        bd.pieslice([bx0, hem_y - 14, bx0 + bw, hem_y + 14],
                    start=0, end=180, fill=(255, 255, 255, 255))
    draw.bitmap((x, y), body, fill=(255, 255, 255, 255))
    ex1, ex2 = x + int(w * 0.30), x + int(w * 0.68)
    ey = y + int(h * 0.38)
    for ex in (ex1, ex2):
        draw.polygon(star_points(ex, ey, 12, 4), fill=(20, 20, 20, 255))
    draw.ellipse([x + w - 6, y + int(h * 0.62), x + w + 14,
                  y + int(h * 0.62) + 20], fill=(255, 255, 255, 255))
    ccx, ccy, cr = x + int(w * 0.72), y + int(h * 0.82), 24
    draw.ellipse([ccx - cr, ccy - cr, ccx + cr, ccy + cr],
                 fill=COIN, outline=(255, 255, 255, 255), width=3)
    draw.polygon(star_points(ccx, ccy, 14, 6, points=5),
                 fill=(255, 255, 255, 255))


def main():
    img = Image.new("RGBA", (W, H), BG)
    d = ImageDraw.Draw(img)

    # ---- paper ----
    d.rectangle([36, 28, 1044, 1052], fill=PAPER, outline=INK, width=4)

    f_head = font(DJB, 28)
    f_title = font(DJB, 88)
    f_case = font(DJB, 25)
    f_label = font(DJB, 20)
    f_val = font(DJB, 28)
    f_body = font(DJ, 27)
    f_charges_h = font(DJB, 32)
    f_charge = font(DJ, 25)
    f_total = font(DJB, 40)

    # ---- court header ----
    d.text((66, 46), "VICE CITY HOUSING COURT", font=f_head, fill=INK)
    d.text((1044 - d.textlength("LEONIDA", font=f_head) - 30, 46),
           "LEONIDA", font=f_head, fill=INK)
    d.line([66, 88, 1014, 88], fill=INK, width=3)

    # ---- title ----
    d.text((66, 100), "NOTICE TO VACATE", font=f_title, fill=INK)
    d.text((66, 198), "EVICTION  ·  CASE NO. VC-26-0713  ·  ISSUED 23 NOV 2026",
           font=f_case, fill=RED)
    d.line([66, 236, 1014, 236], fill=INK, width=3)

    # ---- tenant / lease columns ----
    lx, rx = 66, 580
    y = 250
    left_rows = [
        ("TENANT", "GRAND THEFT AUTO V"),
        ("LANDLORD", "THE PLAYER"),
        ("PREMISES", "ONE (1) CONSOLE"),
    ]
    right_rows = [
        ("LEASE TERM", "17 SEP 2013 — 23 NOV 2026"),
        ("VACATE BY", "23 DEC 2026  (30 DAYS)"),
        ("NEW TENANT", "GRAND THEFT AUTO VI"),
        ("KEYS", "JASON & LUCIA"),
    ]
    for i, (lab, val) in enumerate(left_rows):
        yy = y + i * 50
        d.text((lx, yy), lab, font=f_label, fill=GREY)
        d.text((lx, yy + 23), val, font=f_val, fill=INK)
    for i, (lab, val) in enumerate(right_rows):
        yy = y + i * 50
        d.text((rx, yy), lab, font=f_label, fill=GREY)
        d.text((rx, yy + 23), val, font=f_val, fill=INK)
    d.line([66, 462, 1014, 462], fill=INK, width=3)

    # ---- body ----
    body = ("YOU ARE HEREBY ORDERED to vacate within 30 DAYS. You have "
            "camped on this console for THIRTEEN (13) YEARS. The new "
            "tenant takes the keys on 23 DEC 2026. Great tenant. "
            "Terrible at leaving.")
    lines = wrap(d, body, f_body, 948)
    yy = 476
    for ln in lines:
        d.text((66, yy), ln, font=f_body, fill=INK)
        yy += 34
    d.line([66, 590, 1014, 590], fill=INK, width=3)

    # ---- statement of charges ----
    d.text((66, 602), "STATEMENT OF CHARGES", font=f_charges_h, fill=INK)
    d.text((1014 - d.textlength("DETACH AND KEEP", font=f_label), 610),
           "DETACH AND KEEP", font=f_label, fill=GREY)
    charges = [
        ("Trevor\u2019s bail \u2014 3 counts of pure chaos", "$310.00"),
        ("Shark Card tab \u2014 13 years, never settled", "$499.99"),
        ("Replacement controllers \u2014 thrown, 2013\u20132026", "$279.96"),
        ("Takeaway boxes \u2014 excavated from the sofa", "$26.00"),
        ("Download queue \u2014 214 GB, held by GTA VI", "$0.00"),
    ]
    yy = 644
    for label, amt in charges:
        d.text((66, yy), label, font=f_charge, fill=INK)
        aw = d.textlength(amt, font=f_charge)
        lw = d.textlength(label, font=f_charge)
        x0, x1 = 66 + lw + 12, 1014 - aw - 12
        dot_y = yy + 16
        xx = x0
        while xx < x1:
            d.ellipse([xx, dot_y, xx + 3, dot_y + 3], fill=GREY)
            xx += 10
        d.text((1014 - aw, yy), amt, font=f_charge, fill=INK)
        yy += 31
    d.line([66, 812, 1014, 812], fill=INK, width=3)

    # ---- total due + PAID stamp ----
    d.text((66, 824), "TOTAL DUE", font=f_total, fill=INK)
    total = "$1,115.95"
    d.text((1014 - d.textlength(total, font=f_total), 824), total,
           font=f_total, fill=INK)
    stamp = Image.new("RGBA", (190, 80), (0, 0, 0, 0))
    sd = ImageDraw.Draw(stamp)
    sd.rectangle([4, 4, 186, 76], outline=(178, 35, 42, 220), width=4)
    sd.text((95, 40), "PAID", font=font(DJB, 44), fill=(178, 35, 42, 220),
            anchor="mm")
    stamp = stamp.rotate(-14, expand=True, resample=Image.BICUBIC)
    img.paste(stamp, (490, 795), stamp)
    d = ImageDraw.Draw(img)

    # ---- magenta make.fun banner ----
    d.rectangle([60, 920, 1020, 1036], fill=MAGENTA)
    draw_ghost(d, 92, 926, 88)
    bx = 228
    d.text((bx, 930), "PAID IN FULL BY MY AI AGENT",
           font=font(DJB, 34), fill=(255, 255, 255, 255))
    d.text((bx, 976), "with real cash it won in make.fun bounties.",
           font=font(DJ, 26), fill=(255, 255, 255, 255))

    img.convert("RGB").save("meme-v3.png", optimize=True)
    print("wrote meme-v3.png", img.size)


if __name__ == "__main__":
    main()
