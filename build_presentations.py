#!/usr/bin/env python3
"""
build_presentations.py
Two steps, run from the repository root:

    python build_presentations.py           # sync design system + build decks
    python build_presentations.py --sync    # only refresh the slides in place

1. SYNC — every slide is a standalone HTML file. The shared design system
   (design-system/eci-slides.css, eci-slides.js and the ECI logo) is inlined
   into each slide between marker comments, so editing the design system and
   re-running this script updates all slides at once:

       <!--eci:head-->   fonts, icons, design-system CSS + JS
       <!--eci:frame-->  ambient background, ECI brand bar, footer, page number
       <!--eci:logo-->   full Escuela Colombiana de Ingeniería logo (SVG)
       <!--eci:emblem--> ECI emblem only (index.html)

2. BUILD — each deck folder is merged into one single-file presentation
   (one per entry in DECKS) with transitions, overview grid and navigation.
"""

import os
import re
import sys

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
DS_DIR = os.path.join(REPO_ROOT, 'design-system')

AUTHOR = 'Andersson David Sánchez Méndez'

DECKS = [
    {
        "folder":  "CVS - MYSD & DOPO",
        "count":   16,
        "output":  "CVS-presentation.html",
        "title":   "Control de Versiones — MYSD & DOPO",
        "short":   "Control de Versiones",
        "theme":   "cvs",
        "courses": ["MYSD", "DOPO"],
    },
    {
        "folder":  "Oracle SQL Developer - MYSD",
        "count":   11,
        "output":  "OracleSQL-presentation.html",
        "title":   "Oracle SQL Developer — MYSD",
        "short":   "Oracle SQL Developer",
        "theme":   "oracle",
        "courses": ["MYSD"],
    },
    {
        "folder":  "PostgreSQL VSC - MYSD",
        "count":   12,
        "output":  "SQL-PostgreVSC-presentation.html",
        "title":   "PostgreSQL en VS Code — MYSD",
        "short":   "PostgreSQL en VS Code",
        "theme":   "postgres",
        "courses": ["MYSD"],
    },
    {
        "folder":  "Pruebas Unitarias - DOPO",
        "count":   9,
        "output":  "PruebasUnitarias-presentation.html",
        "title":   "Pruebas Unitarias en Java — DOPO",
        "short":   "Pruebas Unitarias",
        "theme":   "junit",
        "courses": ["DOPO"],
    },
    {
        "folder":  "Analisis Software Eclipse - DOPO",
        "count":   15,
        "output":  "Analisis-Eclipse-presentation.html",
        "title":   "Análisis de Software en Eclipse — DOPO",
        "short":   "Análisis de Software · Eclipse",
        "theme":   "eclipse",
        "courses": ["DOPO"],
    },
    {
        "folder":  "Analisis Software VSC - DOPO",
        "count":   12,
        "output":  "Analisis-VSC-presentation.html",
        "title":   "Análisis de Software en VS Code — DOPO",
        "short":   "Análisis de Software · VS Code",
        "theme":   "vscode",
        "courses": ["DOPO"],
    },
]

FONTS = ('https://fonts.googleapis.com/css2?family=Inter:wght@300..900'
         '&family=JetBrains+Mono:wght@400;500;700&display=swap')
FONT_AWESOME = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css'


# --------------------------------------------------------------------------
# Design-system sync
# --------------------------------------------------------------------------

def read(path: str) -> str:
    with open(path, encoding='utf-8') as f:
        return f.read()


def minify_css(css: str) -> str:
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
    css = re.sub(r'\s+', ' ', css)
    css = re.sub(r'\s*([{};,>])\s*', r'\1', css)
    css = re.sub(r':\s+', ':', css)
    # `a:hover` style selectors survive; restore spaces needed inside values
    return css.replace(';}', '}').strip()


def minify_js(js: str) -> str:
    # Conservative: drop full-line and block comments, collapse indentation.
    js = re.sub(r'/\*.*?\*/', '', js, flags=re.S)
    lines = [ln.strip() for ln in js.splitlines()]
    return '\n'.join(ln for ln in lines if ln and not ln.startswith('//'))


def load_design_system() -> dict:
    css = minify_css(read(os.path.join(DS_DIR, 'eci-slides.css')))
    js = minify_js(read(os.path.join(DS_DIR, 'eci-slides.js')))
    head = (
        '<link rel="preconnect" href="https://fonts.googleapis.com">'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        f'<link href="{FONTS}" rel="stylesheet">'
        f'<link href="{FONT_AWESOME}" rel="stylesheet">'
        f'<style>{css}</style>'
        f'<script>{js}</script>'
    )
    return {
        'head':   head,
        'logo':   read(os.path.join(DS_DIR, 'eci-logo.svg')).strip(),
        'emblem': read(os.path.join(DS_DIR, 'eci-emblem.svg')).strip(),
    }


def frame_html(ds: dict, deck: dict, n: int) -> str:
    total = deck['count']
    pct = round(n / total * 100, 2)
    courses = ''.join(f'<span>{c}</span>' for c in deck['courses'])
    return (
        '<div class="bg" aria-hidden="true">'
        '<div class="aura x1"></div><div class="aura x2"></div><div class="aura x3"></div></div>'
        '<header class="top"><div class="brand">'
        f'<span class="emblem">{ds["emblem"]}</span>'
        '<span class="brand-name"><span>Escuela Colombiana de Ingeniería</span>'
        '<b>Julio Garavito</b></span></div></header>'
        f'<footer class="foot" style="--p:{pct}%">'
        f'<div class="foot-l"><span class="foot-author">{AUTHOR}</span><span class="dot"></span>'
        f'<span class="foot-course">{courses}</span><span class="dot"></span>'
        f'<span>{deck["short"]}</span></div>'
        f'<div class="foot-r"><span class="foot-num"><b>{n:02d}</b> / {total:02d}</span></div>'
        '<div class="foot-bar"></div></footer>'
    )


def fill_marker(html: str, name: str, content: str) -> str:
    pattern = re.compile(r'<!--eci:%s-->.*?<!--/eci:%s-->' % (name, name), re.S)
    return pattern.sub(lambda m: f'<!--eci:{name}-->{content}<!--/eci:{name}-->', html)


def sync_deck(ds: dict, deck: dict) -> int:
    folder = os.path.join(REPO_ROOT, deck['folder'])
    changed = 0
    for n in range(1, deck['count'] + 1):
        path = os.path.join(folder, f'{n}-slide.html')
        raw = read(path)
        out = fill_marker(raw, 'head', ds['head'])
        out = fill_marker(out, 'frame', frame_html(ds, deck, n))
        out = fill_marker(out, 'logo', ds['logo'])
        out = re.sub(r'(<body\b[^>]*\bdata-deck=")[^"]*(")', r'\g<1>%s\2' % deck['theme'], out)
        if out != raw:
            with open(path, 'w', encoding='utf-8', newline='\n') as f:
                f.write(out)
            changed += 1
    return changed


# --------------------------------------------------------------------------
# Presentation shell
# --------------------------------------------------------------------------

# Shell template uses __PLACEHOLDER__ tokens so no .format() escaping is needed.
# Each slide renders in its own iframe (srcdoc), guaranteeing complete CSS
# isolation. Two stacked iframes allow cross-fade transitions between slides.
SHELL = '''<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="__DECK_TITLE__ · Escuela Colombiana de Ingeniería Julio Garavito · IS-FUNDAMENTOS">
  <meta name="theme-color" content="#05070d">
  <title>__DECK_TITLE__ · ECI</title>
  <link rel="icon" href="data:image/svg+xml,__FAVICON__">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="__FONTS__" rel="stylesheet">
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    :root { --a: __ACCENT__; --red: #e63323; --line: rgba(255,255,255,.1); --ease: cubic-bezier(.2,.75,.1,1); }
    html, body { width: 100%; height: 100%; background: #000; overflow: hidden; color: #f5f5f7;
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; -webkit-font-smoothing: antialiased; }
    button { font: inherit; color: inherit; }

    #stage { position: fixed; inset: 0 0 64px 0; overflow: hidden; transition: bottom .5s var(--ease); }
    body.immersive #stage { bottom: 0; }
    .frame { position: absolute; top: 0; left: 0; width: 1280px; height: 720px; border: 0; display: block;
      transform-origin: top left; background: #05070d; border-radius: 6px;
      box-shadow: 0 40px 120px -20px rgba(0,0,0,.9), 0 0 0 1px rgba(255,255,255,.06);
      transition: opacity .55s var(--ease), filter .55s var(--ease); }
    .frame.out { opacity: 0; filter: blur(6px); pointer-events: none; }


    #bar { position: fixed; left: 0; right: 0; bottom: 0; height: 64px; z-index: 40;
      display: grid; grid-template-columns: 1fr auto 1fr; align-items: center; gap: 16px; padding: 0 18px;
      background: rgba(12,14,20,.72); -webkit-backdrop-filter: saturate(180%) blur(24px); backdrop-filter: saturate(180%) blur(24px);
      border-top: 1px solid var(--line); transition: transform .5s var(--ease), opacity .5s; }
    body.immersive #bar { transform: translateY(100%); opacity: 0; }
    body.immersive.peek #bar { transform: none; opacity: 1; }

    .who { display: flex; align-items: center; gap: 12px; min-width: 0; }
    .who svg { width: 26px; height: 25px; flex: none; color: #fff; }
    .who-t { display: flex; flex-direction: column; min-width: 0; line-height: 1.25; }
    .who-t b { font-size: 13.5px; font-weight: 650; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
    .who-t span { font-size: 12px; color: rgba(235,235,245,.55); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

    .ctl { display: flex; align-items: center; gap: 6px; padding: 5px; border-radius: 999px; background: rgba(255,255,255,.06); border: 1px solid var(--line); }
    .btn { height: 36px; min-width: 36px; padding: 0 12px; border: 0; border-radius: 999px; background: transparent; cursor: pointer;
      display: inline-flex; align-items: center; justify-content: center; gap: 6px; font-size: 13px; font-weight: 550; color: rgba(245,245,247,.86);
      transition: background .2s, color .2s, transform .2s var(--ease); }
    .btn:hover { background: rgba(255,255,255,.1); color: #fff; }
    .btn:active { transform: scale(.94); }
    .btn:disabled { opacity: .3; cursor: default; background: transparent; }
    .btn svg { width: 16px; height: 16px; }
    .btn:focus-visible, #jump:focus-visible { outline: 2px solid var(--a); outline-offset: 2px; }
    #count { font-variant-numeric: tabular-nums; font-size: 13px; color: rgba(235,235,245,.7); padding: 0 6px; display: flex; align-items: center; gap: 4px; }
    #jump { width: 34px; height: 26px; border-radius: 8px; border: 1px solid transparent; background: transparent; color: #fff; text-align: center;
      font: inherit; font-weight: 650; -moz-appearance: textfield; }
    #jump::-webkit-outer-spin-button, #jump::-webkit-inner-spin-button { -webkit-appearance: none; margin: 0; }
    #jump:hover, #jump:focus { border-color: var(--line); background: rgba(255,255,255,.06); }
    .right { display: flex; justify-content: flex-end; gap: 6px; align-items: center; }
    .hint { font-size: 11.5px; color: rgba(235,235,245,.4); margin-right: 6px; white-space: nowrap; }
    kbd { font-family: inherit; font-size: 10.5px; padding: 1px 5px; border-radius: 4px; border: 1px solid var(--line); background: rgba(255,255,255,.05); }

    #grid { position: fixed; inset: 0; z-index: 60; background: rgba(5,7,13,.9); -webkit-backdrop-filter: blur(30px); backdrop-filter: blur(30px);
      overflow-y: auto; padding: 72px 48px 48px; opacity: 0; visibility: hidden; transition: opacity .4s var(--ease), visibility .4s; }
    #grid.on { opacity: 1; visibility: visible; }
    #grid h2 { font-size: 28px; letter-spacing: -.02em; margin-bottom: 6px; }
    #grid p { color: rgba(235,235,245,.6); font-size: 14px; margin-bottom: 28px; }
    #grid .close { position: fixed; top: 20px; right: 24px; }
    .thumbs { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 22px; }
    .thumb { position: relative; aspect-ratio: 16/9; border-radius: 12px; overflow: hidden; cursor: pointer; border: 1px solid var(--line);
      background: #05070d; transition: transform .35s var(--ease), border-color .3s, box-shadow .35s; transform: translateY(12px); opacity: 0; }
    #grid.on .thumb { transform: none; opacity: 1; transition-delay: calc(var(--i) * 30ms); }
    .thumb:hover { transform: translateY(-4px) !important; border-color: var(--a); box-shadow: 0 20px 40px -20px var(--a); }
    .thumb.cur { border-color: var(--a); box-shadow: 0 0 0 2px var(--a); }
    .thumb iframe { position: absolute; top: 0; left: 0; width: 1280px; height: 720px; border: 0; transform-origin: top left; pointer-events: none; }
    .thumb span { position: absolute; left: 10px; bottom: 8px; font-size: 11.5px; font-weight: 650; padding: 3px 8px; border-radius: 6px;
      background: rgba(0,0,0,.65); -webkit-backdrop-filter: blur(8px); backdrop-filter: blur(8px); max-width: calc(100% - 20px);
      white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

    @media (max-width: 760px) {
      .hint, .who-t span, .btn .lbl { display: none; }
      #bar { grid-template-columns: auto 1fr auto; padding: 0 10px; gap: 8px; }
      .ctl { justify-self: center; }
      #grid { padding: 64px 16px 24px; }
      .thumbs { grid-template-columns: 1fr 1fr; gap: 12px; }
    }
    @media (prefers-reduced-motion: reduce) { * { transition: none !important; } }
  </style>
</head>
<body>
  <main id="stage" aria-live="polite">
    <iframe class="frame" id="fa" title="Diapositiva" tabindex="-1"></iframe>
    <iframe class="frame out" id="fb" title="Diapositiva" tabindex="-1"></iframe>
  </main>

  <nav id="bar" aria-label="Navegación de la presentación">
    <div class="who">
      __EMBLEM__
      <div class="who-t"><b>__DECK_TITLE__</b><span id="stitle"></span></div>
    </div>
    <div class="ctl">
      <button class="btn" id="prev" aria-label="Diapositiva anterior" title="Anterior (←)">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 18l-6-6 6-6"/></svg></button>
      <span id="count"><input id="jump" type="number" min="1" max="__COUNT__" value="1" aria-label="Ir a la diapositiva"> / __COUNT__</span>
      <button class="btn" id="next" aria-label="Diapositiva siguiente" title="Siguiente (→)">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 6l6 6-6 6"/></svg></button>
    </div>
    <div class="right">
      <span class="hint"><kbd>←</kbd> <kbd>→</kbd> navegar · <kbd>G</kbd> vista general · <kbd>F</kbd> pantalla completa</span>
      <button class="btn" id="btn-grid" aria-label="Vista general" title="Vista general (G)">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/></svg></button>
      <button class="btn" id="btn-fs" aria-label="Pantalla completa" title="Pantalla completa (F)">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M8 3H5a2 2 0 0 0-2 2v3M21 8V5a2 2 0 0 0-2-2h-3M3 16v3a2 2 0 0 0 2 2h3M16 21h3a2 2 0 0 0 2-2v-3"/></svg></button>
    </div>
  </nav>

  <section id="grid" aria-label="Vista general de diapositivas" aria-hidden="true">
    <button class="btn close" id="grid-close" aria-label="Cerrar vista general" title="Cerrar (Esc)">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M6 6l12 12M18 6L6 18"/></svg></button>
    <h2>__DECK_TITLE__</h2>
    <p>__COUNT__ diapositivas · Escuela Colombiana de Ingeniería Julio Garavito</p>
    <div class="thumbs" id="thumbs"></div>
  </section>

  <script>
    var SLIDES = [
      __SLIDES_JS__
    ];
    var TITLES = [__TITLES_JS__];
    var TOTAL = SLIDES.length;

    var stage = document.getElementById('stage');
    var frames = [document.getElementById('fa'), document.getElementById('fb')];
    var front = 0, cur = -1;
    var jump = document.getElementById('jump');
    var prev = document.getElementById('prev'), next = document.getElementById('next');
    var stitle = document.getElementById('stitle');
    var grid = document.getElementById('grid'), thumbs = document.getElementById('thumbs');

    function fit() {
      var r = stage.getBoundingClientRect();
      var pad = document.body.classList.contains('immersive') ? 0 : Math.min(28, r.width * .03);
      var s = Math.min((r.width - pad * 2) / 1280, (r.height - pad * 2) / 720);
      var x = (r.width - 1280 * s) / 2, y = (r.height - 720 * s) / 2;
      frames.forEach(function (f) { f.style.transform = 'translate(' + x + 'px,' + y + 'px) scale(' + s + ')'; });
    }

    function goTo(n) {
      n = Math.max(0, Math.min(n, TOTAL - 1));
      if (n === cur) return;
      cur = n;
      var back = frames[1 - front], shown = frames[front];
      back.onload = function () {
        back.onload = null;
        back.classList.remove('out'); shown.classList.add('out');
        front = 1 - front;
        setTimeout(function () { if (shown.classList.contains('out')) shown.removeAttribute('srcdoc'); }, 600);
      };
      back.srcdoc = SLIDES[n];
      jump.value = n + 1;
      stitle.textContent = TITLES[n] || '';
      document.title = (TITLES[n] ? TITLES[n] + ' · ' : '') + '__DECK_TITLE__';
      prev.disabled = n === 0; next.disabled = n === TOTAL - 1;
      history.replaceState(null, '', '#' + (n + 1));
      document.querySelectorAll('.thumb').forEach(function (t, i) { t.classList.toggle('cur', i === n); });
    }

    function buildGrid() {
      if (thumbs.children.length) return;
      SLIDES.forEach(function (html, i) {
        var t = document.createElement('div');
        t.className = 'thumb'; t.style.setProperty('--i', i); t.tabIndex = 0;
        t.setAttribute('role', 'button'); t.setAttribute('aria-label', 'Ir a la diapositiva ' + (i + 1));
        var f = document.createElement('iframe');
        f.setAttribute('data-static', ''); f.setAttribute('tabindex', '-1'); f.setAttribute('loading', 'lazy');
        f.title = TITLES[i] || ('Diapositiva ' + (i + 1));
        f.srcdoc = html;
        var l = document.createElement('span'); l.textContent = (i + 1) + ' · ' + (TITLES[i] || '');
        t.appendChild(f); t.appendChild(l);
        t.addEventListener('click', function () { toggleGrid(false); goTo(i); });
        t.addEventListener('keydown', function (e) { if (e.key === 'Enter') { toggleGrid(false); goTo(i); } });
        thumbs.appendChild(t);
      });
      scaleThumbs();
    }
    function scaleThumbs() {
      document.querySelectorAll('.thumb').forEach(function (t) {
        t.firstChild.style.transform = 'scale(' + (t.clientWidth / 1280) + ')';
      });
    }
    function toggleGrid(on) {
      if (on === undefined) on = !grid.classList.contains('on');
      if (on) buildGrid();
      grid.classList.toggle('on', on);
      grid.setAttribute('aria-hidden', on ? 'false' : 'true');
      document.querySelectorAll('.thumb').forEach(function (t, i) { t.classList.toggle('cur', i === cur); });
      if (on) { requestAnimationFrame(scaleThumbs); var c = thumbs.children[cur]; if (c) c.scrollIntoView({ block: 'center' }); }
    }

    function toggleFs() {
      if (!document.fullscreenElement) document.documentElement.requestFullscreen().catch(function () {});
      else document.exitFullscreen();
    }

    prev.addEventListener('click', function () { goTo(cur - 1); });
    next.addEventListener('click', function () { goTo(cur + 1); });
    document.getElementById('btn-fs').addEventListener('click', toggleFs);
    document.getElementById('btn-grid').addEventListener('click', function () { toggleGrid(); });
    document.getElementById('grid-close').addEventListener('click', function () { toggleGrid(false); });
    jump.addEventListener('change', function () { var v = parseInt(this.value, 10); if (!isNaN(v)) goTo(v - 1); });
    jump.addEventListener('keydown', function (e) { if (e.key === 'Enter') { this.blur(); } e.stopPropagation(); });

    function onKey(e) {
      if (e.target === jump) return;
      var k = e.key;
      if (grid.classList.contains('on')) { if (k === 'Escape' || k === 'g' || k === 'G') toggleGrid(false); return; }
      if (k === 'ArrowRight' || k === 'ArrowDown' || k === ' ' || k === 'PageDown') { e.preventDefault(); goTo(cur + 1); }
      else if (k === 'ArrowLeft' || k === 'ArrowUp' || k === 'PageUp') { e.preventDefault(); goTo(cur - 1); }
      else if (k === 'Home') { e.preventDefault(); goTo(0); }
      else if (k === 'End') { e.preventDefault(); goTo(TOTAL - 1); }
      else if (k === 'f' || k === 'F') toggleFs();
      else if (k === 'g' || k === 'G') toggleGrid(true);
    }
    document.addEventListener('keydown', onKey);
    /* Keys pressed while focus is inside a slide iframe */
    frames.forEach(function (f) { f.addEventListener('load', function () {
      try { f.contentWindow.addEventListener('keydown', onKey); } catch (e) {}
    }); });

    /* Swipe on touch screens */
    var sx = null;
    stage.addEventListener('touchstart', function (e) { sx = e.touches[0].clientX; }, { passive: true });
    stage.addEventListener('touchend', function (e) {
      if (sx === null) return; var dx = e.changedTouches[0].clientX - sx; sx = null;
      if (Math.abs(dx) > 50) goTo(cur + (dx < 0 ? 1 : -1));
    });

    /* Immersive mode: in fullscreen the bar hides and peeks on mouse move */
    var peekT;
    document.addEventListener('fullscreenchange', function () {
      document.body.classList.toggle('immersive', !!document.fullscreenElement); fit();
    });
    document.addEventListener('mousemove', function (e) {
      if (!document.body.classList.contains('immersive')) return;
      document.body.classList.toggle('peek', e.clientY > window.innerHeight - 90);
      clearTimeout(peekT); peekT = setTimeout(function () { document.body.classList.remove('peek'); }, 2200);
    });

    window.addEventListener('resize', function () { fit(); if (grid.classList.contains('on')) scaleThumbs(); });
    window.addEventListener('hashchange', function () { var h = parseInt(location.hash.slice(1), 10); if (!isNaN(h)) goTo(h - 1); });

    fit();
    var h = parseInt(location.hash.slice(1), 10);
    goTo(isNaN(h) ? 0 : h - 1);
  </script>
</body>
</html>'''

ACCENTS = {
    'cvs': '#58a6ff', 'oracle': '#00d4ff', 'postgres': '#4fc3f7',
    'junit': '#f89820', 'eclipse': '#f89820', 'vscode': '#2f9bff',
}


def escape_js_template(html: str) -> str:
    """Escape HTML for embedding inside a JS template literal (backtick string)."""
    html = html.replace('\\', '\\\\')   # must be first
    html = html.replace('`',  '\\`')
    html = html.replace('${', '\\${')
    # Prevent the HTML parser from closing the outer <script> block when it
    # encounters </script> inside a slide's embedded HTML string.
    # Using <\/script>: the outer HTML parser does not see this as </script>,
    # but JavaScript evaluates \/ as / so srcdoc receives the correct </script>.
    html = re.sub(r'</script', r'<\\/script', html, flags=re.IGNORECASE)
    return html


def extract_title(html: str, fallback: str) -> str:
    m = re.search(r'<title[^>]*>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
    return m.group(1).strip() if m else fallback


def favicon(emblem: str) -> str:
    svg = emblem.replace('fill="currentColor"', 'fill="#ffffff"')
    return (svg.replace('%', '%25').replace('#', '%23').replace('"', "'")
               .replace('<', '%3C').replace('>', '%3E'))


def build_deck(ds: dict, deck: dict):
    folder = os.path.join(REPO_ROOT, deck['folder'])
    htmls, titles = [], []

    # Iterate in numeric order (not filesystem alphabetical order)
    for n in range(1, deck['count'] + 1):
        raw = read(os.path.join(folder, f'{n}-slide.html'))
        htmls.append(escape_js_template(raw))
        titles.append(extract_title(raw, f'Diapositiva {n}'))

    slides_js = ',\n      '.join(f'`{h}`' for h in htmls)
    titles_js = ', '.join('"' + t.replace('\\', '').replace('"', "'") + '"' for t in titles)

    out = (SHELL
           .replace('__FAVICON__',    favicon(ds['emblem']))
           .replace('__EMBLEM__',     ds['emblem'])
           .replace('__FONTS__',      FONTS)
           .replace('__ACCENT__',     ACCENTS.get(deck['theme'], '#58a6ff'))
           .replace('__DECK_TITLE__', deck['title'])
           .replace('__COUNT__',      str(deck['count']))
           .replace('__TITLES_JS__',  titles_js)
           .replace('__SLIDES_JS__',  slides_js))   # last: slide HTML may contain tokens

    out_path = os.path.join(REPO_ROOT, deck['output'])
    with open(out_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(out)

    size_kb = len(out.encode('utf-8')) // 1024
    print(f'  Written: {deck["output"]}  ({size_kb} KB, {deck["count"]} slides)')


def verify(output: str, expected_count: int):
    content = read(os.path.join(REPO_ROOT, output))

    # Count only the ones inside JS template literals (the outer shell adds one extra)
    found = len(re.findall(r'`<!doctype html', content, re.IGNORECASE))
    assert found == expected_count, \
        f'Slide count mismatch in {output}: expected {expected_count}, found {found}'

    for marker in ['var SLIDES', 'var TITLES', 'goTo(', 'ArrowRight']:
        assert marker in content, f'Missing JS marker in {output}: {marker}'

    print(f'  Verified: {expected_count} slides embedded OK')


if __name__ == '__main__':
    ds = load_design_system()
    for deck in DECKS:
        changed = sync_deck(ds, deck)
        print(f'Synced design system: {deck["folder"]} ({changed} slides updated)')
    index = os.path.join(REPO_ROOT, 'index.html')
    page = read(index)
    synced = fill_marker(fill_marker(page, 'logo', ds['logo']), 'emblem', ds['emblem'])
    if synced != page:
        with open(index, 'w', encoding='utf-8', newline='\n') as f:
            f.write(synced)
        print('Synced design system: index.html')
    if '--sync' in sys.argv:
        sys.exit(0)

    for deck in DECKS:
        print(f'\nBuilding: {deck["title"]}')
        build_deck(ds, deck)
        verify(deck['output'], deck['count'])

    print('\nAll presentations built successfully.')
    print('Open the .html files in a browser to view them.')
