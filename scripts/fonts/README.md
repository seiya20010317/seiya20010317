# Embedded typeface

[JetBrains Mono](https://github.com/JetBrains/JetBrainsMono) v2.304 is subset
by role and embedded directly into every generated SVG as a base64 WOFF2.
This prevents font-metric drift and avoids all external requests.

| file | weight | use |
|---|---:|---|
| `jbmono-head.woff2` | 600 | section labels |
| `jbmono-400.woff2` | 400 | chart labels |
| `jbmono-600.woff2` | 600 | chart values and globe label |

JetBrains Mono is licensed under the SIL Open Font License 1.1. See `OFL.txt`.
