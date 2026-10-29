# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Educational presentation slides for the Escuela Colombiana de Ingeniería (ECI). Each slide is a **standalone, self-contained HTML file** — a shared design system in `design-system/` is inlined into every slide by the build. No package manager. Open any slide `.html` file directly in a browser to view it. `build_presentations.py` (Python 3, standard library only) syncs the design system and merges each deck folder into a single-file presentation.

Author: Andersson David Sánchez Méndez (Monitor MYSD & DOPO).

Companion repository: [fis-eci/software-foundations-eci](https://github.com/fis-eci/software-foundations-eci) holds the full learning-unit material; each unit page there links to its deck here.

## Repository Structure

Six slide decks, each in its own folder, with one built presentation per deck in the repo root:

- `CVS - MYSD & DOPO/` — 16 slides on Version Control Systems (Git/GitHub) → `CVS-presentation.html`
- `Pruebas Unitarias - DOPO/` — 9 slides on Unit Testing in Java (JUnit + BlueJ) → `PruebasUnitarias-presentation.html`
- `Oracle SQL Developer - MYSD/` — 11 slides on Oracle SQL environments (server vs. local) → `OracleSQL-presentation.html`
- `PostgreSQL VSC - MYSD/` — 12 slides on PostgreSQL in VS Code → `SQL-PostgreVSC-presentation.html`
- `Analisis Software Eclipse - DOPO/` — 15 slides on software analysis in Eclipse → `Analisis-Eclipse-presentation.html`
- `Analisis Software VSC - DOPO/` — 12 slides on software analysis in VS Code → `Analisis-VSC-presentation.html`

`index.html` is the GitHub Pages landing page linking to every deck.

## Building

```bash
python build_presentations.py          # sync design system into every slide + build decks
python build_presentations.py --sync   # only sync the design system into the slides
```

Decks are declared in the `DECKS` list (folder, slide `count`, output file, title, `short` footer label, `theme`, `courses`). When adding or removing a slide, update that deck's `count` and the slide counts in `README.md` and `index.html`, then rebuild. The built `*-presentation.html` files embed each slide in its own iframe and add the presenter (transitions, `G` overview grid, swipe, immersive fullscreen) — regenerate them instead of editing them by hand.

## Design System

`design-system/` is the single source of truth for every slide:

- `eci-slides.css` — tokens, per-deck palettes (`body[data-deck]`), components, motion
- `eci-slides.js` — entrance choreography, 3D point sphere (`<canvas id="orb">`), card tilt, layout audit
- `eci-logo.svg` / `eci-emblem.svg` — official Escuela Colombiana de Ingeniería logo (Wikimedia Commons, CC BY-SA 4.0), recolorable via `currentColor`

The build inlines them into each slide between marker comments, so slides stay standalone:

- `<!--eci:head--><!--/eci:head-->` in `<head>`: fonts, Font Awesome, CSS, JS
- `<!--eci:frame--><!--/eci:frame-->` right after `<body>`: ambient background, ECI brand bar, footer (author, course, deck, page number, progress)
- `<!--eci:logo--><!--/eci:logo-->`: full ECI logo (covers and closings); `index.html` also uses `<!--eci:emblem-->`

Never edit content between markers — edit `design-system/` and rerun the build.

## HTML Slide Architecture

Every slide follows the same skeleton:

```html
<body class="slide" data-deck="cvs">            <!-- add "cover" for title/closing slides -->
<!--eci:frame--><!--/eci:frame-->
<div class="top-meta"><span class="chip on"><i class="fas fa-book-reader"></i>S1 · Teoría</span></div>
<main class="stage">
  <div class="head"><span class="kicker rv">S1: Teoría</span>
    <h1 class="h1" data-split>Título con <span class="grad">acento</span></h1></div>
  ...components...
</main>
```

- **Fixed canvas**: `1280×720px`; `.stage` sits between the 68px top bar and the 46px footer
- **Typography**: Inter (text) + JetBrains Mono (code, ligatures disabled so `<=` stays `<=`)
- **Components** (see the CSS for the full list): `.card` (+ `k1/k2/k3/kok/kwarn/kbad/kr`, `top-c`, `hl`, `tight`), `.ic`, `.list`, `.steps`/`.step`, `.flow`, `.code` + `.code-bar` + `pre` with `.k .t .s .f .n .c .a .g .p` highlight spans, `.note` (+ `tip/warn/bad/pause`), `.tag`, `.table`, `.link`, `.video`, `.dlg` (connection dialog mock), `.mini`, analysis tool colors `.t-sonar .t-pmd .t-jacoco .t-pit`
- **Motion**: `.rv`, `.rv-x`, `.rv-z` reveal in DOM order; `data-stagger` tags children; `data-split` animates headline words. `#static` in the URL (or `data-static` on the iframe) disables motion
- **Slide-specific CSS** goes in a small `<style>` after the `eci:head` marker. Classes used on `<a>` elements need a `.slide` prefix for `color` (`.slide a { color: inherit }`)
- **Language**: `lang="es"` (Spanish content throughout)

### Per-Deck Design Themes

| Deck | `data-deck` | Background | Primary accent | Secondary accent | Tertiary |
|---|---|---|---|---|---|
| CVS | `cvs` | `#05070d` | `#58a6ff` (blue) | `#2ea44f` (green) | `#a371f7` (violet) |
| Oracle SQL | `oracle` | `#050820` (navy) | `#00d4ff` (cyan) | `#ff6b35` (orange) | `#00ff88` (green) |
| PostgreSQL VSC | `postgres` | `#040814` (deep navy) | `#4fc3f7` (cyan) | `#00e58a` (green) | `#ff6b35` (orange) |
| Pruebas Unitarias | `junit` | `#031128` (Java blue) | `#f89820` (orange) | `#4caf50` (green) | `#4f8ff7` (blue) |
| Análisis Eclipse | `eclipse` | `#05070d` | `#f89820` (orange) | `#58a6ff` (blue) | `#2ea44f` (green) |
| Análisis VS Code | `vscode` | `#05070d` | `#2f9bff` (VS Code blue) | `#4fc3f7` (cyan) | `#2ea44f` (green) |

ECI institutional red `#e63323` is used for the brand and the progress bar on every deck.

## Working on Slides

- To add a new slide, copy the nearest existing slide in the same deck and edit the content inside `<main>`.
- Absolute pixel values are intentional; the fixed 1280×720 canvas makes positioning predictable.
- Verify layout by opening `N-slide.html#static-qa`: the design-system JS appends a hidden `<pre id="qa-report">` listing elements that spill into the footer, overflow the canvas, are clipped, or spill out of their container (an empty list `[]` means clean).
- External images should use stable CDNs (YouTube thumbnails: `https://i.ytimg.com/vi/<id>/hqdefault.jpg`) or data URIs.
- Keep shared styling in `design-system/`; do not add external `.css` files to slides.
