#!/usr/bin/env python3
"""Generate the profile's self-typing, emoji-like ASCII cat.

The mascot is intentionally hand drawn instead of derived from a photograph:
it stays friendly at README scale, never crops awkwardly, and needs only the
Python standard library.
"""

import base64
import html
from pathlib import Path

ART = (
    "           *",
    "          /_\\",
    "         /___\\",
    "        /\\_/\\",
    "       ( ^.^ )",
    "        > ^ <",
    "       /|   |\\",
    "      (_|   |_)",
    "        /   \\",
    "       (__|__)",
)

FONT_SIZE = 16.0
CHAR_WIDTH = FONT_SIZE * 0.6
LINE_HEIGHT = 19.0
ROW_DELAY = 0.11
ROW_DURATION = 0.52
LIGHT = "#6e7681"
DARK = "#c9d1d9"


def embedded_font() -> str:
    font = Path(__file__).parent / "fonts" / "jbmono-400.woff2"
    encoded = base64.b64encode(font.read_bytes()).decode("ascii")
    return (
        "@font-face{font-family:JBMono;font-style:normal;font-weight:400;"
        "font-display:block;src:url(data:font/woff2;base64,"
        f"{encoded}) format('woff2')}}"
    )


def render() -> str:
    cols = max(len(line) for line in ART)
    width = cols * CHAR_WIDTH
    height = len(ART) * LINE_HEIGHT + 2
    family = (
        "JBMono,ui-monospace,SFMono-Regular,Menlo,Consolas,"
        "&apos;Liberation Mono&apos;,monospace"
    )
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:.1f}" '
        f'height="{height:.1f}" viewBox="0 0 {width:.1f} {height:.1f}" '
        f'font-family="{family}">',
        "<style>",
        embedded_font(),
        f".ink{{fill:{LIGHT}}}.cursor{{fill:{LIGHT}}}",
        "@media(prefers-color-scheme:dark){"
        f".ink{{fill:{DARK}}}.cursor{{fill:{DARK}}}}}",
        "</style><defs>",
    ]

    geometry = []
    for index, line in enumerate(ART):
        y = index * LINE_HEIGHT
        x = (width - len(line) * CHAR_WIDTH) / 2
        line_width = len(line) * CHAR_WIDTH
        begin = index * ROW_DELAY
        geometry.append((line, x, y, line_width, begin))
        parts.append(
            f'<clipPath id="row-{index}"><rect x="{x:.2f}" y="{y:.2f}" '
            f'height="{LINE_HEIGHT:.2f}" width="0">'
            f'<animate attributeName="width" from="0" to="{line_width:.2f}" '
            f'begin="{begin:.2f}s" dur="{ROW_DURATION:.2f}s" '
            'fill="freeze"/></rect></clipPath>'
        )
    parts.append("</defs>")

    for index, (line, x, y, line_width, begin) in enumerate(geometry):
        end = begin + ROW_DURATION
        parts.append(
            f'<text xml:space="preserve" x="{x:.2f}" '
            f'y="{y + FONT_SIZE:.2f}" font-size="{FONT_SIZE}" class="ink" '
            f'clip-path="url(#row-{index})">'
            f"{html.escape(line, quote=False)}</text>"
        )
        parts.append(
            f'<rect x="{x:.2f}" y="{y + 1:.2f}" width="2.4" '
            f'height="{FONT_SIZE:.2f}" class="cursor" opacity="0">'
            f'<animate attributeName="x" from="{x:.2f}" '
            f'to="{x + line_width:.2f}" begin="{begin:.2f}s" '
            f'dur="{ROW_DURATION:.2f}s" fill="freeze"/>'
            f'<set attributeName="opacity" to=".65" begin="{begin:.2f}s"/>'
            f'<set attributeName="opacity" to="0" begin="{end:.2f}s"/>'
            "</rect>"
        )

    parts.append("</svg>")
    return "".join(parts)


def main() -> None:
    output = Path("ascii.svg")
    svg = render()
    output.write_text(svg, encoding="utf-8")
    print(f"wrote {output}: {len(ART)} rows, {len(svg) / 1024:.1f} KB")


if __name__ == "__main__":
    main()
