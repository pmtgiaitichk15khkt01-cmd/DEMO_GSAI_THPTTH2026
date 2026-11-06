"""Bounded proof for a specific interval-coded cubic parameter answer contract."""
import re

import sympy as sp

from qa_runtime import parse_math_expression
from services.academic_context import folded


def interval_code_conflict(question):
    """Prove a mismatched numeric key; never rewrite a question or its answer.

    Only supports the observed opposite-sides-of-Oy task, a globally positive
    constant derivative discriminant and a quadratic parameter product.
    Unsupported clauses/formulas return no verdict, not a correctness claim.
    """
    if question.get('opt') or question.get('stmts'):
        return ''
    raw = str(question.get('q', ''))
    if len(raw) > 10000:
        return ''
    text = folded(raw)
    if 'hai diem cuc tri nam ve hai phia cua truc tung' not in text:
        return ''
    # Extra restrictions can change an interval into isolated admissible values.
    if any(term in text for term in ('so nguyen', 'so tu nhien', 'm thuoc', 'm duong', 'm am')):
        return ''
    if re.search(r'\bm\s*(?:\\in\b|∈|[<>≤≥=])', raw):
        return ''
    code_match = re.search(r'neu la mot khoang a b thi nhap (?:gia tri )?(\d{1,6})\b', text)
    answer = str(question.get('ans', '')).strip().replace(',', '.')
    if not code_match or not re.fullmatch(r'[+-]?\d{1,6}(?:\.\d{1,6})?', answer):
        return ''
    code = sp.Rational(code_match[1])
    if sp.Rational(answer) == code:
        return ''
    task = 'tim gia tri thuc cua tham so m de do thi ham so co hai diem cuc tri nam ve hai phia cua truc tung'
    if task not in text:
        return ''
    tail = text.split(task, 1)[1].strip()
    expected_tail = ('neu co nhieu gia tri hay tinh tong cua chung neu la mot khoang a b thi nhap gia tri '
                     + code_match[1] + ' neu khong co gia tri nao thoa man nhap 0')
    known_note = ' biet rang yeu cau bai toan tuong duong voi phuong trinh y 0 co hai nghiem trai dau'
    if tail not in (expected_tail, expected_tail + known_note):
        return ''
    task_start = re.search(r'\btìm\b', raw, re.I)
    if not task_start:
        return ''
    for formula in list(re.finditer(r'(?:\by|\bf\s*\(\s*x\s*\))\s*=\s*([^$\n;]+)', raw))[:3]:
        expression = formula[1]
        if formula.end() > task_start.start() or folded(raw[:formula.start()] + raw[formula.end():task_start.start()]) != 'cho ham so bac ba':
            continue
        if len(expression) > 160 or not re.fullmatch(r'[0-9xm+\-*/^().{}\s]+', expression):
            continue
        value = expression.replace('m', 't').replace('^', '**').replace('{', '(').replace('}', ')')
        value = re.sub(r'(?<=[0-9xt)])(?=[xt(])', '*', value)
        try:
            polynomial = parse_math_expression(value)
            x, t = sp.symbols('x t', real=True)
            if not polynomial.is_polynomial(x, t) or sp.degree(polynomial, x) != 3:
                continue
            a, b, c, d = [sp.expand(polynomial).coeff(x, i) for i in (3, 2, 1, 0)]
            if a.free_symbols or a == 0 or sp.degree(b, t) > 1 or sp.degree(c, t) != 2:
                continue
            # Derivative roots exist for every real parameter in this narrow case.
            discriminant = sp.simplify(4*b*b - 12*a*c)
            if discriminant.free_symbols or discriminant.is_positive is not True:
                continue
            solution = sp.solve_univariate_inequality(c/a < 0, t, relational=False)
            if isinstance(solution, sp.Interval) and solution.measure.is_positive is True:
                return 'parameter_interval_code_answer_mismatch'
        except (ValueError, TypeError, NotImplementedError, ZeroDivisionError):
            continue
    return ''
