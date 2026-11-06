"""Preserve typed content at presentation boundaries; do not judge curriculum."""
import hashlib
import json
import re

from services.lesson_export import _TOKENS

T1_CONTEXT_REVISION = 2026110603


def _chemical_macros(text, convert):
    """Visit balanced ce bodies, including braced charges/isotopes."""
    parts, cursor = [], 0
    for start in re.finditer(r'\\ce\s*\{', text):
        if start.start() < cursor:
            continue
        depth, end = 1, start.end()
        while end < len(text) and depth:
            depth += (text[end] == '{') - (text[end] == '}')
            end += 1
        if depth:
            continue
        parts.extend((text[cursor:start.start()], convert(text[start.end():end-1])))
        cursor = end
    return ''.join(parts) + text[cursor:]


def wrap_naked_chemistry(text):
    """Add math delimiters to ce in prose only; keep formula bodies/code exact."""
    def wrap(body):
        # Reactions on their own lines stay readable on narrow screens/print;
        # ordinary chemical formulae remain inline with the sentence.
        if re.search(r'->|<-|<=>|→|←|⇌', body):
            return '\n\n$$\\ce{' + body + '}$$\n\n'
        return '$\\ce{' + body + '}$'
    parts, cursor = [], 0
    for match in _TOKENS.finditer(str(text)):
        parts.extend((_chemical_macros(text[cursor:match.start()], wrap), match[0]))
        cursor = match.end()
    parts.append(_chemical_macros(text[cursor:], wrap))
    return ''.join(parts)


def _chemical_core_tex(body):
    """Conservative ce presentation subset for native KaTeX without mhchem.

    No atom, coefficient, charge, phase or reaction direction is inferred.
    Export still uses the complete bundled mhchem renderer and original body.
    """
    arrows = {'<=>': r'\rightleftharpoons ', '<->': r'\leftrightarrow ', '->': r'\rightarrow ',
              '<-': r'\leftarrow ', '→': r'\rightarrow ', '←': r'\leftarrow ', '⇌': r'\rightleftharpoons ',
              '↑': r'\uparrow ', '↓': r'\downarrow '}
    output, i, previous = [], 0, ''
    while i < len(body):
        arrow = next((key for key in arrows if body.startswith(key, i)), None)
        if arrow:
            if body[i+len(arrow):].lstrip().startswith('['):
                raise ValueError('Annotated chemical arrow needs mhchem')
            output.append(arrows[arrow]); i += len(arrow); previous = ''
            continue
        char = body[i]
        if char.isspace():
            output.append(r'\,'); i += 1
            continue
        if char in '^_':
            match = re.match(r'[\^_](?:\{([A-Za-z0-9+\-]+)\}|([0-9]*[+\-]?))', body[i:])
            value = (match[1] or match[2]) if match else ''
            if not value:
                raise ValueError('Unsupported chemical script')
            output.append(('{}' if not output else '') + char + '{' + value + '}')
            i += match.end(); previous = 'script'
            continue
        match = re.match(r'[A-Za-z]+|\d+(?:\.\d+)?', body[i:])
        if match:
            token = match[0]
            if token[0].isdigit():
                output.append('_{' + token + '}' if previous in ('atom', ')', ']') else token)
                previous = 'number'
            else:
                output.append(r'\mathrm{' + token + '}'); previous = 'atom'
            i += len(token)
            continue
        if char in '()[]':
            output.append(char); previous = char; i += 1
            continue
        if char in '+-':
            tail = body[i+1:].lstrip()
            charge = previous in ('atom', 'number', ')', ']', 'script') and (not tail or tail[0] in ',;+' or tail.startswith(('->','<=>','→','⇌')))
            output.append('^{' + char + '}' if charge else char)
            previous = 'script' if charge else ''; i += 1
            continue
        if char in ',;=*.·#':
            output.append({'*': r'\cdot ', '·': r'\cdot ', '#': r'\equiv '}.get(char, char))
            previous = ''; i += 1
            continue
        raise ValueError('Chemical notation needs mhchem review')
    return ''.join(output)


def chemical_display_markdown(text):
    """Display-only conversion; stored lesson/answers/source remain unchanged."""
    value = wrap_naked_chemistry(str(text or ''))
    def token(match):
        raw = match[0]
        if raw.startswith(('`', '~~~')):
            return raw
        try:
            return _chemical_macros(raw, _chemical_core_tex)
        except ValueError:
            # Do not pretend unsupported notation was rendered correctly.
            return '⚠️ Công thức cần đối chiếu bản gốc: `' + raw.replace('`', '') + '`'
    return _TOKENS.sub(token, value)


def preserve_math_and_code(text, normalize_prose):
    value = str(text or '')
    prefix = 'GSAIPRESERVE' + hashlib.sha256(value.encode()).hexdigest()[:16]
    while prefix in value:
        prefix += 'X'
    slots = []

    def save(match):
        original = match[0]
        # Streamlit's Markdown math path uses dollars. Change delimiters only,
        # retaining the formula body and whether it is inline or display math.
        if original.startswith(r'\['):
            original = '$$' + original[2:-2] + '$$'
        elif original.startswith(r'\('):
            original = '$' + original[2:-2] + '$'
        slots.append(original)
        return f'{prefix}N{len(slots)-1}END'

    result = normalize_prose(_TOKENS.sub(save, value))
    for index, original in enumerate(slots):
        result = result.replace(f'{prefix}N{index}END', original)
    return result


def option_markdown_label(option):
    """Display naked numeric intervals containing infinity as Markdown math.

    Existing math/code and the stored answer option remain untouched.
    This intentionally does not guess arbitrary prose or scientific notation.
    """
    endpoint = r'(?:[+-]?\d+(?:[.,]\d+)?|[+-]?\\infty)'
    interval = re.compile(r'[\[(]\s*' + endpoint + r'\s*[;,]\s*' + endpoint + r'\s*[\])]')
    def normalize_prose(text):
        return interval.sub(lambda m: '$' + m[0] + '$' if r'\infty' in m[0] else m[0], text)
    return preserve_math_and_code(option, normalize_prose)


def polya_display_markdown(text):
    """Put recognized Polya stages in separate paragraphs without editing tasks."""
    def format_prose(value):
        value = re.sub(r'(?m)^[ \t]*[-*][ \t]+(?=(?:\*\*|__)?Bước[ \t]+[1-4]\s*:)', '', value)
        heading = re.compile(
            r'(?:\*\*|__)?Bước[ \t]+([1-4])[ \t]*:[ \t]*(?:\*\*|__)?[ \t]*'
            r'(Tìm hiểu đề|Lập kế hoạch|Thực hiện kế hoạch|Kiểm tra và nhìn lại)'
            r'[ \t]*[:.]?(?:\*\*|__)?[ \t]*', re.I)
        titles = {'1': 'Tìm hiểu đề', '2': 'Lập kế hoạch',
                  '3': 'Thực hiện kế hoạch', '4': 'Kiểm tra và nhìn lại'}
        def separate(match):
            if match[2].casefold() != titles[match[1]].casefold():
                return match[0]
            return '\n\n**Bước ' + match[1] + ': ' + titles[match[1]] + ':** '
        value = heading.sub(separate, value)
        return re.sub(r'\n{3,}', '\n\n', value)
    return preserve_math_and_code(text, format_prose).strip()


def student_essay_text(text):
    """Hide reserved author metadata, retaining the question and Polya prompts.

    A complete JSON value may occupy several lines. Do not guess its closing
    delimiters or consume the following student exercise when JSON is damaged.
    """
    value = str(text or '')
    spans = []
    for match in re.finditer(
            r'(?mi)^[ \t]*(?:[-*][ \t]+)?(?:\*\*|__)?'
            r'(OUTCOME|COGNITIVE_REASON|COGNITIVE_STEPS)(?:\*\*|__)?'
            r':[ \t]*(?:\*\*|__)?[ \t]*', value):
        end = value.find('\n', match.end())
        end = len(value) if end < 0 else end
        if match[1].upper() == 'COGNITIVE_STEPS':
            tail = value[match.end():].lstrip()
            try:
                _, length = json.JSONDecoder().raw_decode(tail)
                end = max(end, len(value) - len(tail) + length)
            except (ValueError, TypeError):
                pass
        spans.append((match.start(), end))
    for start, end in reversed(spans):
        value = value[:start] + value[end:]
    return polya_display_markdown(value)
