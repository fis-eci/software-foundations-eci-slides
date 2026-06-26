#!/usr/bin/env python3
"""
build_presentations.py
Merges individual HTML slide files into single-file HTML presentations.

Run from the repository root:
    python build_presentations.py

Output files are written to the repository root:
    CVS-presentation.html
    OracleSQL-presentation.html
    PruebasUnitarias-presentation.html
"""

import os
import re

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))

DECKS = [
    {
        "folder": "CVS - MYSD & DOPO",
        "count":  16,
        "output": "CVS-presentation.html",
        "title":  "Control de Versiones — MYSD & DOPO",
    },
    {
        "folder": "Oracle SQL Developer - MYSD",
        "count":  11,
        "output": "OracleSQL-presentation.html",
        "title":  "Oracle SQL Developer — MYSD",
    },
    {
        "folder": "PostgreSQL VSC - MYSD",
        "count":  12,
        "output": "SQL-PostgreVSC-presentation.html",
        "title":  "PostgreSQL VSC — MYSD",
    },
    {
        "folder": "Pruebas Unitarias - DOPO",
        "count":  9,
        "output": "PruebasUnitarias-presentation.html",
        "title":  "Pruebas Unitarias en Java — DOPO",
    },
    {
        "folder": "Analisis Software Eclipse - DOPO",
        "count":  15,
        "output": "Analisis-Eclipse-presentation.html",
        "title":  "Análisis de Software Eclipse — DOPO",
    },
    {
        "folder": "Analisis Software VSC - DOPO",
        "count":  13,
        "output": "Analisis-VSC-presentation.html",
        "title":  "Análisis de Software VSC — DOPO",
    },
]

# Shell template uses __PLACEHOLDER__ tokens so no .format() escaping is needed.
# The iframe srcdoc approach gives each slide its own browsing context,
# guaranteeing complete CSS isolation — no class-name conflicts across slides.
SHELL = '''<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>__DECK_TITLE__</title>
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    html, body {
      width: 100%; height: 100%;
      background: #0a0a0a;
      overflow: hidden;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }

    /* Stage: the area above the nav bar where the slide lives */
    #stage {
      position: fixed;
      top: 0; left: 0; right: 0; bottom: 52px;
      overflow: hidden;
    }

    /* The iframe is positioned absolutely and scaled via JS transform */
    #slide-frame {
      position: absolute;
      top: 0; left: 0;
      width: 1280px;
      height: 720px;
      border: none;
      display: block;
      transform-origin: top left;
      /* transform is set dynamically by scaleSlide() */
    }

    /* Progress bar sits just above the nav bar */
    #progress-wrap {
      position: fixed;
      bottom: 52px; left: 0; right: 0;
      height: 3px;
      background: #21262d;
      z-index: 9998;
    }
    #progress-bar {
      height: 100%;
      background: #58a6ff;
      transition: width 0.2s ease;
    }

    /* Navigation bar */
    #nav-bar {
      position: fixed;
      bottom: 0; left: 0; right: 0;
      height: 52px;
      background: rgba(13, 17, 23, 0.97);
      border-top: 1px solid #30363d;
      display: flex;
      align-items: center;
      gap: 10px;
      padding: 0 14px;
      z-index: 9999;
    }

    .nbtn {
      background: #21262d;
      color: #c9d1d9;
      border: 1px solid #30363d;
      border-radius: 6px;
      padding: 5px 13px;
      font-size: 13px;
      cursor: pointer;
      transition: background 0.15s;
      flex-shrink: 0;
    }
    .nbtn:hover  { background: #30363d; }
    .nbtn:disabled { opacity: 0.3; cursor: default; }

    #counter {
      color: #8b949e;
      font-size: 13px;
      flex-shrink: 0;
      min-width: 52px;
      text-align: center;
    }

    #slide-title {
      color: #c9d1d9;
      font-size: 13px;
      flex: 1;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }

    #jump-wrap {
      display: flex;
      align-items: center;
      gap: 5px;
      flex-shrink: 0;
    }
    #jump-label { color: #8b949e; font-size: 12px; }
    #jump-input {
      background: #21262d;
      color: #c9d1d9;
      border: 1px solid #30363d;
      border-radius: 4px;
      padding: 3px 6px;
      font-size: 13px;
      width: 48px;
      text-align: center;
    }
    #jump-input:focus { outline: none; border-color: #58a6ff; }

    #btn-fs {
      background: transparent;
      color: #8b949e;
      border: 1px solid #30363d;
      border-radius: 6px;
      padding: 4px 10px;
      font-size: 15px;
      cursor: pointer;
      flex-shrink: 0;
    }
    #btn-fs:hover { color: #c9d1d9; background: #21262d; }

    .hint { color: #484f58; font-size: 11px; flex-shrink: 0; }
  </style>
</head>
<body>

  <div id="stage">
    <iframe id="slide-frame" srcdoc=""></iframe>
  </div>

  <div id="progress-wrap">
    <div id="progress-bar" style="width: 0%"></div>
  </div>

  <div id="nav-bar">
    <button class="nbtn" id="btn-prev">&#9664; Anterior</button>
    <span id="counter">1 / __COUNT__</span>
    <span id="slide-title">__DECK_TITLE__</span>
    <div id="jump-wrap">
      <span id="jump-label">Ir a:</span>
      <input id="jump-input" type="number" min="1" max="__COUNT__" value="1">
    </div>
    <button class="nbtn" id="btn-next">Siguiente &#9654;</button>
    <button id="btn-fs" title="Pantalla completa (F)">&#x26F6;</button>
    <span class="hint">&#8592; &#8594; &nbsp;Espacio</span>
  </div>

  <script>
    var SLIDES = [
      __SLIDES_JS__
    ];
    var TITLES = [__TITLES_JS__];
    var TOTAL  = SLIDES.length;
    var NAV_H  = 52 + 3; /* nav bar + progress bar */

    var frame    = document.getElementById('slide-frame');
    var counterEl = document.getElementById('counter');
    var titleEl  = document.getElementById('slide-title');
    var progEl   = document.getElementById('progress-bar');
    var btnPrev  = document.getElementById('btn-prev');
    var btnNext  = document.getElementById('btn-next');
    var jumpIn   = document.getElementById('jump-input');

    var cur = 0;

    function scaleSlide() {
      var stageW = window.innerWidth;
      var stageH = window.innerHeight - NAV_H;
      var s      = Math.min(stageW / 1280, stageH / 720);
      var offX   = (stageW - 1280 * s) / 2;
      var offY   = (stageH - 720  * s) / 2;
      frame.style.transform = 'translate(' + offX + 'px, ' + offY + 'px) scale(' + s + ')';
    }

    function goTo(n) {
      cur = Math.max(0, Math.min(n, TOTAL - 1));
      frame.srcdoc    = SLIDES[cur];
      counterEl.textContent = (cur + 1) + ' / ' + TOTAL;
      titleEl.textContent   = TITLES[cur] || '';
      progEl.style.width    = ((cur + 1) / TOTAL * 100) + '%';
      btnPrev.disabled = cur === 0;
      btnNext.disabled = cur === TOTAL - 1;
      jumpIn.value     = cur + 1;
      history.replaceState(null, '', '#' + (cur + 1));
    }

    btnNext.addEventListener('click', function() { goTo(cur + 1); });
    btnPrev.addEventListener('click', function() { goTo(cur - 1); });

    jumpIn.addEventListener('change', function() {
      var n = parseInt(this.value, 10);
      if (!isNaN(n)) goTo(n - 1);
    });
    jumpIn.addEventListener('keydown', function(e) {
      if (e.key === 'Enter') {
        var n = parseInt(this.value, 10);
        if (!isNaN(n)) goTo(n - 1);
        frame.focus();
      }
    });

    document.addEventListener('keydown', function(e) {
      if (document.activeElement === jumpIn) return;
      if (e.key === 'ArrowRight' || e.key === 'ArrowDown' || e.key === ' ') {
        e.preventDefault(); goTo(cur + 1);
      } else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
        e.preventDefault(); goTo(cur - 1);
      } else if (e.key === 'Home') {
        e.preventDefault(); goTo(0);
      } else if (e.key === 'End') {
        e.preventDefault(); goTo(TOTAL - 1);
      } else if (e.key === 'f' || e.key === 'F') {
        toggleFs();
      }
    });

    document.getElementById('btn-fs').addEventListener('click', toggleFs);

    function toggleFs() {
      if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen().catch(function() {});
      } else {
        document.exitFullscreen();
      }
    }

    window.addEventListener('resize', scaleSlide);
    window.addEventListener('fullscreenchange', scaleSlide);

    /* Restore slide from URL hash, default to slide 1 */
    var h = parseInt(location.hash.slice(1), 10);
    scaleSlide();
    goTo(isNaN(h) ? 0 : h - 1);
  </script>

</body>
</html>'''


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


def build_deck(deck: dict):
    folder = os.path.join(REPO_ROOT, deck['folder'])
    htmls, titles = [], []

    # Iterate in numeric order (not filesystem alphabetical order)
    for n in range(1, deck['count'] + 1):
        path = os.path.join(folder, f'{n}-slide.html')
        with open(path, encoding='utf-8') as f:
            raw = f.read()
        htmls.append(escape_js_template(raw))
        titles.append(extract_title(raw, f'Slide {n}'))

    slides_js = ',\n      '.join(f'`{h}`' for h in htmls)
    # Escape double quotes in titles to avoid breaking the JS string
    titles_js = ', '.join(f'"{t.replace(chr(34), chr(39))}"' for t in titles)

    out = (SHELL
           .replace('__DECK_TITLE__', deck['title'])
           .replace('__COUNT__',      str(deck['count']))
           .replace('__SLIDES_JS__',  slides_js)
           .replace('__TITLES_JS__',  titles_js))

    out_path = os.path.join(REPO_ROOT, deck['output'])
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(out)

    size_kb = len(out.encode('utf-8')) // 1024
    print(f'  Written: {deck["output"]}  ({size_kb} KB, {deck["count"]} slides)')


def verify(output: str, expected_count: int):
    path = os.path.join(REPO_ROOT, output)
    with open(path, encoding='utf-8') as f:
        content = f.read()

    # Count only the ones inside JS template literals (the outer shell adds one extra)
    # Match both `<!DOCTYPE html` and `<!doctype html` (case-insensitive)
    found = len(re.findall(r'`<!doctype html', content, re.IGNORECASE))
    assert found == expected_count, \
        f'Slide count mismatch in {output}: expected {expected_count}, found {found}'

    for marker in ['var SLIDES', 'var TITLES', 'goTo(', 'ArrowRight']:
        assert marker in content, f'Missing JS marker in {output}: {marker}'

    print(f'  Verified: {expected_count} slides embedded OK')


if __name__ == '__main__':
    for deck in DECKS:
        print(f'\nBuilding: {deck["title"]}')
        build_deck(deck)
        verify(deck['output'], deck['count'])

    print('\nAll presentations built successfully.')
    print('Open the .html files in a browser to view them.')
