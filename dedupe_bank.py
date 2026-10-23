# VIP 74.1 - HỆ THỐNG GIA SƯ AI THPT 2026 (CHUẨN GDPT 2018 - BẢN VÁ HOÀN THIỆN ĐA MÔN & ĐA KHỐI LỚP)
# -*- coding: utf-8 -*-
"""
HỆ THỐNG GSAI - THPT 2026 (VIP 66.2): dedupe_bank.py
Loại câu trùng ngữ liệu trong ngân hàng đề GSAI, đồng bộ quy chuẩn Chốt Chặn Cuối Cùng VIP 66.2 (18/10/2026).

Dùng độc lập:
    python dedupe_bank.py exams_To_n_h_c_json.xz  out_dir

Dùng trong app (thay MỌI hàm get_q_fingerprint cũ):
    from dedupe_bank import q_fingerprint, q_family_fingerprint

Quy ước:
  - TRÙNG HẲN (exact): cùng nội dung sau chuẩn hóa (bỏ "Câu n", $, \\, khoảng trắng,
    \\dfrac->\\frac, ...). CHỮ SỐ ĐƯỢC GIỮ NGUYÊN, nên 2 câu chỉ khác số liệu là KHÁC NHAU.
    Thứ tự phương án A/B/C/D không ảnh hưởng (đảo đáp án vẫn bị coi là trùng).
  - GẦN TRÙNG (near): chung họ số liệu, độ giống n-gram >= NEAR_THRESHOLD.
  - HỌ MẪU (family): cùng văn bản nhưng khác số -> KHÔNG xóa, chỉ thống kê độ đa dạng.
"""
import sys, os, re, json, lzma, gzip, csv, hashlib, collections, unicodedata

NEAR_THRESHOLD = 0.90

_LATEX_ALIAS = [
    (r"\\dfrac|\\tfrac", r"\\frac"),
    (r"\\left|\\right", ""),
    (r"\\leqslant|\\leq", r"\\le"),
    (r"\\geqslant|\\geq", r"\\ge"),
    (r"\\neq", r"\\ne"),
    (r"\\displaystyle|\\textstyle|\\,|\\;|\\!|\\quad|\\qquad", ""),
    (r"\\mathrm|\\mathbf|\\text", ""),
    (r"\\varnothing|\\emptyset", "emptyset"),
    (r"\\to|\\rightarrow", "->"),
    (r"\\infty", "inf"),
]
_QNUM = re.compile(r"^\s*(?:(?:câu|bài)\s*\d+\s*[\.\:\)]\s*)+", re.I)
_OPT_PREFIX = re.compile(r"^\s*[A-Da-d]\s*[\.\)]\s*")


def _norm(s):
    s = unicodedata.normalize("NFC", str(s or ""))
    s = _QNUM.sub("", s).lower()
    for pat, rep in _LATEX_ALIAS:
        s = re.sub(pat, rep, s)
    s = s.replace("−", "-").replace("–", "-").replace("×", "*").replace("·", "*")
    s = re.sub(r"(?<=\d),(?=\d)", ".", s)            # 1,5 == 1.5
    s = re.sub(r"[\s\$\\\{\}\(\)\[\]\.\,\:\;\'\"`~_^]+", "", s)
    return s


def _opts(q):
    o = q.get("opt") or []
    return sorted(_norm(_OPT_PREFIX.sub("", str(x))) for x in o)


def _stmts(q):
    out = []
    for s in q.get("stmts") or []:
        if isinstance(s, dict):
            out.append(_norm(s.get("t", "")) + ("|T" if s.get("a") else "|F"))
        else:
            out.append(_norm(s))
    return sorted(out)


def q_fingerprint(q):
    """Dấu vân tay chính xác. Chữ số được giữ. Phương án/mệnh đề không phụ thuộc thứ tự."""
    if not isinstance(q, dict):
        return ""
    payload = "§".join([_norm(q.get("q", "")), "¦".join(_opts(q)), "¦".join(_stmts(q))])
    return hashlib.sha1(payload.encode("utf-8")).hexdigest()


def q_family_fingerprint(q):
    """Họ mẫu: như trên nhưng che hết chữ số (để đo độ đa dạng, KHÔNG dùng để xóa)."""
    if not isinstance(q, dict):
        return ""
    payload = "§".join([_norm(q.get("q", "")), "¦".join(_opts(q)), "¦".join(_stmts(q))])
    payload = re.sub(r"\d+", "#", payload)
    return hashlib.sha1(payload.encode("utf-8")).hexdigest()


def _digits(q):
    t = " ".join([str(q.get("q", ""))] + [str(x) for x in (q.get("opt") or [])]
                 + [str(s.get("t", "")) if isinstance(s, dict) else str(s) for s in (q.get("stmts") or [])])
    return tuple(sorted(re.findall(r"\d+(?:[.,]\d+)?", t)))


def _grams(q, n=5):
    t = _norm(q.get("q", "")) + "".join(_opts(q)) + "".join(_stmts(q))
    return {t[i:i + n] for i in range(max(1, len(t) - n + 1))}


def _quality(q):
    """Điểm để chọn bản đại diện: đủ đáp án, lời giải, hình > thiếu."""
    s = 0
    if q.get("ans") not in (None, "") or q.get("stmts"): s += 4
    if len(str(q.get("explain", ""))) > 30: s += 3
    if q.get("opt") or q.get("stmts"): s += 1
    for k in ("f", "bbt", "geom_3d", "tikz", "mslgn_data", "composite_visual"):
        if q.get(k): s += 1
    if q.get("var_warning"): s -= 3
    return s


def load_bank(path):
    op = lzma.open if path.endswith(".xz") else gzip.open if path.endswith(".gz") else open
    with op(path, "rt", encoding="utf-8") as f:
        d = json.load(f)
    return d["exams"] if isinstance(d, dict) and "exams" in d else d


def run(path, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    exams = load_bank(path)
    groups = collections.OrderedDict()     # key -> list[(exam_idx, part, pos, q)]
    total = 0
    for ei, e in enumerate(exams):
        for part in ("p1", "p2", "p3"):
            for pos, q in enumerate(e.get(part, []) or []):
                total += 1
                key = (str(e.get("subject", "")), str(e.get("grade", "")), part, q_fingerprint(q))
                groups.setdefault(key, []).append((ei, part, pos, q))
    exact_unique = len(groups)

    # --- gần trùng: gộp trong cùng (môn, lớp, phần, họ số liệu) ---
    reps = []   # (key, best_q, members)
    for key, mem in groups.items():
        best = max(mem, key=lambda m: _quality(m[3]))[3]
        reps.append([key, best, list(mem)])
    buckets = collections.defaultdict(list)
    for r in reps:
        buckets[(r[0][0], r[0][1], r[0][2], _digits(r[1]))].append(r)
    merged = []
    near_removed = 0
    for _, lst in buckets.items():
        kept = []
        for r in lst:
            g = _grams(r[1])
            hit = None
            for k in kept:
                gk = k[3]
                inter = len(g & gk)
                if inter / max(1, len(g | gk)) >= NEAR_THRESHOLD:
                    hit = k; break
            if hit:
                hit[2].extend(r[2]); near_removed += 1
                if _quality(r[1]) > _quality(hit[1]): hit[1] = r[1]
            else:
                kept.append([r[0], r[1], list(r[2]), g])
        merged.extend(kept)

    uniq = []
    fam = collections.Counter()
    per_pool = collections.Counter()
    rows = []
    for i, (key, best, mem, _g) in enumerate(merged, 1):
        q = dict(best)
        q["uid"] = f"U{i:06d}"
        q["seen_in_exams"] = len({m[0] for m in mem})
        q["dup_count"] = len(mem)
        uniq.append((key, q))
        fam[(key[0], key[1], key[2], q_family_fingerprint(best))] += 1
        per_pool[key[:3]] += 1
        if len(mem) > 1:
            rows.append([q["uid"], key[0], key[1], key[2], len(mem), q["seen_in_exams"], str(q.get("q", ""))[:90].replace("\n", " ")])

    # --- ghi kết quả ---
    out = collections.defaultdict(lambda: collections.defaultdict(list))
    for key, q in uniq:
        out[key[0]][key[1]].append({**q, "_part": key[2]})
    bank = {"version": "UNIQUE-" + str(len(uniq)), "total": len(uniq),
            "questions": {s: dict(g) for s, g in out.items()}}
    with lzma.open(os.path.join(out_dir, "unique_questions.json.xz"), "wt", encoding="utf-8", preset=9) as f:
        json.dump(bank, f, ensure_ascii=False)
    rows.sort(key=lambda r: -r[4])
    with open(os.path.join(out_dir, "dedupe_report.csv"), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f); w.writerow(["uid", "mon", "lop", "phan", "so_lan_lap", "so_de_chua", "trich_doan"]); w.writerows(rows)

    lines = [f"Tổng số câu đầu vào         : {total}",
             f"Số câu khác nhau (exact)    : {exact_unique}",
             f"Gộp thêm do gần trùng       : {near_removed}",
             f"SỐ CÂU DUY NHẤT SAU LỌC     : {len(uniq)}  ({len(uniq)/max(1,total):.2%} của đầu vào)",
             f"Số 'họ mẫu' (che số liệu)   : {len(fam)}",
             "", "Theo (môn, lớp, phần):"]
    for k, v in sorted(per_pool.items()):
        lines.append(f"  {k[0]} | lớp {k[1]} | {k[2]} : {v}")
    summary = "\n".join(lines)
    open(os.path.join(out_dir, "dedupe_summary.txt"), "w", encoding="utf-8").write(summary)
    print(summary)
    return bank


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__); sys.exit(1)
    run(sys.argv[1], sys.argv[2])
