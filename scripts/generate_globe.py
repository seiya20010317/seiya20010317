#!/usr/bin/env python3
"""Generate the continuously rotating globe used by the profile README."""

import base64
from pathlib import Path

WIDTH = 620
HEIGHT = 330
CX = 310
CY = 152
RADIUS = 112


def font_face() -> str:
    font = Path(__file__).parent / "fonts" / "jbmono-600.woff2"
    encoded = base64.b64encode(font.read_bytes()).decode("ascii")
    return (
        "@font-face{font-family:JBMono;font-style:normal;font-weight:600;"
        "font-display:block;src:url(data:font/woff2;base64,"
        f"{encoded}) format('woff2')}}"
    )


def render() -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}"
viewBox="0 0 {WIDTH} {HEIGHT}" fill="none">
<style>
{font_face()}
.ocean{{fill:url(#ocean-light)}}.land{{fill:url(#land-light)}}
.grid{{stroke:#ffffff;stroke-opacity:.22}}.atmosphere{{stroke:#54aeff}}
.orbit{{stroke:#8c959f}}.satellite{{fill:#57606a}}
.star{{fill:#8c959f}}.label{{fill:#57606a}}
@media(prefers-color-scheme:dark){{
 .ocean{{fill:url(#ocean-dark)}}.land{{fill:url(#land-dark)}}
 .grid{{stroke:#f0f6fc;stroke-opacity:.2}}.atmosphere{{stroke:#58a6ff}}
 .orbit{{stroke:#484f58}}.satellite{{fill:#c9d1d9}}
 .star{{fill:#8b949e}}.label{{fill:#c9d1d9}}
}}
</style>
<defs>
  <radialGradient id="ocean-light" cx="38%" cy="30%" r="72%">
    <stop offset="0" stop-color="#54aeff"/><stop offset=".55" stop-color="#218bff"/>
    <stop offset="1" stop-color="#0550ae"/>
  </radialGradient>
  <radialGradient id="ocean-dark" cx="38%" cy="30%" r="72%">
    <stop offset="0" stop-color="#79c0ff"/><stop offset=".52" stop-color="#1f6feb"/>
    <stop offset="1" stop-color="#0a3069"/>
  </radialGradient>
  <linearGradient id="land-light" x1="0" y1="0" x2="0" y2="1">
    <stop stop-color="#56d364"/><stop offset="1" stop-color="#1a7f37"/>
  </linearGradient>
  <linearGradient id="land-dark" x1="0" y1="0" x2="0" y2="1">
    <stop stop-color="#7ee787"/><stop offset="1" stop-color="#238636"/>
  </linearGradient>
  <clipPath id="globe-clip"><circle cx="{CX}" cy="{CY}" r="{RADIUS}"/></clipPath>
  <filter id="soft-glow" x="-40%" y="-40%" width="180%" height="180%">
    <feGaussianBlur stdDeviation="5" result="blur"/>
    <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <g id="continents">
    <path d="M18 96L39 75 70 66 101 75 123 96 111 116 88 122 72 143
      52 137 43 119 27 112Z"/>
    <path d="M83 142L107 148 123 169 115 190 102 222 88 204 78 174Z"/>
    <path d="M145 91L174 68 211 62 247 70 270 82 300 77 334 95
      322 113 293 122 268 111 241 127 215 122 202 139 177 129 157 110Z"/>
    <path d="M180 133L213 126 239 145 235 168 221 198 205 215
      189 190 177 158Z"/>
    <path d="M282 181L311 172 339 188 334 207 305 217 282 200Z"/>
    <path d="M118 73L130 55 147 63 142 79Z"/>
    <path d="M256 143L269 138 279 151 269 160Z"/>
  </g>
  <path id="orbit-path" d="M166 152C190 70 430 70 454 152
    C430 234 190 234 166 152Z"/>
</defs>

<!-- quiet star field -->
<g class="star">
  <circle cx="84" cy="67" r="2"><animate class="motion" attributeName="opacity"
    values=".2;.9;.2" dur="3.2s" repeatCount="indefinite"/></circle>
  <circle cx="128" cy="226" r="1.5"><animate class="motion" attributeName="opacity"
    values=".8;.15;.8" dur="4.4s" repeatCount="indefinite"/></circle>
  <circle cx="493" cy="75" r="2"><animate class="motion" attributeName="opacity"
    values=".25;1;.25" dur="3.8s" repeatCount="indefinite"/></circle>
  <circle cx="530" cy="213" r="1.5"><animate class="motion" attributeName="opacity"
    values=".9;.2;.9" dur="4.9s" repeatCount="indefinite"/></circle>
  <circle cx="92" cy="151" r="1"/><circle cx="548" cy="132" r="1"/>
  <circle cx="165" cy="42" r="1"/><circle cx="457" cy="257" r="1"/>
</g>

<!-- orbit sits behind the globe -->
<path d="M166 152C190 70 430 70 454 152" class="orbit"
  stroke-width="1" stroke-dasharray="4 7" opacity=".65"/>

<!-- sphere -->
<circle cx="{CX}" cy="{CY}" r="{RADIUS + 7}" class="atmosphere"
  stroke-width="2" opacity=".2" filter="url(#soft-glow)">
  <animate class="motion" attributeName="opacity" values=".16;.38;.16"
    dur="4s" repeatCount="indefinite"/>
</circle>
<circle cx="{CX}" cy="{CY}" r="{RADIUS}" class="ocean"/>

<!-- continuously wrapping world strip -->
<g clip-path="url(#globe-clip)" class="land">
  <g transform="translate(130 0)">
    <use href="#continents" x="0"/><use href="#continents" x="360"/>
    <animateTransform class="motion" attributeName="transform" type="translate"
      from="130 0" to="-230 0" dur="11s" repeatCount="indefinite"/>
  </g>
</g>

<!-- globe grid and specular highlight -->
<g clip-path="url(#globe-clip)" class="grid" stroke-width="1">
  <ellipse cx="{CX}" cy="{CY}" rx="{RADIUS}" ry="37"/>
  <ellipse cx="{CX}" cy="{CY}" rx="{RADIUS}" ry="76"/>
  <ellipse cx="{CX}" cy="{CY}" rx="43" ry="{RADIUS}"/>
  <ellipse cx="{CX}" cy="{CY}" rx="80" ry="{RADIUS}"/>
</g>
<ellipse cx="275" cy="112" rx="45" ry="68" fill="#ffffff" opacity=".08"
  transform="rotate(25 275 112)" clip-path="url(#globe-clip)"/>
<circle cx="{CX}" cy="{CY}" r="{RADIUS}" stroke="#ffffff"
  stroke-opacity=".34" stroke-width="1.5"/>

<!-- foreground orbit and moving satellite -->
<path d="M454 152C430 234 190 234 166 152" class="orbit"
  stroke-width="1" stroke-dasharray="4 7" opacity=".65"/>
<circle r="4" class="satellite">
  <animateMotion class="motion" dur="6.5s" repeatCount="indefinite"
    rotate="auto"><mpath href="#orbit-path"/></animateMotion>
</circle>

<text x="{CX}" y="302" text-anchor="middle" class="label"
  font-family="JBMono,ui-monospace,monospace" font-size="13"
  font-weight="600" letter-spacing="2">HELLO, WORLD.</text>
</svg>"""


def main() -> None:
    output = Path("earth.svg")
    svg = render()
    output.write_text(svg, encoding="utf-8")
    print(f"wrote {output}: {len(svg) / 1024:.1f} KB")


if __name__ == "__main__":
    main()
