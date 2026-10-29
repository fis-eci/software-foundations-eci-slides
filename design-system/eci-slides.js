/* ECI Slides — motion layer. Inlined into every slide by build_presentations.py. */
(function () {
  'use strict';
  var root = document.documentElement;
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var frame = null;
  try { frame = window.frameElement; } catch (e) { /* cross-origin */ }
  var isStatic = reduce || /[?&#]static/.test(location.search + location.hash) || (frame && frame.hasAttribute('data-static'));

  function ready(fn) {
    if (document.readyState !== 'loading') fn();
    else document.addEventListener('DOMContentLoaded', fn);
  }

  /* Split headline text into words for a staggered 3D reveal.
     Element children (e.g. .grad spans) are wrapped whole so their own
     background-clip and animations keep working. */
  function splitWords(el) {
    var w = 0, nodes = Array.prototype.slice.call(el.childNodes);
    nodes.forEach(function (n) {
      if (n.nodeType === 3) {
        var parts = n.textContent.split(/(\s+)/), frag = document.createDocumentFragment();
        parts.forEach(function (p) {
          if (!p) return;
          if (/^\s+$/.test(p)) { frag.appendChild(document.createTextNode(p)); return; }
          var s = document.createElement('span');
          s.className = 'w'; s.style.setProperty('--w', w++); s.textContent = p;
          frag.appendChild(s);
        });
        el.replaceChild(frag, n);
      } else if (n.nodeType === 1 && n.tagName !== 'BR') {
        var s = document.createElement('span');
        s.className = 'w'; s.style.setProperty('--w', w++);
        el.replaceChild(s, n); s.appendChild(n);
      }
    });
  }

  /* Pointer-driven 3D tilt + spotlight on cards. */
  function tilt(card) {
    card.addEventListener('pointermove', function (e) {
      var r = card.getBoundingClientRect();
      var x = (e.clientX - r.left) / r.width, y = (e.clientY - r.top) / r.height;
      card.style.setProperty('--mx', (x * 100) + '%');
      card.style.setProperty('--my', (y * 100) + '%');
      card.style.transform = 'perspective(900px) rotateX(' + ((.5 - y) * 6) + 'deg) rotateY(' + ((x - .5) * 7) + 'deg) translateZ(6px)';
    });
    card.addEventListener('pointerleave', function () { card.style.transform = ''; });
  }

  /* Rotating 3D point sphere (Fibonacci lattice) for cover/closing slides. */
  function orb(canvas) {
    var ctx = canvas.getContext('2d'); if (!ctx) return;
    var cs = getComputedStyle(document.body);
    var c1 = cs.getPropertyValue('--a1').trim() || '#58a6ff';
    var c2 = cs.getPropertyValue('--a2').trim() || '#2ea44f';
    var dpr = Math.min(window.devicePixelRatio || 1, 2), W, H;
    var N = 520, pts = [], gold = Math.PI * (3 - Math.sqrt(5));
    for (var i = 0; i < N; i++) {
      var y = 1 - (i / (N - 1)) * 2, rad = Math.sqrt(1 - y * y), th = gold * i;
      pts.push([Math.cos(th) * rad, y, Math.sin(th) * rad, i % 7 === 0]);
    }
    var mx = 0, my = 0, t0 = performance.now();
    function size() {
      var r = canvas.getBoundingClientRect();
      W = r.width; H = r.height;
      canvas.width = W * dpr; canvas.height = H * dpr;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    }
    size();
    document.addEventListener('pointermove', function (e) {
      mx = (e.clientX / window.innerWidth - .5); my = (e.clientY / window.innerHeight - .5);
    });
    function draw(now) {
      var t = (now - t0) / 1000;
      var ay = t * .22 + mx * .9, ax = -.35 + my * .6;
      var R = Math.min(W, H) * .36, cx = W / 2, cy = H / 2;
      var sy = Math.sin(ay), cy_ = Math.cos(ay), sx = Math.sin(ax), cx_ = Math.cos(ax);
      ctx.clearRect(0, 0, W, H);
      /* equatorial rings */
      ctx.lineWidth = 1;
      for (var k = 0; k < 3; k++) {
        ctx.beginPath();
        for (var a = 0; a <= 64; a++) {
          var ang = a / 64 * Math.PI * 2, tilt = k * .9 + t * .05;
          var px = Math.cos(ang) * 1.18, py = Math.sin(ang) * 1.18 * Math.sin(tilt), pz = Math.sin(ang) * 1.18 * Math.cos(tilt);
          var x1 = px * cy_ + pz * sy, z1 = -px * sy + pz * cy_;
          var y1 = py * cx_ - z1 * sx, z2 = py * sx + z1 * cx_;
          var p = 2.6 / (2.6 + z2);
          var X = cx + x1 * R * p, Y = cy + y1 * R * p;
          if (a === 0) ctx.moveTo(X, Y); else ctx.lineTo(X, Y);
        }
        ctx.strokeStyle = k === 1 ? c2 : c1;
        ctx.globalAlpha = .18;
        ctx.stroke();
      }
      for (var i = 0; i < N; i++) {
        var P = pts[i];
        var x1 = P[0] * cy_ + P[2] * sy, z1 = -P[0] * sy + P[2] * cy_;
        var y1 = P[1] * cx_ - z1 * sx, z2 = P[1] * sx + z1 * cx_;
        var p = 2.6 / (2.6 + z2);
        var depth = (1 - z2) / 2;
        ctx.globalAlpha = .12 + depth * .85;
        ctx.fillStyle = P[3] ? c2 : c1;
        var s = (P[3] ? 2.4 : 1.5) * p;
        ctx.beginPath(); ctx.arc(cx + x1 * R * p, cy + y1 * R * p, s, 0, 6.2832); ctx.fill();
      }
      ctx.globalAlpha = 1;
      if (!isStatic) requestAnimationFrame(draw);
    }
    requestAnimationFrame(draw);
  }

  /* Count-up numbers: <span data-count="42">0</span> */
  function countUp(el) {
    var to = parseFloat(el.getAttribute('data-count')), dur = 1400, t0 = performance.now();
    if (isStatic) { el.textContent = to; return; }
    (function step(now) {
      var k = Math.min(1, (now - t0) / dur), e = 1 - Math.pow(1 - k, 3);
      el.textContent = Math.round(to * e);
      if (k < 1) requestAnimationFrame(step);
    })(t0);
  }

  ready(function () {
    if (isStatic) root.classList.add('static');
    document.querySelectorAll('[data-split]').forEach(splitWords);
    /* Stagger children of [data-stagger]; tag them for reveal */
    document.querySelectorAll('[data-stagger]').forEach(function (g) {
      var kind = g.getAttribute('data-stagger') || 'rv';
      Array.prototype.forEach.call(g.children, function (c) { c.classList.add(kind); });
    });
    var i = 0;
    document.querySelectorAll('.rv, .rv-x, .rv-z').forEach(function (el) { el.style.setProperty('--i', i++); });
    if (!isStatic) document.querySelectorAll('.card').forEach(tilt);
    document.querySelectorAll('[data-count]').forEach(countUp);
    var c = document.getElementById('orb'); if (c) orb(c);
    if (/qa/.test(location.hash)) (document.fonts ? document.fonts.ready : Promise.resolve()).then(function () { setTimeout(audit, 500); });
  });

  /* Layout audit (open a slide with #static-qa): reports elements that spill
     into the footer/outside the canvas or are clipped by their container. */
  function audit() {
    var out = [], foot = document.querySelector('.foot');
    var lim = foot ? foot.getBoundingClientRect().top : 720;
    function name(el) { return el.tagName.toLowerCase() + (el.className && el.className.baseVal === undefined ? '.' + String(el.className).trim().split(/\s+/).join('.') : '') + ' "' + (el.textContent || '').trim().slice(0, 40) + '"'; }
    document.querySelectorAll('.stage *, .cover-stage *, .top-meta *').forEach(function (el) {
      if (el.closest('svg') && el.tagName !== 'svg') return;
      var r = el.getBoundingClientRect(); if (!r.width || !r.height) return;
      if (el.id === 'orb') return;
      if (r.bottom > lim + 1 && !el.closest('.top-meta')) out.push('BOTTOM ' + Math.round(r.bottom - lim) + 'px ' + name(el));
      if (r.right > 1281 || r.left < -1) out.push('SIDE ' + name(el));
      var par = el.parentElement;
      if (par && !par.classList.contains('stage') && !par.classList.contains('cover-stage') && getComputedStyle(el).position === 'static' && getComputedStyle(par).display !== 'inline') {
        var pr = par.getBoundingClientRect();
        if (pr.height && r.bottom > pr.bottom + 5) out.push('SPILL ' + Math.round(r.bottom - pr.bottom) + 'px ' + name(el));
      }
      var cs = getComputedStyle(el);
      if ((cs.overflow === 'hidden' || cs.overflowY === 'hidden' || cs.overflowX === 'hidden') && el.tagName !== 'svg') {
        if (el.scrollHeight > el.clientHeight + 2) out.push('CLIP-Y ' + (el.scrollHeight - el.clientHeight) + 'px ' + name(el));
        if (el.scrollWidth > el.clientWidth + 2 && cs.textOverflow !== 'ellipsis') out.push('CLIP-X ' + (el.scrollWidth - el.clientWidth) + 'px ' + name(el));
      }
    });
    var seen = {}, uniq = out.filter(function (x) { return seen[x] ? false : (seen[x] = 1); });
    var pre = document.createElement('pre'); pre.id = 'qa-report'; pre.hidden = true;
    pre.textContent = JSON.stringify(uniq); document.body.appendChild(pre);
  }
})();
