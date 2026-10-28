"""Validated boundaries shared by the four stations. No credentials or UI state."""
import ast
import hashlib
import hmac
import json
import math
import re
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP


def split_api_keys(value):
    return list(dict.fromkeys(k for k in re.split(r"[,;\s]+", str(value or "").strip()) if k))


def admin_password_matches(candidate, configured):
    configured = str(configured or "").strip()
    candidate = str(candidate or "").strip()
    if configured.startswith("sha256:"):
        expected = configured.split(":", 1)[1]
        return len(expected) == 64 and hmac.compare_digest(hashlib.sha256(candidate.encode()).hexdigest(), expected)
    return bool(configured) and hmac.compare_digest(candidate.encode(), configured.encode())


def normalize_bool(value):
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)) and value in (0, 1):
        return bool(value)
    if isinstance(value, str):
        text = value.strip().casefold()
        if text in {"true", "đúng", "dung", "t", "1"}:
            return True
        if text in {"false", "sai", "f", "0"}:
            return False
    return None


def numeric_answer_matches(user_answer, expected_answer, decimals=None):
    """Default absolute tolerance only; rounding requires explicit question metadata."""
    user = "" if user_answer is None else str(user_answer).strip().replace(",", ".")
    expected = "" if expected_answer is None else str(expected_answer).strip().replace(",", ".")
    if not user or not expected:
        return False
    try:
        u, e = Decimal(user), Decimal(expected)
        if not u.is_finite() or not e.is_finite():
            return False
        if decimals is not None:
            digits = int(decimals)
            if not 0 <= digits <= 10:
                return False
            step = Decimal(1).scaleb(-digits)
            return u.quantize(step, rounding=ROUND_HALF_UP) == e.quantize(step, rounding=ROUND_HALF_UP)
        return abs(u - e) <= Decimal("0.015")
    except (InvalidOperation, ValueError, TypeError, OverflowError):
        return False


def parse_grade(value):
    match = re.fullmatch(r"(?:Lớp\s*)?(\d{1,2})", str(value).strip(), re.IGNORECASE)
    if not match or not 6 <= int(match.group(1)) <= 12:
        raise ValueError("Khối lớp phải nằm từ 6 đến 12.")
    return int(match.group(1))


def mcq_answer_matches(question, selected):
    if selected is None or not str(selected).strip():
        return False
    selected = str(selected).strip()
    options = [str(o).strip() for o in question.get("opt", [])]
    expected = str(question.get("ans") or "").strip().upper()
    if expected not in {"A", "B", "C", "D"}:
        return False
    if selected in options:
        return options.index(selected) == ord(expected) - ord("A")
    return selected.upper() == expected


def display_frame(frame):
    """Keep raw records unchanged; normalize mixed objects only for Arrow display."""
    result = frame.copy()
    def text(value):
        if value is None:
            return ""
        if isinstance(value, (dict, list, tuple)):
            return json.dumps(value, ensure_ascii=False, default=str)
        return str(value)
    for name in result.columns:
        if result[name].dtype == object:
            result[name] = result[name].map(text)
    return result


def paired_statistics(pre, post):
    import numpy as np
    from scipy import stats
    pre, post = np.asarray(pre, dtype=float), np.asarray(post, dtype=float)
    if pre.ndim != 1 or pre.shape != post.shape or len(pre) < 2 or not np.all(np.isfinite(pre)) or not np.all(np.isfinite(post)):
        raise ValueError("Cần ít nhất 2 cặp điểm hợp lệ của cùng học sinh.")
    if np.any((pre < 0) | (pre > 10) | (post < 0) | (post > 10)):
        raise ValueError("Điểm phải nằm trong thang 0–10.")
    diff = post - pre
    sd, gain = float(np.std(diff, ddof=1)), float(np.mean(diff))
    result = dict(n=len(pre), gain=gain, t=None, p=None, dz=None, ci=None,
                  hake=gain / (10 - float(np.mean(pre))) if float(np.mean(pre)) < 10 else None,
                  shapiro_p=None, wilcoxon_p=None)
    if sd <= 1e-12:
        return result
    test = stats.ttest_rel(post, pre)
    margin = float(stats.t.ppf(.975, len(pre)-1) * sd / math.sqrt(len(pre)))
    result.update(t=float(test.statistic), p=float(test.pvalue), dz=gain/sd, ci=(gain-margin, gain+margin))
    if 3 <= len(diff) <= 5000:
        result["shapiro_p"] = float(stats.shapiro(diff).pvalue)
    if len(diff) >= 3 and np.any(diff != 0):
        result["wilcoxon_p"] = float(stats.wilcoxon(diff).pvalue)
    return result


def parse_math_expression(source):
    """Construct SymPy nodes from a bounded AST; never evaluate Python strings."""
    import sympy as sp
    if not isinstance(source, str) or len(source) > 300 or "__" in source:
        return None
    symbols = dict(zip("xyzt", sp.symbols("x y z t", real=True)))
    functions = {"sin": sp.sin, "cos": sp.cos, "tan": sp.tan, "sqrt": sp.sqrt, "log": sp.log, "ln": sp.log, "exp": sp.exp}
    try:
        tree = ast.parse(source, mode="eval")
        nodes = list(ast.walk(tree))
        powers = [n for n in nodes if isinstance(n, ast.BinOp) and isinstance(n.op, ast.Pow)]
        if len(nodes) > 120 or len(powers) > 3 or any(any(isinstance(n, ast.Pow) for n in ast.walk(p.left)) for p in powers):
            return None
        def build(node, depth=0):
            if depth > 24:
                raise ValueError("Expression too deep")
            if isinstance(node, ast.Constant) and type(node.value) in (int, float) and math.isfinite(node.value) and abs(node.value) <= 1_000_000:
                return sp.Rational(str(node.value))
            if isinstance(node, ast.Name) and node.id in symbols:
                return symbols[node.id]
            if isinstance(node, ast.Name) and node.id in {"pi", "E"}:
                return sp.pi if node.id == "pi" else sp.E
            if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.USub, ast.UAdd)):
                val = build(node.operand, depth+1)
                return -val if isinstance(node.op, ast.USub) else val
            if isinstance(node, ast.BinOp):
                if isinstance(node.op, ast.Pow):
                    exponent_node = node.right
                    if isinstance(exponent_node, ast.UnaryOp) and isinstance(exponent_node.op, (ast.UAdd, ast.USub)):
                        exponent_node = exponent_node.operand
                    if not isinstance(exponent_node, ast.Constant) or type(exponent_node.value) not in (int, float) or abs(exponent_node.value) > 12:
                        raise ValueError("Exponent must be a small literal")
                left, right = build(node.left, depth+1), build(node.right, depth+1)
                if isinstance(node.op, ast.Add): return left + right
                if isinstance(node.op, ast.Sub): return left - right
                if isinstance(node.op, ast.Mult): return left * right
                if isinstance(node.op, ast.Div): return left / right
                if isinstance(node.op, ast.Pow): return left ** right
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in functions and len(node.args) == 1 and not node.keywords:
                return functions[node.func.id](build(node.args[0], depth+1))
            raise ValueError("Unsupported math syntax")
        result = build(tree.body)
        return result if isinstance(result, sp.Expr) and not result.has(sp.zoo, sp.nan, sp.oo, -sp.oo) else None
    except (ValueError, TypeError, SyntaxError, RecursionError, OverflowError, ZeroDivisionError):
        return None


def exam_response_metadata(exam, answers):
    """Versioned per-item correctness; raw choices are never interpreted as correctness."""
    results = {}
    content = {part: exam.get(part, []) for part in ("p1", "p2", "p3")}
    fingerprint = hashlib.sha256(json.dumps(content, ensure_ascii=False, sort_keys=True, default=str).encode()).hexdigest()
    for part, questions in content.items():
        for i, q in enumerate(questions):
            key = f"{part}_{i}"
            if part == "p1":
                results[key] = mcq_answer_matches(q, answers.get(key))
            elif part == "p3":
                results[key] = numeric_answer_matches(answers.get(key), q.get("ans"), q.get("rounding_decimals"))
            else:
                for j, stmt in enumerate(q.get("stmts", [])):
                    expected = normalize_bool(stmt.get("a", stmt.get("ans")))
                    selected = normalize_bool(answers.get(f"{key}_{j}"))
                    results[f"{key}_{j}"] = expected is not None and selected is not None and selected == expected
    return {"_exam_fingerprint": fingerprint, "_item_results": results}


def observed_item_matrix(logs):
    import numpy as np
    groups = {}
    seen = set()
    for entry in logs:
        if entry.get("type") not in (None, "EXAM_RESULT") or entry.get("grading_status") == "ai_reference":
            continue
        identity = entry.get("event_id") or entry.get("id")
        if identity and identity in seen:
            continue
        raw = entry.get("answers") or entry.get("answers_json") or {}
        try:
            answers = json.loads(raw) if isinstance(raw, str) else raw
            fingerprint, outcomes = answers.get("_exam_fingerprint"), answers.get("_item_results")
            if not fingerprint or not isinstance(outcomes, dict) or len(outcomes) < 2 or not all(type(v) is bool for v in outcomes.values()):
                continue
        except (ValueError, TypeError, AttributeError):
            continue
        if identity:
            seen.add(identity)
        keys = tuple(sorted(outcomes))
        groups.setdefault((fingerprint, keys), []).append([int(outcomes[k]) for k in keys])
    if not groups:
        return np.empty((0, 0)), []
    (_, keys), rows = max(groups.items(), key=lambda pair: len(pair[1]))
    if len(rows) < 3:
        return np.empty((0, 0)), []
    return np.asarray(rows, dtype=float), list(keys)
