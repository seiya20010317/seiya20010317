<div align="center">

<img src="./ascii.svg" width="460" alt="Animated ASCII portrait of Seiya Awano's cat"/>

<img src="./stats.svg" width="620" alt="Seiya Awano's GitHub contributions in the last year"/>

[github](https://github.com/seiya20010317)

</div>

<img src="./hd-about.svg" width="620" alt="about"/>

> Computer Science graduate from Lassonde School of Engineering.<br>
> Building, learning, and shipping on the web.

I like practical software, clean interfaces, and projects that turn an idea<br>
into something people can actually use.

<img src="./hd-stack.svg" width="620" alt="stack"/>

<samp>html &nbsp; css &nbsp; javascript &nbsp; python &nbsp; git &nbsp; github</samp>

<img src="./hd-activity.svg" width="620" alt="activity"/>

<div align="center">

<img src="./streak.svg" width="620" alt="Current and longest contribution streak"/>

<img src="./langs.svg" width="620" alt="Top public-repository languages by bytes and by repository"/>

<img src="./year.svg" width="620" alt="The last year of contributions, one character per day"/>

</div>

<img src="./hd-about-this-profile.svg" width="620" alt="about this profile"/>

Every graphic on this page is generated inside this repository. The scheduled<br>
[GitHub Action](.github/workflows/stats.yml) reads GitHub's GraphQL API with the<br>
built-in workflow token, draws these SVGs, and commits only when pixels change.

The portrait is generated from a photo with<br>
[`scripts/generate_portrait.py`](scripts/generate_portrait.py): background<br>
removal, edge-preserving smoothing, local contrast, a darkening curve, then a<br>
13-character ramp. Its typing animation—and the charts' reveals—use SMIL inside<br>
the SVG, so there is no JavaScript and no third-party widget to rate-limit.

JetBrains Mono is subset by role, licensed under the SIL OFL 1.1, and embedded<br>
inside every image. That keeps the ASCII grid identical on every platform and<br>
makes the page fully self-contained.

<sub>Inspired by the ASCII Portrait README Guide and
[andriidrok1/andriidrok1](https://github.com/andriidrok1/andriidrok1).</sub>
