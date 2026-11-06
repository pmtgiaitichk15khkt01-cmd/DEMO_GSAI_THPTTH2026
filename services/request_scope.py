"""Conservative checks for explicit request scope, not curriculum certification."""
import re

from services.academic_context import canonical_subject, folded


def explicit_request_scope(subject, request):
    if canonical_subject(subject) != "Toán học":
        return {}
    text = folded(request)
    pattern = r"\bchi (?:(?:dung|su dung|lay|khao sat|xet|ve do thi) (?:cac )?)?ham(?: so)? bac (?:ba|3)\b|\bonly cubic(?: functions?)?\b"
    for match in re.finditer(pattern, text):
        prefix = text[:match.start()].split()[-2:]
        if {"khong", "not"} & set(prefix):
            continue
        return {"function_family": "cubic_only"}
    return {}


def request_scope_prompt(scope):
    if scope.get("function_family") != "cubic_only":
        return ""
    return ("\nRàng buộc đã nhận diện từ yêu cầu: CHỈ HÀM BẬC BA. "
            "Giữ dạng hàm bậc ba trong câu gốc và câu thay thế; không thay bằng "
            "hàm bậc nhất, phân thức hoặc bậc bốn. Tính đồng/nghịch biến không xác định dạng hàm.\n")


def _model_family(model):
    if not isinstance(model, dict):
        return "unknown"
    kind = model.get("type")
    if kind in {"func_1_1", "func_2_1", "parabola", "func_2", "func_4", "quartic"}:
        return "noncubic"
    if kind in {"func_3", "cubic"}:
        try:
            import math
            a = float(model["a"])
            if math.isfinite(a):
                return "cubic" if a != 0 else "noncubic"
        except (KeyError, TypeError, ValueError, OverflowError):
            pass
    return "unknown"


def _primary_expressions(text):
    # Read declared functions, not answer options, derivatives or tangent lines.
    assignment = re.compile(r"(?:\by|\b[fghs]\s*\(\s*[xt]\s*\))\s*=\s*")
    for match in assignment.finditer(text[:10000]):
        prefix = folded(text[max(0, match.start()-100):match.start()])
        function_pos = max(prefix.rfind("ham so"), prefix.rfind("ham bac"))
        auxiliary_pos = max(prefix.rfind("duong thang"), prefix.rfind("tiep tuyen"), prefix.rfind("tiem can"))
        if auxiliary_pos > function_pos:
            continue
        rest = text[match.end():]
        alias = re.match(r"[fghs]\s*\(\s*[xt]\s*\)\s*=\s*", rest)
        if alias:
            rest = rest[alias.end():]
        rest = re.split(r"\$|\n|;", rest, maxsplit=1)[0]
        rest = re.split(r"\s+(?:và|có|là|trên|biết|thì|với|tại|đồng|nghịch)\b", rest, maxsplit=1, flags=re.I)[0]
        yield rest.strip().rstrip(". ,")


def _expression_family(expression):
    if not expression or len(expression) > 300:
        return "unknown"
    # Preserve domain evidence before symbolic cancellation (e.g. x^4/x).
    denominators = re.findall(r"\\(?:d?frac)\{[^{}]*\}\{([^{}]+)\}", expression)
    denominators += re.findall(r"/\s*\(([^()]*)\)", expression)
    if any(re.search(r"[xt]", value) for value in denominators) or re.search(r"/\s*[xt](?:\b|\^)", expression):
        return "noncubic"
    from services.neuro_symbolic_verifier import clean_latex_math_to_sympy_expr
    parsed = clean_latex_math_to_sympy_expr(expression)
    if parsed is None:
        return "unknown"
    try:
        import sympy as sp
        allowed = {sp.Symbol("x", real=True), sp.Symbol("t", real=True)}
        if parsed.free_symbols - allowed or len(parsed.free_symbols) > 1:
            return "unknown"
        variable = next(iter(parsed.free_symbols), sp.Symbol("x", real=True))
        if parsed.is_polynomial(variable):
            return "cubic" if sp.degree(parsed, variable) == 3 else "noncubic"
        if parsed.is_rational_function(variable):
            return "noncubic"
    except (TypeError, ValueError, NotImplementedError):
        pass
    return "unknown"


def question_scope_issue(question, scope):
    """Report demonstrated contradictions only; unknown is not a certification."""
    if scope.get("function_family") != "cubic_only" or not isinstance(question, dict):
        return ""
    if _standalone_grouped_statistics(question):
        return "outside_explicit_request"
    families = [_model_family(question.get("f"))]
    families.extend(_expression_family(value) for value in _primary_expressions(str(question.get("q", ""))))
    return "outside_explicit_request" if "noncubic" in families else ""


def _standalone_grouped_statistics(question):
    """Positive content evidence; never classify from the generic word 'khảo sát'."""
    text = folded(question.get("q", ""))
    grouped = any(term in text for term in ("mau so lieu ghep nhom", "bang so lieu ghep nhom", "bang mau so lieu ghep nhom"))
    # A question explicitly modelling observations with a function is not this case.
    function_context = any(term in text for term in ("ham so", "ham bac", "dao ham"))
    return grouped and not function_context


def question_topic_issue(question, subject, topics):
    """Detect this demonstrated metadata/content conflict, not general topic proof."""
    if canonical_subject(subject) != "Toán học" or not isinstance(question, dict):
        return ""
    selected = [folded(topic) for topic in topics]
    if not selected:
        return ""
    function_only = all(any(term in topic for term in ("ham so", "dao ham", "ham bac")) for topic in selected)
    statistics_allowed = any(any(term in topic for term in ("thong ke", "ghep nhom", "phan tan", "so lieu")) for topic in selected)
    if function_only and not statistics_allowed and _standalone_grouped_statistics(question):
        return "outside_selected_topic"
    return ""
