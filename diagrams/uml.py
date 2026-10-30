"""
uml.py — tiny UML renderer for the IS-FUNDAMENTOS design units.

Every diagram is declared in specs.py with explicit coordinates (the same
layout students reproduce in Astah). Each diagram renders to:

  out/<name>.svg       standalone, light theme (wiki + Astah reference)
  out/<name>.frag.svg  class-based markup themed by design-system CSS (slides)

Standard library only.
"""

import html
import math
import re

MONO_W = 0.6          # JetBrains Mono advance width (em)
NAME_W = 0.62         # Inter semibold, generous average (em)
FS = 12.5             # member font size
FS_NAME = 13.5        # class name font size
LINE = 17             # member line height
PAD = 10


def esc(s):
    return html.escape(str(s), quote=True)


def text_w(s, fs, w=MONO_W):
    return len(s.lstrip('*_')) * fs * w


def member(s, x, y):
    """Member line. Prefixes: '*' new in this version (highlighted), '_' static (underlined)."""
    new = '*' in s[:2]
    static = '_' in s[:2]
    body = s.lstrip('*_')
    return '<text class="u-mem%s" x="%.1f" y="%.1f" xml:space="preserve"%s>%s</text>' % (
        ' u-new' if new else '', x, y, ' text-decoration="underline"' if static else '', esc(body))


# ---------------------------------------------------------------------------
# Geometry helpers
# ---------------------------------------------------------------------------

def clip(box, p, origin=None):
    """Point where the ray from origin (default: centre) towards p leaves the box."""
    x, y, w, h = box
    cx, cy = origin if origin else (x + w / 2, y + h / 2)
    if origin:
        # distance to each side from the (shifted) origin
        dx, dy = p[0] - cx, p[1] - cy
        ts = []
        if dx > 0: ts.append((x + w - cx) / dx)
        if dx < 0: ts.append((x - cx) / dx)
        if dy > 0: ts.append((y + h - cy) / dy)
        if dy < 0: ts.append((y - cy) / dy)
        t = min(t for t in ts if t >= 0) if ts else 0
        return cx + dx * t, cy + dy * t
    dx, dy = p[0] - cx, p[1] - cy
    if dx == 0 and dy == 0:
        return cx, cy
    tx = (w / 2) / abs(dx) if dx else math.inf
    ty = (h / 2) / abs(dy) if dy else math.inf
    t = min(tx, ty)
    return cx + dx * t, cy + dy * t


def unit(a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]
    d = math.hypot(dx, dy) or 1
    return dx / d, dy / d


# ---------------------------------------------------------------------------
# Diagram
# ---------------------------------------------------------------------------

class Diagram:
    def __init__(self, name, w, h, title=''):
        self.name, self.w, self.h, self.title = name, w, h, title
        self.nodes = {}
        self.parts = []      # (z, svg) — edges first, nodes on top
        self.edges = []

    # ----- nodes -------------------------------------------------------------
    def cls(self, key, x, y, name=None, attrs=(), ops=(), stereo=None, tone='n',
            w=None, underline=False, italic=False, note=None, compact=False):
        """Class / object / table box. tone: n (neutral) or k1..k5 header tint."""
        name = name or key
        lines_a = list(attrs)
        lines_o = list(ops)
        width = max([text_w(name, FS_NAME, NAME_W)] +
                    ([text_w('«%s»' % stereo, 11.5, NAME_W)] if stereo else []) +
                    [text_w(s, FS) for s in lines_a + lines_o]) + 2 * PAD + 6
        width = max(width, 96) if w is None else w
        head_h = 26 + (14 if stereo else 0)
        a_h = (len(lines_a) * LINE + 10) if (lines_a or not compact) else 0
        o_h = (len(lines_o) * LINE + 10) if lines_o else (0 if compact else 8)
        h = head_h + a_h + o_h
        self.nodes[key] = (x, y, width, h)
        g = ['<g class="u-node u-%s">' % tone,
             '<rect class="u-box" x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="4"/>' % (x, y, width, h),
             '<path class="u-head" d="M%.1f %.1f h%.1f v%.1f h-%.1f z"/>' % (x + .5, y + .5, width - 1, head_h - .5, width - 1)]
        ty = y + 17
        if stereo:
            g.append('<text class="u-stereo" x="%.1f" y="%.1f" text-anchor="middle">«%s»</text>' % (x + width / 2, ty - 1, esc(stereo)))
            ty += 14
        deco = ' text-decoration="underline"' if underline else ''
        ital = ' font-style="italic"' if italic else ''
        g.append('<text class="u-name" x="%.1f" y="%.1f" text-anchor="middle"%s%s>%s</text>' % (x + width / 2, ty + 1, deco, ital, esc(name)))
        yy = y + head_h
        if a_h:
            g.append('<line class="u-sep" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>' % (x, yy, x + width, yy))
            for i, s in enumerate(lines_a):
                g.append(member(s, x + PAD, yy + 17 + i * LINE))
            yy += a_h
        if lines_o or not compact:
            g.append('<line class="u-sep" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>' % (x, yy, x + width, yy))
            for i, s in enumerate(lines_o):
                g.append(member(s, x + PAD, yy + 17 + i * LINE))
        g.append('</g>')
        self.parts.append((2, ''.join(g)))
        if note:
            self.note(x, y + h + 8, note, w=width)
        return self

    def actor(self, key, x, y, name):
        """Stick figure; (x, y) is the head centre."""
        self.nodes[key] = (x - 22, y - 12, 44, 72)
        self.parts.append((2,
            '<g class="u-actor"><circle cx="%.1f" cy="%.1f" r="9"/>'
            '<path d="M%.1f %.1f v24 M%.1f %.1f h30 M%.1f %.1f l-12 18 M%.1f %.1f l12 18"/>'
            '<text class="u-label" x="%.1f" y="%.1f" text-anchor="middle">%s</text></g>'
            % (x, y, x, y + 9, x - 15, y + 17, x, y + 33, x, y + 33, x, y + 66, esc(name))))
        return self

    def usecase(self, key, x, y, name, w=150, h=48, tone='k1'):
        self.nodes[key] = (x, y, w, h)
        self.parts.append((2,
            '<g class="u-node u-%s"><ellipse class="u-box u-uc" cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f"/>'
            '<text class="u-name" x="%.1f" y="%.1f" text-anchor="middle">%s</text></g>'
            % (tone, x + w / 2, y + h / 2, w / 2, h / 2, x + w / 2, y + h / 2 + 5, esc(name))))
        return self

    def package(self, key, x, y, w, h, name, tone='k1', body=''):
        self.nodes[key] = (x, y, w, h)
        self.parts.append((1,
            '<g class="u-node u-%s"><path class="u-box" d="M%.1f %.1f h%.1f v-18 h-%.1f z"/>'
            '<rect class="u-box u-pkg" x="%.1f" y="%.1f" width="%.1f" height="%.1f"/>'
            '<path class="u-head" d="M%.1f %.1f h%.1f v-17 h-%.1f z"/>'
            '<text class="u-name" x="%.1f" y="%.1f">%s</text>%s</g>'
            % (tone, x, y, 120, 120, x, y, w, h, x + .5, y, 119, 119, x + 10, y - 4, esc(name), body)))
        return self

    def note(self, x, y, text, w=200):
        lines = text.split('\n')
        h = len(lines) * 16 + 14
        self.parts.append((3,
            '<g class="u-note"><path d="M%.1f %.1f h%.1f l10 10 v%.1f h-%.1f z"/>%s</g>'
            % (x, y, w - 10, h - 10, w, ''.join(
                '<text class="u-mem" x="%.1f" y="%.1f">%s</text>' % (x + 9, y + 18 + i * 16, esc(l)) for i, l in enumerate(lines)))))
        return self

    def tag(self, x, y, text, tone='k1'):
        """Rounded label pill (e.g. table names over a conceptual model)."""
        w = text_w(text, 12, NAME_W) + 18
        self.parts.append((3,
            '<g class="u-tag u-%s"><rect x="%.1f" y="%.1f" width="%.1f" height="22" rx="11"/>'
            '<text x="%.1f" y="%.1f" text-anchor="middle">%s</text></g>' % (tone, x, y, w, x + w / 2, y + 15.5, esc(text))))
        return self

    def text(self, x, y, s, cls='u-label', anchor='start'):
        self.parts.append((3, '<text class="%s" x="%.1f" y="%.1f" text-anchor="%s">%s</text>' % (cls, x, y, anchor, esc(s))))
        return self

    # ----- edges -------------------------------------------------------------
    def edge(self, a, b, kind='assoc', ra='', ma='', rb='', mb='', label='', arrow='',
             via=(), da=(0, 0), db=(0, 0), lpos=.5, loff=(0, -8), aclass=None, flip=False):
        """kind: assoc | nav (open arrow at b) | comp (diamond at a) | agg | gen (triangle at b)
                 | dep (dashed, open arrow at b) | link (object link) | fk (table reference)"""
        A, B = self.nodes[a], self.nodes[b]
        ca = (A[0] + A[2] / 2 + da[0], A[1] + A[3] / 2 + da[1])
        cb = (B[0] + B[2] / 2 + db[0], B[1] + B[3] / 2 + db[1])
        pts_mid = list(via)
        first_t = pts_mid[0] if pts_mid else cb
        last_f = pts_mid[-1] if pts_mid else ca
        pa = clip(A, first_t if pts_mid else cb, ca) if not pts_mid else self._clip_from(A, da, first_t)
        pb = clip(B, last_f if pts_mid else ca, cb) if not pts_mid else self._clip_from(B, db, last_f)
        pts = [pa] + pts_mid + [pb]
        dashed = kind in ('dep', 'real')
        d = 'M' + ' L'.join('%.1f %.1f' % p for p in pts)
        out = ['<path class="u-edge%s" d="%s"/>' % (' u-dash' if dashed else '', d)]
        # end decorations
        ub = unit(pts[-2], pts[-1])
        ua = unit(pts[1], pts[0])
        if kind in ('nav', 'dep', 'fk'):
            out.append(self._open_arrow(pb, ub))
        if kind == 'gen':
            out.append(self._triangle(pb, ub))
        if kind in ('comp', 'agg'):
            out.append(self._diamond(pa, unit(pts[0], pts[1]), filled=(kind == 'comp')))
        # end labels
        if ra or ma:
            out.append(self._end_labels(pa, ua, ra, ma, flip))
        if rb or mb:
            out.append(self._end_labels(pb, ub, rb, mb, not flip))
        # association name
        if label:
            seg = self._point_at(pts, lpos)
            s = esc(label)
            if arrow == '>':
                s += ' ▶'
            elif arrow == '<':
                s = '◀ ' + s
            out.append('<text class="u-label u-assoc" x="%.1f" y="%.1f" text-anchor="middle">%s</text>' % (seg[0] + loff[0], seg[1] + loff[1], s))
        if aclass:
            m = self._point_at(pts, .5)
            C = self.nodes[aclass]
            pc = clip(C, m)
            out.append('<path class="u-edge u-dash" d="M%.1f %.1f L%.1f %.1f"/>' % (m[0], m[1], pc[0], pc[1]))
        self.parts.append((1, ''.join(out)))
        return self

    def _clip_from(self, N, d, target):
        """Orthogonal exit: leave the box straight towards the first/last bend."""
        x, y, w, h = N[0] + d[0], N[1] + d[1], N[2], N[3]
        tx, ty = target
        if x <= tx <= x + w:
            return (tx, y + h) if ty > y + h else (tx, y)
        if y <= ty <= y + h:
            return (x + w, ty) if tx > x + w else (x, ty)
        return clip((x, y, w, h), target)

    @staticmethod
    def _point_at(pts, t):
        segs = [(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
        lens = [math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in segs]
        total = sum(lens) or 1
        goal = total * t
        for (a, b), L in zip(segs, lens):
            if goal <= L:
                k = goal / (L or 1)
                return a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k
            goal -= L
        return pts[-1]

    @staticmethod
    def _open_arrow(p, u, size=11):
        px, py = -u[1], u[0]
        b = (p[0] - u[0] * size, p[1] - u[1] * size)
        return '<path class="u-edge" d="M%.1f %.1f L%.1f %.1f L%.1f %.1f"/>' % (
            b[0] + px * 5.5, b[1] + py * 5.5, p[0], p[1], b[0] - px * 5.5, b[1] - py * 5.5)

    @staticmethod
    def _triangle(p, u, size=15):
        px, py = -u[1], u[0]
        b = (p[0] - u[0] * size, p[1] - u[1] * size)
        return '<path class="u-tri" d="M%.1f %.1f L%.1f %.1f L%.1f %.1f z"/>' % (
            p[0], p[1], b[0] + px * 8, b[1] + py * 8, b[0] - px * 8, b[1] - py * 8)

    @staticmethod
    def _diamond(p, u, filled):
        # u points outward from the owning box; diamond sits on the box border
        px, py = -u[1], u[0]
        m = (p[0] + u[0] * 9, p[1] + u[1] * 9)
        e = (p[0] + u[0] * 18, p[1] + u[1] * 18)
        return '<path class="%s" d="M%.1f %.1f L%.1f %.1f L%.1f %.1f L%.1f %.1f z"/>' % (
            'u-dfill' if filled else 'u-tri', p[0], p[1], m[0] + px * 6, m[1] + py * 6, e[0], e[1], m[0] - px * 6, m[1] - py * 6)

    @staticmethod
    def _end_labels(p, u, role, mult, flip):
        """u: unit direction travelling into the end point (towards the box)."""
        out = []

        def put(cls, q, anchor, text):
            out.append('<text class="%s" x="%.1f" y="%.1f" text-anchor="%s">%s</text>' % (cls, q[0], q[1], anchor, esc(text)))

        if abs(u[0]) > .8:                       # horizontal entry
            x = p[0] - u[0] * 7
            anchor = 'end' if u[0] > 0 else 'start'
            top, bottom = (p[1] - 6, p[1] + 15)
            if flip:
                top, bottom = bottom, top
            if role: put('u-role', (x, top), anchor, role)
            if mult: put('u-mult', (x, bottom), anchor, mult)
        elif abs(u[1]) > .8:                     # vertical entry
            y = p[1] - u[1] * 13 + 4
            r_side, m_side = (1, -1) if not flip else (-1, 1)
            if role: put('u-role', (p[0] + 7 * r_side, y), 'start' if r_side > 0 else 'end', role)
            if mult: put('u-mult', (p[0] + 7 * m_side, y), 'start' if m_side > 0 else 'end', mult)
        else:                                    # diagonal entry
            px, py = -u[1], u[0]
            sgn = -1 if flip else 1
            base = (p[0] - u[0] * 18, p[1] - u[1] * 18)

            def anchor(vx):
                return 'middle' if abs(vx) < .35 else ('start' if vx > 0 else 'end')
            if role: put('u-role', (base[0] + px * 11 * sgn, base[1] + py * 11 * sgn + 4), anchor(px * sgn), role)
            if mult: put('u-mult', (base[0] - px * 11 * sgn, base[1] - py * 11 * sgn + 4), anchor(-px * sgn), mult)
        return ''.join(out)

    # ----- output -------------------------------------------------------------
    def markup(self):
        body = ''.join(s for _, s in sorted(self.parts, key=lambda t: t[0]))
        x0, y0, x1, y1 = self.bounds(body)
        return ('<svg class="uml" xmlns="http://www.w3.org/2000/svg" viewBox="%d %d %d %d" role="img" aria-label="%s">%s</svg>'
                % (x0, y0, x1 - x0, y1 - y0, esc(self.title or self.name), body))

    def bounds(self, body, pad=14):
        """Tight viewBox around everything drawn (boxes, edge points, text with estimated width)."""
        xs, ys = [], []
        for (x, y, w, h) in self.nodes.values():
            xs += [x, x + w]; ys += [y, y + h]
        for m in re.finditer(r'd="([^"]+)"', body):
            nums = [float(v) for v in re.findall(r'-?\d+(?:\.\d+)?', m.group(1))]
            if m.group(1).lstrip().startswith('M') and not re.search(r'[hvlz]', m.group(1)):
                xs += nums[0::2]; ys += nums[1::2]
        for m in re.finditer(r'<text[^>]*x="([\d.-]+)" y="([\d.-]+)"[^>]*?(?:text-anchor="(\w+)")?[^>]*>([^<]*)<', body):
            x, y, anc, t = float(m.group(1)), float(m.group(2)), m.group(3) or 'start', html.unescape(m.group(4))
            w = len(t) * 7.4
            l = x - w if anc == 'end' else (x - w / 2 if anc == 'middle' else x)
            xs += [l, l + w]; ys += [y - 13, y + 4]
        if not xs:
            return 0, 0, self.w, self.h
        return (int(min(xs) - pad), int(min(ys) - pad), int(max(xs) + pad), int(max(ys) + pad))


# ---------------------------------------------------------------------------
# Sequence diagrams
# ---------------------------------------------------------------------------

class Sequence:
    """participants: list of (key, label). steps: list of tuples:
         ('msg', a, b, text)        synchronous call
         ('ret', a, b, text)        return (dashed)
         ('self', a, text)          call to self
         ('note', a, text)
         ('frag', kind, guard, [a, b], steps)            loop / opt / break
         ('alt', [a, b], [(guard, steps), (guard, steps)])
    """
    COL = 190
    TOP = 18

    def __init__(self, name, participants, steps, w=None, col=None, title=''):
        self.name, self.title = name, title
        self.col = col or self.COL
        self.parts = []
        self.x = {}
        for i, (k, lab) in enumerate(participants):
            self.x[k] = 90 + i * self.col
        self.participants = participants
        self.w = w or int(90 + (len(participants) - 1) * self.col + 120)
        self.y = self.TOP + 44
        self.body = []
        self._steps(steps, 0)
        self.h = int(self.y + 24)

    def _steps(self, steps, depth):
        for st in steps:
            kind = st[0]
            if kind == 'msg' or kind == 'ret':
                _, a, b, t = st
                self.y += 27
                x1, x2 = self.x[a], self.x[b]
                y = self.y
                cls = 'u-edge u-dash' if kind == 'ret' else 'u-edge'
                self.body.append('<path class="%s" d="M%.1f %.1f H%.1f"/>' % (cls, x1, y, x2))
                dirn = 1 if x2 > x1 else -1
                if kind == 'msg':
                    self.body.append('<path class="u-dfill" d="M%.1f %.1f l%.1f -4.5 v9 z"/>' % (x2, y, -9 * dirn))
                else:
                    self.body.append('<path class="u-edge" d="M%.1f %.1f l%.1f -5 M%.1f %.1f l%.1f 5"/>' % (x2, y, -9 * dirn, x2, y, -9 * dirn))
                tx = (x1 + x2) / 2
                self.body.append('<text class="u-msg%s" x="%.1f" y="%.1f" text-anchor="middle">%s</text>'
                                 % (' u-ret' if kind == 'ret' else '', tx, y - 6, esc(t)))
            elif kind == 'self':
                _, a, t = st
                self.y += 30
                x = self.x[a]
                y = self.y
                self.body.append('<path class="u-edge" d="M%.1f %.1f h28 v16 h-26"/>' % (x, y - 8))
                self.body.append('<path class="u-dfill" d="M%.1f %.1f l9 -4.5 v9 z"/>' % (x + 2, y + 8))
                self.body.append('<text class="u-msg" x="%.1f" y="%.1f">%s</text>' % (x + 34, y + 3, esc(t)))
                self.y += 10
            elif kind == 'note':
                _, a, t = st
                self.y += 26
                x = self.x[a]
                w = text_w(t, 11.5) + 18
                self.body.append('<g class="u-note"><path d="M%.1f %.1f h%.1f l8 8 v14 h-%.1f z"/><text class="u-mem" x="%.1f" y="%.1f">%s</text></g>'
                                 % (x + 10, self.y - 14, w - 8, w, x + 18, self.y + 2, esc(t)))
                self.y += 6
            elif kind == 'frag':
                _, fk, guard, span, inner = st
                self._fragment(fk, [(guard, inner)], span, depth)
            elif kind == 'alt':
                _, span, branches = st
                self._fragment('alt', branches, span, depth)

    def _fragment(self, kind, branches, span, depth):
        xs = [self.x[k] for k in span]
        x1, x2 = min(xs) - 62 + depth * 8, max(xs) + 74 - depth * 8
        top = self.y + 14
        self.y = top + 6
        seps = []
        for i, (guard, inner) in enumerate(branches):
            if i > 0:
                self.y += 14
                seps.append((self.y, guard))
                self.y += 4
            else:
                first_guard = guard
            self._steps(inner, depth + 1)
        self.y += 16
        bottom = self.y
        lw = text_w(kind, 11.5, NAME_W) + 16
        g = ['<g class="u-frag"><rect x="%.1f" y="%.1f" width="%.1f" height="%.1f"/>' % (x1, top, x2 - x1, bottom - top),
             '<path d="M%.1f %.1f h%.1f v12 l-7 7 h-%.1f z"/>' % (x1, top, lw, lw - 7),
             '<text class="u-fk" x="%.1f" y="%.1f">%s</text>' % (x1 + 7, top + 13.5, kind),
             '<text class="u-guard" x="%.1f" y="%.1f">[%s]</text>' % (x1 + lw + 8, top + 14, esc(first_guard))]
        for (sy, guard) in seps:
            g.append('<line class="u-dash" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>' % (x1, sy - 8, x2, sy - 8))
            g.append('<text class="u-guard" x="%.1f" y="%.1f">[%s]</text>' % (x1 + 8, sy + 6, esc(guard)))
        g.append('</g>')
        self.body.insert(0, ''.join(g))
        self.y += 4

    def markup(self):
        head = []
        for k, lab in self.participants:
            x = self.x[k]
            w = max(text_w(lab, FS_NAME, NAME_W) + 24, 90)
            head.append('<g class="u-node u-k1"><rect class="u-box" x="%.1f" y="%d" width="%.1f" height="30" rx="4"/>'
                        '<path class="u-head" d="M%.1f %.1f h%.1f v29 h-%.1f z"/>'
                        '<text class="u-name" x="%.1f" y="%d" text-anchor="middle">%s</text></g>'
                        % (x - w / 2, self.TOP, w, x - w / 2 + .5, self.TOP + .5, w - 1, w - 1, x, self.TOP + 20, esc(lab)))
            head.append('<line class="u-life" x1="%.1f" y1="%d" x2="%.1f" y2="%d"/>' % (x, self.TOP + 30, x, self.h - 8))
        return ('<svg class="uml" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" role="img" aria-label="%s">%s%s</svg>'
                % (self.w, self.h, esc(self.title or self.name), ''.join(head), ''.join(self.body)))


# ---------------------------------------------------------------------------
# Standalone (light) stylesheet — mirrors the slide classes in eci-slides.css
# ---------------------------------------------------------------------------

LIGHT_CSS = """
.uml{font-family:Inter,Segoe UI,Arial,sans-serif;background:#fff}
.uml text{fill:#1d1d1f}
.u-box{fill:#fff;stroke:#2b2f3a;stroke-width:1.2}
.u-head{fill:#eef1f6;stroke:none}
.u-k1 .u-head{fill:#d8ecff}.u-k2 .u-head{fill:#d9f5e3}.u-k3 .u-head{fill:#ffe7cc}
.u-k4 .u-head{fill:#efe2ff}.u-k5 .u-head{fill:#ffdfe0}
.u-sep{stroke:#2b2f3a;stroke-width:1}
.u-name{font-weight:700;font-size:13.5px}
.u-stereo{font-size:11.5px;fill:#555 !important}
.u-mem,.u-msg,.u-role,.u-mult,.u-guard{font-family:'JetBrains Mono',Consolas,monospace;font-size:12.5px}
.u-msg{font-size:12px}.u-ret{fill:#555 !important}
.u-new{fill:#b4235a !important;font-weight:700}
.u-role,.u-mult{font-size:11.5px;fill:#333 !important}
.u-label{font-size:12px;font-weight:600}
.u-assoc{font-style:italic;font-weight:500}
.u-edge{fill:none;stroke:#2b2f3a;stroke-width:1.3}
.u-dash{stroke-dasharray:6 4;fill:none;stroke:#2b2f3a;stroke-width:1.2}
.u-tri{fill:#fff;stroke:#2b2f3a;stroke-width:1.3}
.u-dfill{fill:#2b2f3a;stroke:#2b2f3a}
.u-actor circle,.u-actor path{fill:none;stroke:#2b2f3a;stroke-width:1.6}
.u-note path{fill:#fff8d6;stroke:#a68b2c}
.u-tag rect{fill:#1f6feb}.u-tag text{fill:#fff !important;font-size:12px;font-weight:700}
.u-k2.u-tag rect{fill:#1a7f37}.u-k3.u-tag rect{fill:#c25e00}.u-k4.u-tag rect{fill:#7c3aed}
.u-frag rect{fill:none;stroke:#2b2f3a;stroke-width:1.1}.u-frag path{fill:#eef1f6;stroke:#2b2f3a;stroke-width:1.1}
.u-fk{font-size:11.5px;font-weight:700}.u-guard{font-size:11.5px;fill:#333 !important}
.u-life{stroke:#2b2f3a;stroke-dasharray:5 5;stroke-width:1}
.u-pkg{fill:#fcfcfd}
"""


def standalone(markup, title=''):
    inner = markup.replace('<svg class="uml" ', '<svg class="uml" ', 1)
    style = ('<style>@import url("https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700'
             '&amp;family=JetBrains+Mono:wght@400;700&amp;display=swap");' + LIGHT_CSS.replace('\n', '') + '</style>')
    head_end = inner.index('>') + 1
    bg = '<rect width="100%" height="100%" fill="#ffffff"/>'
    return '<?xml version="1.0" encoding="utf-8"?>\n' + inner[:head_end] + style + bg + inner[head_end:]
