# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Educational presentation slides for the Escuela Colombiana de Ingeniería (ECI). Each slide is a **standalone, self-contained HTML file** with embedded CSS — no package manager. Open any slide `.html` file directly in a browser to view it. `build_presentations.py` (Python 3, standard library only) merges each deck folder into a single-file presentation.

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
python build_presentations.py
```

Decks are declared in the `DECKS` list (folder, slide `count`, output file, title). When adding or removing a slide, update that deck's `count` and the slide counts in `README.md` and `index.html`, then rebuild. The built `*-presentation.html` files embed each slide in its own iframe and add JavaScript navigation — regenerate them instead of editing them by hand.

## HTML Slide Architecture

Every slide follows the same pattern:

- **Fixed canvas**: `1280×720px` (16:9 presentation ratio), everything absolutely or flexbox-positioned inside it
- **Self-contained styling**: all CSS lives in a `<style>` block in `<head>` — no external stylesheets
- **CDN dependencies** (loaded at runtime):
  - Font Awesome 6.4.0 — icons
  - Google Fonts — Roboto, Roboto Mono, Orbitron, Montserrat, JetBrains Mono, Fira Code
- **Mostly HTML + CSS** — a few slides include small inline scripts; navigation JavaScript is added only by the build
- **Language**: `lang="es"` (Spanish content throughout)

### Common CSS Patterns

- CSS custom properties (`:root { --color-... }`) define the per-deck color palette
- Decorative elements (glowing dots, grid backgrounds, floating circles) are pure CSS
- Code snippets use `<pre>/<code>` with monospace fonts and dark backgrounds
- Footer strips contain author name, course badge, and slide number

### Per-Deck Design Themes

| Deck | Background | Primary accent | Secondary accent | Tertiary |
|---|---|---|---|---|
| CVS | `#0d1117` (GitHub dark) | `#58a6ff` (blue) | `#2ea44f` (green) | — |
| Oracle SQL | `#0a0e27` (dark navy) | `#00d4ff` (cyan) | `#ff6b35` (orange) | `#00ff88` (green) |
| PostgreSQL VSC | `#0a0e1a` (deep navy) | `#4fc3f7` (cyan) | `#00ff88` (green) | `#ff6b35` (orange) |
| Pruebas Unitarias | `#003366` (Java blue) | `#f89820` (orange) | `#2e7d32` (green) | `#1565c0` (blue) |
| Análisis Eclipse | `#0d1117` (GitHub dark) | `#f89820` (orange) | `#58a6ff` (blue) | `#2ea44f` (green) |
| Análisis VS Code | `#0d1117` (GitHub dark) | `#007acc` (VS Code blue) | `#4fc3f7` (cyan) | `#2ea44f` (green) |

## Working on Slides

- To add a new slide, copy the nearest existing slide in the same deck and edit the content — the visual structure and CSS palette are already set up.
- Absolute pixel values are intentional; the fixed 1280×720 canvas makes positioning predictable.
- External images referenced via `<img src="...">` should use stable CDN or data URIs to stay self-contained.
- Keep all CSS inside the file's `<style>` block — do not introduce external `.css` files.
