#!/usr/bin/env python3
"""cutout_maker.py — Mixed-media collage asset prep for VOX Interstellar v2.

Pillow + numpy only (no rembg on this machine). Three operations:

1. white_cutout: near-white background -> transparent alpha (soft edge),
   then trim the transparent border. Used for the AI images on #FFFFFF
   (watch / reel / trophy) so they sit as real paper cutouts.
2. halftone: portrait -> B&W newspaper halftone (bilevel dither, ink
   #081D31 on paper #F2ECE1). Used for Nolan / Thorne portraits.
3. torn_frame / polaroid: paste a photo onto a jagged torn-paper frame
   (#F4EFE6, 14-18px) with an offset red under-frame (#C9573C) and a
   soft drop shadow; Polaroid variant adds a white bottom caption strip.

Inputs : assets_raw/real/*.jpg, assets_raw/media-generation-*.webp
Outputs: public/assets/*.png (+ newspaper_bg.jpg)
Run    : python3 tools/cutout_maker.py
"""
import os
import random

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "assets_raw")
REAL = os.path.join(RAW, "real")
OUT = os.path.join(ROOT, "public", "assets")
os.makedirs(OUT, exist_ok=True)

PAPER = (244, 239, 230)   # #F4EFE6 torn edge
RED = (201, 87, 60)       # #C9573C offset under-frame
INK = (8, 29, 49)         # #081D31 halftone ink


def find_raw(prefix):
    for f in sorted(os.listdir(RAW)):
        if f.startswith(prefix) and f.endswith(".webp"):
            return os.path.join(RAW, f)
    raise FileNotFoundError(prefix)


def white_cutout(src, dst, hi=232, lo=210):
    """Near-white -> alpha 0, soft linear ramp between lo and hi.

    Two-stage: a soft ramp alpha (keeps enclosed white holes, e.g. the
    trophy wreath centre, transparent) PLUS a flood-fill from the four
    corners over near-white pixels (mn>240) that zeroes the white halo /
    soft drop-shadow fringe the ramp leaves around the subject.
    """
    from PIL import ImageDraw as _ID

    im = Image.open(src).convert("RGB")
    a = np.asarray(im).astype(np.float32)
    mn = a.min(axis=2)  # whitest channel decides
    alpha = np.clip((hi - mn) / max(hi - lo, 1), 0, 1) * 255
    # NOTE: do NOT zero alpha>250 here — solid subject pixels clip to
    # exactly 255, so that test would erase the whole subject.
    alpha = alpha.astype(np.uint8)
    # flood-fill the connected background (corners -> inwards)
    bg = Image.fromarray(np.where(mn > 205, 255, 0).astype(np.uint8))
    draw = _ID.Draw(bg)
    w, h = bg.size
    for xy in [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)]:
        if bg.getpixel(xy) == 255:
            _ID.floodfill(bg, xy, 128, thresh=0)
    flooded = np.asarray(bg) == 128
    alpha = np.where(flooded, 0, alpha).astype(np.uint8)
    # eat 1px of fringe, then soften the edge
    alpha_img = Image.fromarray(alpha).filter(ImageFilter.MinFilter(3))
    alpha_img = alpha_img.filter(ImageFilter.GaussianBlur(0.8))
    alpha = np.asarray(alpha_img)
    out = im.convert("RGBA")
    out.putalpha(Image.fromarray(alpha))
    bbox = out.getbbox()
    if bbox:
        out = out.crop(bbox)
    out.save(dst)
    print(f"cutout {os.path.basename(dst)} {out.size} "
          f"opaque={int((np.asarray(out)[:, :, 3] > 10).mean() * 100)}%")
    return out


def halftone(src, dst, width=900):
    """B&W newspaper halftone: dithered bilevel, ink on paper."""
    im = Image.open(src).convert("L")
    im = ImageOps.autocontrast(im, cutoff=1)
    w, h = im.size
    im = im.resize((width, int(h * width / w)), Image.LANCZOS)
    bw = im.convert("1")  # Floyd-Steinberg dither
    rgb = Image.new("RGB", bw.size, PAPER)
    px = rgb.load()
    bwp = bw.load()
    for y in range(bw.size[1]):
        for x in range(bw.size[0]):
            if bwp[x, y] == 0:
                px[x, y] = INK
    rgb.save(dst)
    print(f"halftone {os.path.basename(dst)} {rgb.size}")
    return rgb


def jagged_rect_mask(w, h, border, seed, jag=7):
    """Alpha mask: jagged torn rectangle inset by `border` from the edge."""
    rng = random.Random(seed)
    mask = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(mask)
    pts = []
    step = 46
    # top edge (left->right), right, bottom (right->left), left (bottom->top)
    x = border
    while x < w - border:
        pts.append((x, border + rng.randint(-jag, jag)))
        x += step
    y = border
    while y < h - border:
        pts.append((w - border + rng.randint(-jag, jag), y))
        y += step
    x = w - border
    while x > border:
        pts.append((x, h - border + rng.randint(-jag, jag)))
        x -= step
    y = h - border
    while y > border:
        pts.append((border + rng.randint(-jag, jag), y))
        y -= step
    d.polygon(pts, fill=255)
    return mask


def torn_frame(photo, dst, border=16, seed=1, polaroid=False, caption_h=0):
    """Photo on a jagged paper frame + offset red under-frame + shadow."""
    pw, ph = photo.size
    cap = caption_h if polaroid else 0
    fw, fh = pw + border * 2, ph + border * 2 + cap
    # red under-frame, offset down-right
    red_layer = Image.new("RGBA", (fw + 26, fh + 26), (0, 0, 0, 0))
    red_mask = jagged_rect_mask(fw, fh, 2, seed + 100)
    red_img = Image.new("RGBA", (fw, fh), RED + (255,))
    red_layer.paste(red_img, (14, 12), red_mask)
    # paper frame
    frame = Image.new("RGBA", (fw, fh), (0, 0, 0, 0))
    paper_mask = jagged_rect_mask(fw, fh, 2, seed)
    paper_img = Image.new("RGBA", (fw, fh), PAPER + (255,))
    frame.paste(paper_img, (0, 0), paper_mask)
    frame.paste(photo.convert("RGBA"), (border, border))
    # shadow: blurred black silhouette of the frame
    canvas = Image.new("RGBA", (fw + 60, fh + 60), (0, 0, 0, 0))
    shadow = Image.new("RGBA", (fw, fh), (8, 29, 49, 110))
    shadow.putalpha(paper_mask.point(lambda v: int(v * 0.55)))
    canvas.paste(shadow, (26, 30), shadow)
    canvas.alpha_composite(red_layer, (10, 8))
    canvas.alpha_composite(frame, (16, 14))
    bbox = canvas.getbbox()
    canvas = canvas.crop(bbox) if bbox else canvas
    canvas.save(dst)
    print(f"frame {os.path.basename(dst)} {canvas.size} "
          f"polaroid={polaroid}")
    return canvas


def fit(im, max_w, max_h):
    im.thumbnail((max_w, max_h), Image.LANCZOS)
    return im


def main():
    import argparse
    parser = argparse.ArgumentParser(description="VOX collage asset processor (cutout, halftone, torn frame, polaroid, newspaper)")
    parser.add_argument("--mode", choices=["cutout", "halftone", "torn", "polaroid", "newspaper"], required=True)
    parser.add_argument("--input", "-i", required=True, help="Source image path")
    parser.add_argument("--output", "-o", required=True, help="Destination image path")
    parser.add_argument("--max-w", type=int, default=900)
    parser.add_argument("--max-h", type=int, default=900)
    parser.add_argument("--border", type=int, default=16)
    parser.add_argument("--seed", type=int, default=11)
    parser.add_argument("--caption-h", type=int, default=96)
    args = parser.parse_args()

    os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
    if args.mode == "cutout":
        white_cutout(args.input, args.output)
    elif args.mode == "halftone":
        halftone(args.input, args.output)
    elif args.mode == "torn":
        im = Image.open(args.input).convert("RGB")
        torn_frame(fit(im, args.max_w, args.max_h), args.output, border=args.border, seed=args.seed, polaroid=False)
    elif args.mode == "polaroid":
        im = Image.open(args.input).convert("RGB")
        torn_frame(fit(im, args.max_w, args.max_h), args.output, border=args.border, seed=args.seed, polaroid=True, caption_h=args.caption_h)
    elif args.mode == "newspaper":
        news = Image.open(args.input).convert("RGB")
        news = ImageOps.autocontrast(news, cutoff=0.5)
        arr = np.asarray(news).astype(np.float32)
        arr[:, :, 0] = np.clip(arr[:, :, 0] * 1.02, 0, 255)
        arr[:, :, 2] = np.clip(arr[:, :, 2] * 0.88, 0, 255)
        news = Image.fromarray(arr.astype(np.uint8))
        news = ImageOps.fit(news, (1080, 1920), Image.LANCZOS)
        news.save(args.output, quality=88)
        print(f"texture {args.output} 1080x1920")


if __name__ == "__main__":
    main()
