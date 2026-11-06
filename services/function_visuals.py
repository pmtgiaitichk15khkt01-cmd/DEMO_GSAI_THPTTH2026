"""Offline, deterministic visuals for one explicitly specified rational function."""
import ast
import html
import math
import re
import textwrap
from functools import lru_cache

import sympy as sp

X = sp.Symbol('x', real=True)
RENDER_REVISION = 2026110510


class NonStandardFunction(ValueError):
    """Outside the three non-degenerate function families selected for this lesson."""


def parse_function(source, strict=False):
    """Restricted arithmetic, never eval/sympify generated text. Keep original holes."""
    if len(source) > 180:
        raise ValueError('Expression too long')
    source = source.replace('\\left', '').replace('\\right', '').replace('\\cdot', '*').replace('\\times', '*')
    source = re.sub(r'\^\{([0-3])\}', r'^\1', source)
    for _ in range(4):
        source = re.sub(r'\\(?:dfrac|frac)\{([^{}]+)\}\{([^{}]+)\}', r'((\1)/(\2))', source)
    source = re.sub(r'(?<=\d)(?=x)|(?<=\))(?=[x(])|(?<=x)(?=\()', '*', source)
    tree = ast.parse(source.replace('^', '**'), mode='eval')
    if len(list(ast.walk(tree))) > 90:
        raise ValueError('Expression too complex')
    excluded = set()

    def visit(node):
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            if not math.isfinite(node.value) or abs(node.value) > 10**9:
                raise ValueError('Coefficient out of range')
            return sp.Rational(str(node.value))
        if isinstance(node, ast.Name) and node.id == 'x':
            return X
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
            value = visit(node.operand)
            return -value if isinstance(node.op, ast.USub) else value
        if isinstance(node, ast.BinOp):
            left, right = visit(node.left), visit(node.right)
            if isinstance(node.op, ast.Add):
                return left + right
            if isinstance(node.op, ast.Sub):
                return left - right
            if isinstance(node.op, ast.Mult):
                return left * right
            if isinstance(node.op, ast.Pow) and right.is_Integer and 0 <= right <= 3:
                return left ** right
            if isinstance(node.op, ast.Div):
                if right == 0:
                    raise ValueError('Zero denominator')
                numerator, denominator = sp.fraction(sp.cancel(right))
                if X in denominator.free_symbols or sp.degree(numerator, X) > 1:
                    raise ValueError('Only linear denominators supported')
                excluded.update(sp.solve(numerator, X))
                return left / right
        raise ValueError('Unsupported expression')

    original = visit(tree.body)
    expression = sp.cancel(original)
    numerator, denominator = sp.fraction(expression)
    if sp.degree(denominator, X) > 1 or sp.degree(numerator, X) > (2 if X in denominator.free_symbols else 3):
        raise ValueError('Unsupported function family')
    if len(excluded) > 1:
        raise ValueError('Multiple excluded points')
    if strict:
        degree_n, degree_d = sp.degree(numerator, X), sp.degree(denominator, X)
        if excluded:
            # A remaining pole is required: cancellation would turn it into a
            # different function with a removable hole, not the SGK family.
            if degree_d != 1 or degree_n not in (0, 1, 2):
                raise NonStandardFunction('Cancelled denominator')
        elif degree_d != 0 or degree_n != 3:
            raise NonStandardFunction('Not a cubic or a non-degenerate rational function')
    return expression, tuple(sorted(excluded, key=float))


def function_model(source, strict=False):
    expression, excluded = parse_function(source, strict=strict)
    derivative = sp.factor(sp.diff(expression, X))
    stationary = [] if derivative == 0 else [r for r in sp.solve(derivative, X) if r.is_real and r not in excluded]
    points = [-sp.oo] + sorted(set(stationary) | set(excluded), key=float) + [sp.oo]
    signs = []
    for left, right in zip(points, points[1:]):
        sample = right - 1 if left == -sp.oo else left + 1 if right == sp.oo else (left + right) / 2
        signs.append(int(sp.sign(derivative.subs(X, sample))))
    limits = []
    for point in points:
        if point in excluded:
            limits.append((sp.limit(expression, X, point, dir='-'), sp.limit(expression, X, point, dir='+')))
        else:
            value = sp.limit(expression, X, point, dir='+' if point == -sp.oo else '-')
            limits.append((value, value))
    return dict(expression=expression, derivative=derivative, excluded=excluded,
                stationary=stationary, points=points, signs=signs, limits=limits)


def _text(value):
    # Limits at algebraic stationary points can retain nested substitutions.
    # Simplify before measuring/placing labels, for every function family.
    if isinstance(value, sp.Basic):
        value = sp.simplify(value)
    return str(value).replace('-oo', '−∞').replace('oo', '+∞').replace('sqrt', '√').replace('**', '^').replace('*', '·').replace('-', '−')


def _svg(width, height, label, content):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img" '
            f'aria-label="{html.escape(label, quote=True)}" style="width:100%;height:auto;display:block;background:white;color:#111;font:18px Times New Roman,serif">'
            + content + '</svg>')


def _label(x, y, text, size=18):
    if '√' in str(text) or re.search(r'\d/\d', str(text)):
        raw = str(text)
        point = re.fullmatch(r'(I)?\((.*); (.*)\)', raw)
        parts = (point[2], point[3]) if point else (raw,)
        rendered = []
        try:
            for part in parts:
                normalized = part.replace('√', 'sqrt').replace('·', '*').replace('−', '-')
                if not re.fullmatch(r'[0-9sqrt()\s+*/.\-^]+', normalized):
                    raise ValueError('Not a numeric expression')
                value = sp.sympify(normalized.replace('^', '**'), locals={'sqrt': sp.sqrt})
                rendered.append(html.unescape(sp.mathml(value, printer='presentation')))
            content = rendered[0] if not point else (
                '<mrow>' + ('<mi>I</mi>' if point[1] else '')
                + '<mo>(</mo>' + rendered[0] + '<mo>;</mo>' + rendered[1] + '<mo>)</mo></mrow>')
            width = max(60, min(370, len(raw)*size*.64+18))
            height = max(38, size*2.6)
            return (f'<foreignObject x="{x-width/2:.3f}" y="{y-height/2:.3f}" width="{width:.3f}" height="{height:.3f}" '
                    f'data-math-label="true" aria-label="{html.escape(raw, quote=True)}">'
                    '<div xmlns="http://www.w3.org/1999/xhtml" style="height:100%;display:flex;align-items:center;justify-content:center;'
                    f'font-size:{max(size,17)}px;color:#111"><math xmlns="http://www.w3.org/1998/Math/MathML">'
                    + content + '</math></div></foreignObject>')
        except (ValueError, TypeError, SyntaxError):
            pass
    return f'<text x="{x:.3f}" y="{y:.3f}" text-anchor="middle" dominant-baseline="middle" fill="#111" font-size="{size}">{html.escape(str(text))}</text>'


def _line(x1, y1, x2, y2, dashed=False):
    return f'<line x1="{x1:.3f}" y1="{y1:.3f}" x2="{x2:.3f}" y2="{y2:.3f}" stroke="#111" stroke-width="1.6"' + (' stroke-dasharray="6 5"' if dashed else '') + '/>'


def variation_svg(model):
    points, signs, limits = model['points'], model['signs'], model['limits']
    width = max(820, 180 * (len(points) - 1) + 120)
    xs = [140 + i * (width - 210) / (len(points) - 1) for i in range(len(points))]
    finite = [float(v) for pair in limits for v in pair if v.is_finite]
    low, high = min(finite or [0]), max(finite or [0])

    def level(value):
        if value == sp.oo:
            return 128
        if value == -sp.oo:
            return 236
        return 182 if high == low else 213 - 62 * (float(value) - low) / (high - low)

    body = f'<rect x="1" y="1" width="{width-2}" height="258" fill="white" stroke="#111" stroke-width="2"/>'
    body += _line(82, 1, 82, 259) + _line(1, 52, width-1, 52) + _line(1, 100, width-1, 100)
    body += _label(42, 28, 'x') + _label(42, 77, 'y′') + _label(42, 180, 'y')
    for i, point in enumerate(points):
        body += _label(xs[i], 28, _text(point))
        if point in model['excluded']:
            pole = any(v in (sp.oo, -sp.oo) for v in limits[i])
            body += _label(xs[i], 77, '∥' if pole else '×')
            for offset in (-3, 3) if pole else (0,):
                body += _line(xs[i]+offset, 101, xs[i]+offset, 258, dashed=not pole)
            for offset, value in zip((-28, 28), limits[i]):
                body += _label(xs[i]+offset, level(value), _text(value), 16)
        else:
            if point in model['stationary']:
                body += _label(xs[i], 77, '0')
            body += _label(xs[i], level(limits[i][0]), _text(limits[i][0]), 17)
    for i, sign in enumerate(signs):
        body += _label((xs[i]+xs[i+1])/2, 77, '+' if sign > 0 else '−' if sign < 0 else '0')
        clearance_left = max(42, min(80, len(_text(limits[i][1]))*4.5))
        clearance_right = max(42, min(80, len(_text(limits[i+1][0]))*4.5))
        x1, x2 = xs[i]+clearance_left, xs[i+1]-clearance_right
        y1, y2 = level(limits[i][1]), level(limits[i+1][0])
        body += _line(x1, y1, x2, y2)
        angle = math.atan2(y2-y1, x2-x1)
        body += '<path d="M %.3f %.3f L %.3f %.3f L %.3f %.3f" fill="none" stroke="#111" stroke-width="1.6"/>' % (x2-9*math.cos(angle-.45), y2-9*math.sin(angle-.45), x2, y2, x2-9*math.cos(angle+.45), y2-9*math.sin(angle+.45))
    return _svg(width, 260, 'Bảng biến thiên y=' + str(model['expression']), body)


def graph_svg(model):
    expression = model['expression']
    numerator, denominator = sp.fraction(expression)
    roots = sp.real_roots(numerator) if sp.degree(numerator, X) > 0 else []
    roots = sorted((r for r in set(roots) if r not in model['excluded']), key=float)
    center = None
    if X in denominator.free_symbols:
        pole = model['excluded'][0]
        quotient = sp.div(numerator, denominator, X)[0]
        center = (pole, quotient.subs(X, pole))
    elif sp.degree(numerator, X) == 3:
        poly = sp.Poly(numerator, X)
        xc = -poly.nth(2) / (3*poly.nth(3))
        center = (xc, expression.subs(X, xc))
    # A generic cubic need not have a short radical expression. Ordered real
    # roots are exact algebraic coordinates, rather than rounded decimals.
    root_names = {}
    legend = []
    if any(r.has(sp.CRootOf) for r in roots):
        subscripts = ('₁', '₂', '₃')
        root_names = {r: 'α' + subscripts[i] for i, r in enumerate(roots)}
        legend.append(' < '.join(root_names.values()) + ' là tất cả nghiệm thực phân biệt của ' + _text(numerator) + ' = 0.')

    def coordinate(value):
        return root_names.get(value, _text(sp.simplify(value)))

    special_points = {}
    for p in model['stationary']:
        special_points[(p, expression.subs(X, p))] = ['Cực trị' if len(model['stationary']) == 2 else 'Điểm dừng']
    for p in roots:
        special_points.setdefault((p, sp.S.Zero), []).append('Ox')
    if 0 not in model['excluded']:
        special_points.setdefault((sp.S.Zero, expression.subs(X, 0)), []).append('Oy')
    if center:
        special_points.setdefault(center, []).append('I')
    landmarks = [float(v) for v in (*model['stationary'], *model['excluded'], *roots)]
    if center:
        landmarks.append(float(center[0]))
    low_x, high_x = min([0, *landmarks]), max([0, *landmarks])
    padding = max(1, (high_x-low_x)*.25)
    xmin, xmax = low_x-padding, high_x+padding
    if xmax-xmin > 100000:
        raise ValueError('Plot window out of range')
    function = sp.lambdify(X, expression, modules='math')
    cuts = [xmin] + [float(v) for v in model['excluded'] if xmin < float(v) < xmax] + [xmax]
    branches, values = [], []
    for left, right in zip(cuts, cuts[1:]):
        samples = []
        for i in range(401):
            x = left + (right-left) * (i+.25)/401
            try:
                y = float(function(x))
                if math.isfinite(y):
                    samples.append((x, y)); values.append(y)
            except (ZeroDivisionError, ValueError, OverflowError):
                pass
        for point in (*model['stationary'], *roots):
            xp = float(point)
            if left < xp < right:
                samples.append((xp, 0.0 if point in roots else float(expression.subs(X, point))))
        samples.sort(key=lambda pair: pair[0])
        branches.append(samples)
    values.sort()
    if not values:
        raise ValueError('No finite plot values')
    special = [float(expression.subs(X, p)) for p in model['stationary']]
    if center:
        special.append(float(center[1]))
    if 0 not in model['excluded']:
        special.append(float(expression.subs(X, 0)))
    if len(model['stationary']) == 2:
        # A textbook sketch must make the extrema readable, rather than flatten
        # them against axes because of large cubic values at the window edges.
        ymin, ymax = min([0, *special]), max([0, *special])
        margin = max(1, (ymax-ymin)*.4)
    else:
        ymin = min([0, values[len(values)//10], *special])
        ymax = max([0, values[9*len(values)//10], *special])
        margin = max(1, (ymax-ymin)*.12)
    ymin, ymax = ymin-margin, ymax+margin
    px = lambda x: 58 + (x-xmin)*690/(xmax-xmin)
    py = lambda y: 430 - (y-ymin)*390/(ymax-ymin)
    body = '<defs><clipPath id="function-plot-clip"><rect x="58" y="40" width="690" height="390"/></clipPath></defs>'
    body += _line(58, py(0), 765, py(0)) + _line(px(0), 440, px(0), 24)
    body += f'<path d="M 757 {py(0)-4:.3f} L 765 {py(0):.3f} L 757 {py(0)+4:.3f} M {px(0)-4:.3f} 32 L {px(0):.3f} 24 L {px(0)+4:.3f} 32" fill="none" stroke="#111" stroke-width="1.6"/>'
    body += _label(773, py(0), 'x') + _label(px(0), 14, 'y') + _label(px(0)-12, py(0)+15, 'O', 15)
    def ticks(lo, hi):
        raw = (hi-lo)/6
        base = 10**math.floor(math.log10(raw))
        step = next((factor*base for factor in (1, 2, 5, 10) if factor*base >= raw), 10*base)
        return [i*sp.Rational(str(step)) for i in range(math.ceil(lo/step), math.floor(hi/step)+1)]

    # Reserve the actual label footprints. Axis coordinates take priority over
    # generic ticks; point labels then choose free positions around their point.
    occupied = []
    label_layer = []
    curve_ink = [(px(x), py(y)) for branch in branches for x, y in branch if ymin <= y <= ymax]

    def touches_curve(rect):
        return any(rect[0]-3 < cx < rect[2]+3 and rect[1]-3 < cy < rect[3]+3 for cx, cy in curve_ink)

    def box(lx, ly, text, size=13):
        if '√' in text or re.search(r'\d/\d', text):
            size = max(17, size)
        half = max(size, len(text)*size*.62)/2 + 4
        vertical = max(size*.65+3, 22 if '√' in text or '/' in text else 0)
        return (lx-half, ly-vertical, lx+half, ly+vertical)

    def overlaps(rect):
        return any(rect[0] < b[2] and rect[2] > b[0] and rect[1] < b[3] and rect[3] > b[1] for b in occupied)

    def annotation(lx, ly, text, kind, size=13, axis=None):
        rect = box(lx, ly, text, size)
        occupied.append(rect)
        # Labels sit above guides with a small white clearance, so a projection
        # ending on the axis never runs through its exact coordinate.
        background = f'<rect x="{rect[0]:.3f}" y="{rect[1]:.3f}" width="{rect[2]-rect[0]:.3f}" height="{rect[3]-rect[1]:.3f}" fill="white"/>'
        attrs = 'data-graph-label="'+kind+'"' + (' data-axis-coordinate="'+axis+'"' if axis else '')
        label = _label(lx, ly, text, size)
        label = label.replace('<text ', '<text '+attrs+' ', 1).replace('<foreignObject ', '<foreignObject '+attrs+' ', 1)
        label_layer.append(background + label)
        return ''

    occupied.extend((box(px(0)-12, py(0)+15, 'O', 15),
                     (px(0)-4, 24, px(0)+4, 440), (58, py(0)-4, 765, py(0)+4)))
    axis_coords = {'x': {}, 'y': {}}
    for p, v in special_points:
        if p != 0:
            axis_coords['x'][p] = coordinate(p)
        if v != 0:
            axis_coords['y'][v] = coordinate(v)
    for axis, coords in axis_coords.items():
        for value, text in sorted(coords.items(), key=lambda item: float(item[0])):
            pos = px(float(value)) if axis == 'x' else py(float(value))
            lx, ly = (pos, py(0)+18) if axis == 'x' else (px(0)-box(0, 0, text)[2]-10, pos)
            rect = box(lx, ly, text)
            if len(text) > 22 or rect[0] < 4 or rect[2] > 810 or overlaps(rect) or touches_curve(rect):
                # Keep close/long exact coordinates in the point callouts, not
                # stacked over each other on an axis.
                continue
            body += annotation(lx, ly, text, 'axis', axis=axis)
            body += _line(pos, py(0)-3, pos, py(0)+3) if axis == 'x' else _line(px(0)-3, pos, px(0)+3, pos)

    for v in ticks(xmin, xmax):
        if abs(v) < 1e-12:
            continue
        text = _text(sp.Rational(str(v)))
        if any(abs(px(v)-px(float(p))) < 36 for p in axis_coords['x']) or overlaps(box(px(v), py(0)+18, text)) or touches_curve(box(px(v), py(0)+18, text)):
            continue
        body += _line(px(v), py(0)-3, px(v), py(0)+3) + annotation(px(v), py(0)+18, text, 'tick')
    for v in ticks(ymin, ymax):
        if abs(v) < 1e-12:
            continue
        text = _text(sp.Rational(str(v)))
        if any(abs(py(v)-py(float(p))) < 25 for p in axis_coords['y']) or overlaps(box(px(0)-25, py(v), text)) or touches_curve(box(px(0)-25, py(v), text)):
            continue
        body += _line(px(0)-3, py(v), px(0)+3, py(v)) + annotation(px(0)-25, py(v), text, 'tick')
    clipped = ''
    for branch in branches:
        coords = ' '.join(f'{px(x):.3f},{max(-10000,min(10000,py(y))):.3f}' for x,y in branch)
        clipped += f'<polyline points="{coords}" fill="none" stroke="#163e87" stroke-width="2"/>'
    asymptote = None
    if X in denominator.free_symbols:
        asymptote = sp.div(numerator, denominator, X)[0]
        clipped += _line(px(xmin), py(float(asymptote.subs(X,xmin))), px(xmax), py(float(asymptote.subs(X,xmax))), True)
    for p in model['excluded']:
        value = sp.limit(expression, X, p)
        if value in (sp.oo, -sp.oo):
            clipped += _line(px(float(p)), 40, px(float(p)), 430, True)
        else:
            clipped += f'<circle cx="{px(float(p)):.3f}" cy="{py(float(value)):.3f}" r="4" fill="white" stroke="#163e87" stroke-width="2"/>'
    body += '<g clip-path="url(#function-plot-clip)">' + clipped + '</g>'
    for (p, v), names in special_points.items():
        xp, yp = px(float(p)), py(float(v))
        occupied.append((xp-6, yp-6, xp+6, yp+6))
        if any(n in names for n in ('Cực trị', 'Điểm dừng', 'I')):
            occupied.extend(((xp-2, min(yp, py(0)), xp+2, max(yp, py(0))),
                             (min(xp, px(0)), yp-2, max(xp, px(0)), yp+2)))
    guides = ''
    for (p, v), names in special_points.items():
        xp, yp = px(float(p)), py(float(v))
        if any(n in names for n in ('Cực trị', 'Điểm dừng', 'I')):
            guides += '<g data-projection="true">' + _line(xp, yp, xp, py(0), True) + _line(xp, yp, px(0), yp, True) + '</g>'
        guides += f'<circle data-point="{html.escape(" ".join(names), quote=True)}" cx="{xp:.3f}" cy="{yp:.3f}" r="3.2" fill="#111" stroke="#111" stroke-width="1.5"/>'
        name = 'I' if 'I' in names else ''
        text = f'{name}({coordinate(p)}; {coordinate(v)})'
        point_text = text
        if len(text) > 34:
            point_text = name or 'P' + str(len(legend)+1)
            legend.append(point_text + ': ' + text)
        placed = False
        half = max(13, len(point_text)*13*.62)/2 + 4
        for dy in (-22, 28, -48, 54, -74, 80):
            for dx in (0, half+12, -half-12, half+40, -half-40):
                lx, ly = xp+dx, yp+dy
                rect = box(lx, ly, point_text)
                if rect[0] < 8 or rect[2] > 808 or rect[1] < 30 or rect[3] > 449 or overlaps(rect):
                    continue
                if touches_curve(rect):
                    continue
                if abs(dx) > half+20 or abs(dy) > 35:
                    target_x = min(max(xp, rect[0]), rect[2])
                    target_y = min(max(yp, rect[1]), rect[3])
                    body += f'<line x1="{xp:.3f}" y1="{yp:.3f}" x2="{target_x:.3f}" y2="{target_y:.3f}" stroke="#555" stroke-width="0.7"/>'
                body += annotation(lx, ly, point_text, 'point')
                placed = True
                break
            if placed:
                break
        if not placed:
            # Extremely crowded data keep exact coordinates in a separate key.
            key = name or 'P' + str(len(legend)+1)
            legend.append(key + ': ' + text)
            for dy in (-22, 28, -48, 54, -74, 80):
                if placed:
                    break
                for dx in (24, -24, 48, -48, 72, -72):
                    lx, ly = xp+dx, yp+dy
                    rect = box(lx, ly, key)
                    if (rect[0] < 8 or rect[2] > 808 or rect[1] < 30 or rect[3] > 449
                            or overlaps(rect) or touches_curve(rect)):
                        continue
                    body += annotation(lx, ly, key, 'point-key')
                    placed = True
                    break
    # Guides are clipped to the graph rectangle; point labels remain readable.
    body += '<g clip-path="url(#function-plot-clip)">' + guides + '</g>'
    body += ''.join(label_layer)
    if asymptote is not None:
        poles = [p for p in model['excluded'] if sp.limit(expression, X, p) in (sp.oo, -sp.oo)]
        caption = '; '.join(['x=' + _text(p) for p in poles] + ['y=' + _text(asymptote)])
        body += _label(410, 469, 'Tiệm cận: ' + caption, 15)
    legend_y = 500
    for item in legend:
        if root_names and item == legend[0] and 'nghiệm thực phân biệt' in item:
            prefix = ' < '.join(root_names.values()) + ' là tất cả nghiệm thực phân biệt của '
            tex = sp.latex(numerator) + ' = 0'
            # Streamlit Markdown does not execute the exported page's KaTeX
            # initializer. Native MathML provides the same exact equation there;
            # exports still enhance this span using its unchanged data-tex.
            fallback = ('<math xmlns="http://www.w3.org/1998/Math/MathML">'
                        + html.unescape(sp.mathml(sp.Eq(numerator, 0, evaluate=False), printer='presentation'))
                        + '</math>')
            body += ('<foreignObject x="20" y="480" width="780" height="74" '
                     'data-exact-coordinate-key="true"><div xmlns="http://www.w3.org/1999/xhtml" '
                     'style="font-family:Times New Roman,serif;font-size:15px;text-align:center;line-height:1.8">'
                     + html.escape(prefix) + '<span class="lesson-math" data-display="false" data-tex="'
                     + html.escape(tex, quote=True) + '">' + fallback + '</span>.'
                     '</div></foreignObject>')
            legend_y = 554
            continue
        for line in textwrap.wrap(item, width=96, break_long_words=True, break_on_hyphens=False):
            body += _label(410, legend_y, line, 15).replace('<text ', '<text data-exact-coordinate-key="true" ', 1)
            legend_y += 23
    return _svg(820, max(490, legend_y+12) if legend else 490, 'Đồ thị y=' + str(expression), body)


@lru_cache(maxsize=64)
def explicit_function_visuals(topic):
    """Only one unambiguous ASCII function in the selected topic; no guessed examples."""
    matches = list(re.finditer(r'(?<!\w)y\s*=\s*((?:(?:\\(?:dfrac|frac|left|right|cdot|times))|[0-9xX+\-*/^().{}\s])+)', topic))
    if len(matches) != 1:
        return ''
    raw = matches[0][1].strip()
    tail = topic[matches[0].end():]
    if not raw.endswith('.') and re.match(r'[A-Za-z_\\]', tail):
        return ''
    source = raw.rstrip('.').strip().lower()
    try:
        model = function_model(source, strict=True)
        numerator, denominator = sp.fraction(model['expression'])
        if re.search(r'2\s*/\s*1|bậc hai trên bậc nhất', topic, re.I):
            if sp.degree(numerator, X) != 2 or sp.degree(denominator, X) != 1:
                raise NonStandardFunction('Not a non-degenerate quadratic over linear')
        if re.search(r'1\s*/\s*1|bậc nhất trên bậc nhất', topic, re.I):
            if sp.degree(numerator, X) > 1 or sp.degree(denominator, X) != 1:
                raise NonStandardFunction('Not a non-degenerate homographic function')
        return ('<section class="verified-function-visuals" data-function-renderer="' + str(RENDER_REVISION) + '" style="break-inside:avoid">'
                '<h3>Bảng biến thiên và đồ thị theo hàm số đã chọn</h3>'
                '<p class="lesson-math" data-display="false" data-tex="y=' + html.escape(sp.latex(model['expression']), quote=True) + '"></p>'
                + '<p>Điểm loại khỏi miền xác định: ' + html.escape(', '.join(_text(p) for p in model['excluded']) or 'không có') + '.</p>'
                + variation_svg(model) + graph_svg(model) + '</section>')
    except NonStandardFunction:
        return '<p class="notice" data-function-rejected="true">Hàm số không thuộc ba dạng không suy biến đang xét. Cần kiểm tra bậc tử, bậc mẫu và điều kiện không khử nhân tử trước khi dựng BBT và đồ thị.</p>'
    except ValueError as error:
        if str(error) == 'Zero denominator':
            return '<p class="notice" data-function-rejected="true">Mẫu số đồng nhất bằng 0: không xác định hàm số, không dựng BBT hoặc đồ thị.</p>'
        return ''
    except (SyntaxError, TypeError, NotImplementedError, OverflowError, ZeroDivisionError, sp.PolynomialError):
        return ''


def with_function_visuals(body, topic, lesson=''):
    """Use the same figure on the lesson page and in all export styles."""
    visuals = explicit_function_visuals(str(topic or ''))
    if not visuals and not re.search(r'(?<!\w)y\s*=', str(topic or '')):
        # A generic topic may have one repeated worked example. Never choose
        # between different examples, or interpret code snippets as mathematics.
        prose = re.sub(r'```[\s\S]*?```|~~~[\s\S]*?~~~|`[^`\n]*`', '', lesson)
        candidates = re.finditer(r'(?<!\w)y\s*=\s*((?:(?:\\(?:dfrac|frac|left|right|cdot|times))|[0-9xX+\-*/^().{}\s])+)', prose)
        figures = set()
        for candidate in candidates:
            raw = candidate[1].strip()
            if not raw.endswith('.') and re.match(r'[A-Za-z_\\]', prose[candidate.end():]):
                continue
            figure = explicit_function_visuals('y=' + raw)
            if figure and 'data-function-rejected' not in figure:
                figures.add(figure)
        if len(figures) > 1:
            # Associate only with the nearest explicit preceding function.
            # Never leave a malformed source BBT alongside its verified model.
            used = set()
            def scoped_table(match):
                prefix = body[:match.start()]
                functions = list(re.finditer(r'data-tex="(y=[^"]+)"', prefix))
                plain = html.unescape(re.sub(r'<[^>]+>', '', match[0]))
                if not functions or not re.search(r"x[\s\S]*y[′'][\s\S]*y", plain):
                    return match[0]
                figure = explicit_function_visuals(html.unescape(functions[-1][1]))
                if figure not in figures:
                    return match[0]
                used.add(figure)
                return figure
            result = re.sub(r'<table\b[^>]*>[\s\S]*?</table>', scoped_table, body)
            return result + "".join(sorted(figures - used))
        if len(figures) == 1:
            visuals = figures.pop()
    if not visuals:
        return body
    replaced = [False]

    def replace_table(match):
        plain = html.unescape(re.sub(r'<[^>]+>', '', match[0]))
        if not replaced[0] and re.search(r'x[\s\S]*y[′\'][\s\S]*y', plain):
            replaced[0] = True
            return visuals
        return match[0]

    result = re.sub(r'<table\b[^>]*>[\s\S]*?</table>', replace_table, body)
    return result if replaced[0] else result + visuals
