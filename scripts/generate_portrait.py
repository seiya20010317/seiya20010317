#!/usr/bin/env python3
"""Generate the profile's detailed, self-typing ASCII cat mascot."""

import base64
import html
from pathlib import Path

# One complete mascot: party hat, ears, face, paws, body, feet, and tail.
# The second item chooses the restrained color role for each row.
ART = (
    ("             .  *  .", "accent"),
    ("                /\\", "accent"),
    ("               /  \\", "accent"),
    ("              /____\\", "accent"),
    ("             /______\\", "accent"),
    ("            /\\      /\\", "ink"),
    ("           /  \\____/  \\", "ink"),
    ("          /            \\", "ink"),
    ("         |    ^    ^    |", "ink"),
    ("      ---|      v       |---", "ink"),
    ("         |   \\______/   |", "ink"),
    ("          \\            /", "ink"),
    ("           `-.______.-'", "ink"),
    ("          __/|      |\\__", "ink"),
    ("        /`   |      |   `\\", "ink"),
    ("       (_    |      |    _)", "ink"),
    ("         `---|  /\\  |---'  )", "ink"),
    ("             (__)(__)  .-'", "ink"),
)

FONT_SIZE = 15.0
CHAR_WIDTH = FONT_SIZE * 0.6
LINE_HEIGHT = 17.0
ROW_DELAY = 0.075
ROW_DURATION = 0.54

LIGHT = {
    "ink": "#6e7681",
    "accent": "#bf3989",
}
DARK = {
    "ink": "#c9d1d9",
    "accent": "#f778ba",
}


def embedded_font() -> str:
    font = Path(__file__).parent / "fonts" / "jbmono-400.woff2"
    encoded = base64.b64encode(font.read_bytes()).decode("ascii")
    return (
        "@font-face{font-family:JBMono;font-style:normal;font-weight:400;"
        "font-display:block;src:url(data:font/woff2;base64,"
        f"{encoded}) format('woff2')}}"
    )


def theme(theme: dict[str, str]) -> str:
    return "".join(f".{name}{{fill:{color}}}" for name, color in theme.items())


def render() -> str:
    cols = max(len(line) for line, _ in ART)
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
        theme(LIGHT),
        f".cursor{{fill:{LIGHT['ink']}}}",
        "@media(prefers-color-scheme:dark){",
        theme(DARK),
        f".cursor{{fill:{DARK['ink']}}}",
        "}</style><defs>",
    ]

    geometry = []
    for index, (line, role) in enumerate(ART):
        y = index * LINE_HEIGHT
        x = (width - len(line) * CHAR_WIDTH) / 2
        line_width = len(line) * CHAR_WIDTH
        begin = index * ROW_DELAY
        geometry.append((line, role, x, y, line_width, begin))
        parts.append(
            f'<clipPath id="row-{index}"><rect x="{x:.2f}" y="{y:.2f}" '
            f'height="{LINE_HEIGHT:.2f}" width="0">'
            f'<animate attributeName="width" from="0" to="{line_width:.2f}" '
            f'begin="{begin:.3f}s" dur="{ROW_DURATION:.2f}s" '
            'fill="freeze"/></rect></clipPath>'
        )
    parts.append("</defs>")

    for index, (line, role, x, y, line_width, begin) in enumerate(geometry):
        end = begin + ROW_DURATION
        parts.append(
            f'<text xml:space="preserve" x="{x:.2f}" '
            f'y="{y + FONT_SIZE:.2f}" font-size="{FONT_SIZE}" class="{role}" '
            f'clip-path="url(#row-{index})">'
            f"{html.escape(line, quote=False)}</text>"
        )
        parts.append(
            f'<rect x="{x:.2f}" y="{y + 1:.2f}" width="2.2" '
            f'height="{FONT_SIZE:.2f}" class="cursor" opacity="0">'
            f'<animate attributeName="x" from="{x:.2f}" '
            f'to="{x + line_width:.2f}" begin="{begin:.3f}s" '
            f'dur="{ROW_DURATION:.2f}s" fill="freeze"/>'
            f'<set attributeName="opacity" to=".58" begin="{begin:.3f}s"/>'
            f'<set attributeName="opacity" to="0" begin="{end:.3f}s"/>'
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
