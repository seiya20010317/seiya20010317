#!/usr/bin/env python3
"""Turn a portrait photo into a self-typing, self-contained ASCII SVG.

This is a one-time/local generator. The scheduled workflow only refreshes
GitHub statistics, so the source photo never needs to be committed.

Pipeline:
  1. remove the background with rembg
  2. composite onto white
  3. preserve edges with a bilateral filter
  4. add local contrast with CLAHE
  5. darken mid-tones with the (v / 255) ** 1.7 curve
  6. map brightness to a 13-character ramp

Usage:
  python scripts/generate_portrait.py photo.jpg ascii.svg
"""

import argparse
import base64
import html
import io
from pathlib import Path
from typing import Optional, Tuple

import cv2
import numpy as np
from PIL import Image, ImageOps
from rembg import remove

RAMP = " .`:-=+*cs#%@"
FONT_SIZE = 12.9
CHAR_W = 7.74  # JetBrains Mono: exactly 0.600 em
LINE_H = 13.35
ROW_DELAY = 0.09
ROW_DURATION = 0.72
LIGHT = "#6e7681"
DARK = "#c9d1d9"


def background_removed_rgb(
    source: Path, crop: Optional[Tuple[int, int, int, int]] = None
) -> Image.Image:
    """Return a tightly cropped RGB subject on a clean white background."""
    original = ImageOps.exif_transpose(Image.open(source)).convert("RGBA")
    if crop:
        original = original.crop(crop)
    cutout = remove(original)
    if not isinstance(cutout, Image.Image):
        cutout = Image.open(io.BytesIO(cutout)).convert("RGBA")

    bbox = cutout.getchannel("A").getbbox()
    if bbox:
        left, top, right, bottom = bbox
        pad = round(max(right - left, bottom - top) * 0.04)
        left = max(0, left - pad)
        top = max(0, top - pad)
        right = min(cutout.width, right + pad)
        bottom = min(cutout.height, bottom + pad)
        cutout = cutout.crop((left, top, right, bottom))

    canvas = Image.new("RGBA", cutout.size, "white")
    return Image.alpha_composite(canvas, cutout).convert("RGB")


def character_rows(image: Image.Image, cols: int) -> list[str]:
    """Process the image and return the brightness-mapped text rows."""
    rgb = np.asarray(image)
    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
    gray = cv2.bilateralFilter(gray, 7, 45, 45)
    gray = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8)).apply(gray)
    # A gentler curve than the high-contrast cat source used previously:
    # it keeps skin open while retaining the glasses, brows, eyes, and lips.
    darkened = np.power(gray.astype(np.float32) / 255.0, 1.5) * 255.0

    height, width = darkened.shape
    rows = max(1, round(cols * (height / width) * 0.48))
    resized = cv2.resize(
        darkened, (cols, rows), interpolation=cv2.INTER_AREA
    )
    indexes = np.rint((255.0 - resized) / 255.0 * (len(RAMP) - 1)).astype(int)
    return ["".join(RAMP[i] for i in row) for row in indexes]


def font_rule(font_path: Path) -> str:
    encoded = base64.b64encode(font_path.read_bytes()).decode("ascii")
    return (
        "@font-face{font-family:JBMono;font-style:normal;font-weight:400;"
        "font-display:block;src:url(data:font/woff2;base64,"
        f"{encoded}) format('woff2')}}"
    )


def render_svg(rows: list[str], font_path: Path) -> str:
    width = len(max(rows, key=len, default="")) * CHAR_W
    height = len(rows) * LINE_H + 2
    family = (
        "JBMono,ui-monospace,SFMono-Regular,Menlo,Consolas,"
        "&apos;Liberation Mono&apos;,monospace"
    )
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:.1f}" '
        f'height="{height:.1f}" viewBox="0 0 {width:.1f} {height:.1f}" '
        f'font-family="{family}">',
        "<style>",
        font_rule(font_path),
        f".ink{{fill:{LIGHT}}}.cursor{{fill:{LIGHT}}}",
        "@media(prefers-color-scheme:dark){"
        f".ink{{fill:{DARK}}}.cursor{{fill:{DARK}}}}}",
        "</style>",
        "<defs>",
    ]

    for index, row in enumerate(rows):
        y = index * LINE_H
        row_width = max(CHAR_W, len(row) * CHAR_W)
        begin = index * ROW_DELAY
        parts.append(
            f'<clipPath id="row-{index}"><rect x="0" y="{y:.2f}" '
            f'height="{LINE_H:.2f}" width="0">'
            f'<animate attributeName="width" from="0" to="{row_width:.2f}" '
            f'begin="{begin:.2f}s" dur="{ROW_DURATION:.2f}s" '
            'fill="freeze"/></rect></clipPath>'
        )
    parts.append("</defs>")

    for index, row in enumerate(rows):
        if not row:
            continue
        y = index * LINE_H
        baseline = y + FONT_SIZE
        row_width = len(row) * CHAR_W
        begin = index * ROW_DELAY
        end = begin + ROW_DURATION
        safe = html.escape(row, quote=False)
        parts.append(
            f'<text xml:space="preserve" x="0" y="{baseline:.2f}" '
            f'font-size="{FONT_SIZE}" class="ink" '
            f'clip-path="url(#row-{index})">{safe}</text>'
        )
        parts.append(
            f'<rect x="0" y="{y + 1:.2f}" width="2.2" '
            f'height="{FONT_SIZE:.2f}" class="cursor" opacity="0">'
            f'<animate attributeName="x" from="0" to="{row_width:.2f}" '
            f'begin="{begin:.2f}s" dur="{ROW_DURATION:.2f}s" '
            'fill="freeze"/>'
            f'<set attributeName="opacity" to=".65" begin="{begin:.2f}s"/>'
            f'<set attributeName="opacity" to="0" begin="{end:.2f}s"/>'
            "</rect>"
        )

    parts.append("</svg>")
    return "".join(parts)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path, nargs="?", default=Path("ascii.svg"))
    parser.add_argument("--cols", type=int, default=90)
    parser.add_argument(
        "--crop",
        metavar="LEFT,TOP,RIGHT,BOTTOM",
        help="optional source crop in pixels, applied before background removal",
    )
    args = parser.parse_args()

    if args.cols < 40:
        parser.error("--cols must be at least 40")
    font_path = Path(__file__).parent / "fonts" / "jbmono-ramp.woff2"
    if not font_path.exists():
        raise SystemExit(f"missing embedded-font subset: {font_path}")

    crop = None
    if args.crop:
        try:
            crop = tuple(int(value) for value in args.crop.split(","))
        except ValueError:
            parser.error("--crop must contain four comma-separated integers")
        if len(crop) != 4 or crop[2] <= crop[0] or crop[3] <= crop[1]:
            parser.error("--crop must be LEFT,TOP,RIGHT,BOTTOM")

    portrait = character_rows(background_removed_rgb(args.source, crop), args.cols)
    blank = " " * (args.cols + 8)
    rows = [blank, blank]
    rows.extend(f"    {row}    " for row in portrait)
    rows.extend((blank, blank))
    svg = render_svg(rows, font_path)
    args.output.write_text(svg, encoding="utf-8")
    print(
        f"wrote {args.output}: {args.cols} columns, {len(rows)} rows, "
        f"{len(svg) / 1024:.1f} KB"
    )


if __name__ == "__main__":
    main()
