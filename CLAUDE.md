# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Educational presentation slides for the Escuela Colombiana de Ingeniería (ECI). Each slide is a **standalone, self-contained HTML file** with embedded CSS — no build system, no JavaScript, no package manager. Open any `.html` file directly in a browser to view it.

Author: Andersson David Sánchez Méndez (Monitor MYSD & DOPO).

## Repository Structure

Three slide decks, each in its own folder:

- `CVS - MYSD & DOPO/` — 16 slides on Version Control Systems (Git/GitHub), GitHub Dark theme (green/blue)
- `Oracle SQL Developer - MYSD/` — 9 slides on Oracle SQL environments (server vs. local), neon cyan/orange theme
- `Pruebas Unitarias - DOPO/` — 11 slides on Unit Testing in Java (JUnit + BlueJ), blue/orange theme

## HTML Slide Architecture

Every slide follows the same pattern:

- **Fixed canvas**: `1280×720px` (16:9 presentation ratio), everything absolutely or flexbox-positioned inside it
- **Self-contained styling**: all CSS lives in a `<style>` block in `<head>` — no external stylesheets
- **CDN dependencies** (loaded at runtime):
  - Font Awesome 6.4.0 — icons
  - Google Fonts — Roboto, Roboto Mono, Orbitron, Montserrat, JetBrains Mono
- **No JavaScript** — purely HTML + CSS
- **Language**: `lang="es"` (Spanish content throughout)

### Common CSS Patterns

- CSS custom properties (`:root { --color-... }`) define the per-deck color palette
- Decorative elements (glowing dots, grid backgrounds, floating circles) are pure CSS
- Code snippets use `<pre>/<code>` with monospace fonts and dark backgrounds
- Footer strips contain author name, course badge, and slide number

### Per-Deck Design Themes

| Deck | Background | Primary accent | Secondary accent |
|---|---|---|---|
| CVS | `#0d1117` (GitHub dark) | `#58a6ff` (blue) | `#3fb950` (green) |
| Oracle SQL | `#0a0a1a` (deep navy) | `#00ffff` (cyan) | `#ff6b35` (orange) |
| Pruebas Unitarias | `#003366` (Java blue) | `#f89820` (orange) | `#4caf50` (green) |

## Working on Slides

- To add a new slide, copy the nearest existing slide in the same deck and edit the content — the visual structure and CSS palette are already set up.
- Absolute pixel values are intentional; the fixed 1280×720 canvas makes positioning predictable.
- External images referenced via `<img src="...">` should use stable CDN or data URIs to stay self-contained.
- Keep all CSS inside the file's `<style>` block — do not introduce external `.css` files.
