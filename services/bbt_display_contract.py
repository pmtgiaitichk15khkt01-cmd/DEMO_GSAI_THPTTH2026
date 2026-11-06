"""Align supplied rows for the existing BBT renderer; never invent limits."""
import re


def supplied_bbt_rows(raw):
    text = str(raw or '').replace(r'\n', '\n')
    rows = []
    for line in text.splitlines():
        if '|' not in line or re.fullmatch(r'[\s|:\-]+', line):
            continue
        line = re.sub(r'(?<!\|)\|\|(?!\|)', '§BAR§', line.strip())
        rows.append([s.strip().replace('§BAR§', '||') for s in line.strip('|').split('|')])
    return rows


def missing_asymptote_limits(raw):
    rows = supplied_bbt_rows(raw)
    return bool(len(rows) == 3 and any(cell.replace('$', '').strip() == '||' for cell in rows[2][1:]))


def aligned_bbt_rows(raw):
    rows = supplied_bbt_rows(raw)
    if len(rows) != 3:
        return None
    clean = lambda s: s.replace('$', '').strip().replace('−', '-')
    def label(value):
        value = clean(value).replace(r'\prime', "'").replace('′', "'").replace('’', "'")
        return re.sub(r'[{}^\s]', '', value)
    variable, derivative, function = [label(row[0]) for row in rows]
    if (not variable or not re.search(r'[^\W\d_]', variable)
            or "'" not in derivative
            or not (derivative.replace("'", '') == function
                    or (function == 'y' and derivative == "f'(x)"))):
        return None
    points = [clean(s) for s in rows[0][1:] if clean(s)]
    n = len(points)
    if not 2 <= n <= 12:
        return None
    tokens = ' '.join(clean(s) for s in rows[1][1:])
    if not re.fullmatch(r'[+\-0|\s]+', tokens):
        return None
    tokens = re.findall(r'\|\||[+\-]|0', tokens)
    if len(tokens) != 2*n-3 or any(t not in ('+', '-') for t in tokens[::2]) or any(t not in ('0', '||') for t in tokens[1::2]):
        return None
    values = [clean(s) for s in rows[2][1:]]
    if len(values) == 2*n-1 and all(v in {r'\nearrow', r'\searrow', '↗', '↘'} for v in values[1::2]):
        values = values[::2]
    if len(values) != n or any(not v for v in values):
        return None
    for i, value in enumerate(values):
        split = [s.strip() for s in value.split('||')]
        marker = tokens[2*i-1] if 0 < i < n-1 else ''
        if (marker == '||' and (len(split) != 2 or not all(split))) or (marker != '||' and len(split) != 1):
            return None
    norm = lambda s: re.sub(r'(?<![A-Za-z])([+-]?)inf\b', lambda m: m[1]+r'\infty', s)
    y = []
    for i, value in enumerate(values):
        y.append(norm(value))
        if i < n-1:
            y.append('↗' if tokens[2*i] == '+' else '↘')
    return [[rows[0][0]] + [norm(v) for v in points], [rows[1][0]] + [''] + tokens + [''], [rows[2][0]] + y]
