"""Exact global monotonicity checks for four explicit numeric polynomials."""
import re

import sympy as sp

from qa_runtime import parse_math_expression
from services.academic_context import folded


def polynomial_choice_conflict(question):
    raw = str(question.get('q', ''))
    if len(raw) > 2000:
        return ''
    domain = r'\\(?:mathbb|mathbf)\s*\{?\s*R\s*\}?|\(\s*-(?:\\infty|∞)\s*;\s*\+?(?:\\infty|∞)\s*\)|\bR\b'
    stem = folded(re.sub(domain, ' DOMAINR ', raw))
    match = re.fullmatch(r'ham so nao (?:duoi day|sau day) (dong bien|nghich bien) tren (?:khoang |toan bo )?domainr', stem)
    options = question.get('opt')
    if not match or not isinstance(options, list) or len(options) != 4:
        return ''
    increasing = match[1] == 'dong bien'
    x = sp.Symbol('x', real=True)
    truths = []
    for option in options:
        value = re.sub(r'^[A-D][.)]\s*', '', str(option).strip(), flags=re.I).strip('$').strip().rstrip('.')
        formula = re.fullmatch(r'(?:y|f\s*\(\s*x\s*\))\s*=\s*([0-9x+*/^().{}\-\s]+)', value)
        if not formula or len(formula[1]) > 160:
            return ''
        expression = formula[1].replace('^', '**').replace('{', '(').replace('}', ')')
        expression = re.sub(r'(?<=[0-9x)])(?=[x(])', '*', expression)
        try:
            polynomial = parse_math_expression(expression)
            if polynomial.free_symbols - {x} or not polynomial.is_polynomial(x):
                return ''
            polynomial = sp.Poly(polynomial, x)
            degree = polynomial.degree()
            if degree not in (0, 1, 2, 3):
                return ''
            derivative = polynomial.diff()
            if degree == 0:
                truths.append(False)
            elif degree == 1:
                slope = derivative.nth(0)
                truths.append(bool(slope > 0 if increasing else slope < 0))
            elif degree == 2:
                truths.append(False)  # A nonconstant linear derivative changes sign.
            else:
                a, b, c = derivative.all_coeffs()
                discriminant = sp.simplify(b*b - 4*a*c)
                # Equality is allowed: an isolated zero of the derivative does
                # not prevent strict monotonicity of a nonconstant polynomial.
                truths.append(bool(discriminant <= 0 and (a > 0 if increasing else a < 0)))
        except (ValueError, TypeError, NotImplementedError, ZeroDivisionError):
            return ''
    if sum(truths) != 1:
        return 'polynomial_choice_not_unique'
    key = str(question.get('ans', '')).strip().upper()
    if key in 'ABCD' and len(key) == 1 and not truths[ord(key)-ord('A')]:
        return 'polynomial_monotonic_choice_key_mismatch'
    return ''
