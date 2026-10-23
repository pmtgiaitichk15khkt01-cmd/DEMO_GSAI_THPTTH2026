# VIP 74.1 - HỆ THỐNG GIA SƯ AI THPT 2026 (CHUẨN GDPT 2018 - BẢN VÁ HOÀN THIỆN ĐA MÔN & ĐA KHỐI LỚP)
# -*- coding: utf-8 -*-
"""
exam_file_extractor.py - Đọc đề thi từ Word (.docx) / PDF và tách câu hỏi (VIP 66.2).
Cập nhật VIP 66.2 (18/10/2026): Đồng bộ chuẩn hóa bóc tách đề thi THPT Quốc gia 2026.

API chính:
    res = extract_exam_file(file_bytes, filename)
        -> {"text": str, "answer_hints": {so_cau: "A"}, "images": [(name, bytes)],
            "warnings": [str], "needs_ocr": bool}
    qs  = split_exam_text(res["text"], res["answer_hints"])
        -> [{"part":"p1|p2|p3","no":int,"q":str,"opt":[...],"stmts":[{"t","a"}],"ans":str|None}]

Sửa các lỗi của extract_text_from_file_upload cũ:
  Word: công thức bị in 2 lần; phân số/căn/mũ/chỉ số/tích phân/hệ phương trình bị dẹt phẳng;
        chữ trong hộp văn bản bị trùng (AlternateContent); đánh số tự động "Câu %1" bị mất;
        gạch chân/tô màu đáp án đúng bị mất; ảnh/MathType không được ghi nhận.
  PDF : đề 2 cột bị đọc lẫn dòng; tiêu đề/chân trang lặp; Unicode tiếng Việt dạng tổ hợp;
        file scan (không có text) không được báo.
"""
import io, re, zipfile, unicodedata, collections
from lxml import etree

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
M = "http://schemas.openxmlformats.org/officeDocument/2006/math"
MC = "http://schemas.openxmlformats.org/markup-compatibility/2006"
NS = {"w": W, "m": M, "mc": MC}
def _w(t): return "{%s}%s" % (W, t)
def _m(t): return "{%s}%s" % (M, t)

# ----------------------------------------------------------------- OMML -> LaTeX
_SYM = {"≤": r"\le ", "≥": r"\ge ", "≠": r"\ne ", "∞": r"\infty ", "→": r"\to ", "⇒": r"\Rightarrow ",
        "⇔": r"\Leftrightarrow ", "∈": r"\in ", "∉": r"\notin ", "⊂": r"\subset ", "⊆": r"\subseteq ",
        "∩": r"\cap ", "∪": r"\cup ", "∅": r"\emptyset ", "∀": r"\forall ", "∃": r"\exists ", "±": r"\pm ",
        "×": r"\times ", "·": r"\cdot ", "÷": r"\div ", "≈": r"\approx ", "∥": r"\parallel ", "⊥": r"\perp ",
        "∠": r"\angle ", "△": r"\triangle ", "°": r"^\circ ", "−": "-", "π": r"\pi ", "α": r"\alpha ",
        "β": r"\beta ", "γ": r"\gamma ", "δ": r"\delta ", "Δ": r"\Delta ", "θ": r"\theta ", "λ": r"\lambda ",
        "μ": r"\mu ", "ω": r"\omega ", "Ω": r"\Omega ", "φ": r"\varphi ", "ε": r"\varepsilon ", "∑": r"\sum ",
        "∫": r"\int ", "∏": r"\prod ", "√": r"\sqrt ", "ℝ": r"\mathbb{R}", "ℕ": r"\mathbb{N}", "ℤ": r"\mathbb{Z}",
        "ℚ": r"\mathbb{Q}", "∘": r"\circ ", "⃗": ""}
_FUNCS = {"sin", "cos", "tan", "cot", "log", "ln", "lim", "max", "min", "sup", "inf", "arcsin", "arccos", "arctan"}

def _sym(s):
    return "".join(_SYM.get(c, c) for c in s)

def _omml(el):
    """Chuyển 1 phần tử OMML sang LaTeX (đệ quy)."""
    tag = etree.QName(el).localname
    def kids(name):
        k = el.find(_m(name))
        return "".join(_omml(c) for c in k) if k is not None else ""
    if tag in ("oMath", "oMathPara", "e", "num", "den", "sub", "sup", "deg", "lim", "fName", "box", "phant"):
        return "".join(_omml(c) for c in el)
    if tag == "r":
        t = "".join(x.text or "" for x in el.findall(_m("t")))
        t = _sym(t)
        sty = el.find("m:rPr/m:sty", NS)
        if sty is not None and sty.get(_m("val")) == "p" and t.strip().isalpha() and len(t.strip()) > 1:
            return r"\text{%s}" % t.strip() if t.strip() not in _FUNCS else "\\" + t.strip() + " "
        t2 = t.strip()
        if t2 in _FUNCS and t2 not in ("max", "min", "sup", "inf") or t2 in ("max", "min"):
            return "\\" + t2 + " "
        return t
    if tag == "f":
        typ = el.find("m:fPr/m:type", NS)
        if typ is not None and typ.get(_m("val")) == "noBar":
            return r"\binom{%s}{%s}" % (kids("num"), kids("den"))
        return r"\frac{%s}{%s}" % (kids("num"), kids("den"))
    if tag == "rad":
        hide = el.find("m:radPr/m:degHide", NS)
        deg = kids("deg").strip()
        if hide is not None and hide.get(_m("val")) in ("1", "true", "on") or not deg:
            return r"\sqrt{%s}" % kids("e")
        return r"\sqrt[%s]{%s}" % (deg, kids("e"))
    if tag == "sSup": return "{%s}^{%s}" % (kids("e"), kids("sup"))
    if tag == "sSub": return "{%s}_{%s}" % (kids("e"), kids("sub"))
    if tag == "sSubSup": return "{%s}_{%s}^{%s}" % (kids("e"), kids("sub"), kids("sup"))
    if tag == "sPre": return "{}_{%s}^{%s}{%s}" % (kids("sub"), kids("sup"), kids("e"))
    if tag == "d":
        pr = el.find("m:dPr", NS)
        beg, end, sep = "(", ")", "|"
        if pr is not None:
            b = pr.find("m:begChr", NS); e_ = pr.find("m:endChr", NS); s = pr.find("m:sepChr", NS)
            if b is not None: beg = b.get(_m("val"), "")
            if e_ is not None: end = e_.get(_m("val"), "")
            if s is not None: sep = s.get(_m("val"), "|")
        inner = (sep if sep != "|" else ",").join("".join(_omml(c) for c in e) for e in el.findall(_m("e")))
        L = {"{": r"\left\{ ", "": r"\left. ", "[": r"\left[ ", "⟨": r"\left\langle ", "|": r"\left| ", "(": r"\left( "}.get(beg, r"\left" + beg + " ")
        R = {"}": r" \right\}", "": r" \right.", "]": r" \right]", "⟩": r" \right\rangle", "|": r" \right|", ")": r" \right)"}.get(end, r" \right" + end)
        if beg == "{" and end == "":
            return r"\begin{cases}%s\end{cases}" % inner.replace(",", r"\\ ") if not el.findall(".//m:eqArr", NS) else r"\begin{cases}%s\end{cases}" % "".join(_omml(c) for c in el.findall(_m("e"))[0])
        return L + inner + R
    if tag == "eqArr":
        return r"\\ ".join("".join(_omml(c) for c in e) for e in el.findall(_m("e")))
    if tag == "nary":
        pr = el.find("m:naryPr/m:chr", NS)
        ch = pr.get(_m("val")) if pr is not None else "∫"
        op = _SYM.get(ch, ch).strip()
        sub, sup = kids("sub"), kids("sup")
        out = op + (("_{%s}" % sub) if sub else "") + (("^{%s}" % sup) if sup else "")
        return out + " " + kids("e")
    if tag == "func": return kids("fName") + " " + kids("e")
    if tag == "limLow": return r"\underset{%s}{%s}" % (kids("lim"), kids("e")) if kids("e").strip() not in ("lim", r"\lim") else r"\lim_{%s}" % kids("lim")
    if tag == "limUpp": return r"\overset{%s}{%s}" % (kids("lim"), kids("e"))
    if tag == "acc":
        c = el.find("m:accPr/m:chr", NS); ch = c.get(_m("val")) if c is not None else "̂"
        cmd = {"⃗": "vec", "→": "vec", "̂": "hat", "̄": "overline", "¯": "overline", "̃": "tilde", "̇": "dot"}.get(ch, "vec")
        return "\\%s{%s}" % (cmd, kids("e"))
    if tag == "bar":
        return r"\overline{%s}" % kids("e")
    if tag == "groupChr": return kids("e")
    if tag == "m":
        rows = []
        for mr in el.findall(_m("mr")):
            rows.append(" & ".join("".join(_omml(c) for c in e) for e in mr.findall(_m("e"))))
        return r"\begin{matrix}%s\end{matrix}" % r" \\ ".join(rows)
    if tag.endswith("Pr"): return ""
    return "".join(_omml(c) for c in el)


def omml_to_latex(el):
    s = _omml(el)
    s = re.sub(r"\s+", " ", s).strip()
    return s

# ----------------------------------------------------------------- DOCX
class _Numbering:
    """Đánh số tự động của Word (vd 'Câu %1.', 'A.', 'a)')."""
    def __init__(self, z):
        self.abs, self.num, self.cnt = {}, {}, collections.defaultdict(int)
        if "word/numbering.xml" not in z.namelist(): return
        r = etree.fromstring(z.read("word/numbering.xml"))
        for a in r.findall("w:abstractNum", NS):
            lv = {}
            for l in a.findall("w:lvl", NS):
                fmt = l.find("w:numFmt", NS); txt = l.find("w:lvlText", NS); st = l.find("w:start", NS)
                lv[int(l.get(_w("ilvl")))] = (fmt.get(_w("val")) if fmt is not None else "decimal",
                                              txt.get(_w("val")) if txt is not None else "",
                                              int(st.get(_w("val"))) if st is not None else 1)
            self.abs[a.get(_w("abstractNumId"))] = lv
        for n in r.findall("w:num", NS):
            a = n.find("w:abstractNumId", NS)
            self.num[n.get(_w("numId"))] = a.get(_w("val")) if a is not None else None

    @staticmethod
    def _fmt(n, f):
        if f == "upperLetter": return chr(64 + (n - 1) % 26 + 1)
        if f == "lowerLetter": return chr(96 + (n - 1) % 26 + 1)
        if f == "upperRoman" or f == "lowerRoman":
            v = [(10, "x"), (9, "ix"), (5, "v"), (4, "iv"), (1, "i")]; o = ""
            for k, s in v:
                while n >= k: o += s; n -= k
            return o.upper() if f == "upperRoman" else o
        if f in ("bullet", "none"): return ""
        return str(n)

    def label(self, p):
        npr = p.find("w:pPr/w:numPr", NS)
        if npr is None: return ""
        nid = npr.find("w:numId", NS); il = npr.find("w:ilvl", NS)
        if nid is None or nid.get(_w("val")) == "0": return ""
        nid = nid.get(_w("val")); il = int(il.get(_w("val"))) if il is not None else 0
        lv = self.abs.get(self.num.get(nid), {})
        if il not in lv: return ""
        fmt, txt, start = lv[il]
        if fmt == "bullet": return ""
        key = (nid, il)
        self.cnt[key] = self.cnt[key] + 1 if self.cnt[key] else start
        for k in list(self.cnt):                      # reset cấp thấp hơn
            if k[0] == nid and k[1] > il: self.cnt[k] = 0
        def rep(m):
            L = int(m.group(1)) - 1
            f2 = lv.get(L, ("decimal",))[0]
            return self._fmt(self.cnt[(nid, L)] or 1, f2)
        return re.sub(r"%(\d)", rep, txt).strip()


def _run_text(r, ctx):
    out = []
    for c in r:
        t = etree.QName(c).localname
        if t == "t": out.append(c.text or "")
        elif t == "tab": out.append(" ")
        elif t in ("br", "cr"): out.append("\n" if c.get(_w("type")) != "page" else "\n")
        elif t == "noBreakHyphen": out.append("-")
        elif t == "sym":
            ch = c.get(_w("char"))
            try: out.append(chr(int(ch, 16)) if ch else "")
            except Exception: pass
        elif t in ("drawing", "pict", "object"):
            n = len(c.findall(".//{*}blip")) + len(c.findall(".//{*}imagedata"))
            if c.findall(".//{*}OLEObject") or t == "object":
                ctx["warnings"].add("Có công thức MathType/OLE (dạng ảnh) - nên dùng AI đa phương thức đọc trang đó")
            if n:
                ctx["img_n"] += 1
                out.append(" [[IMG%d]] " % ctx["img_n"])
            for tb in c.findall(".//w:txbxContent", NS):
                # chỉ lấy hộp văn bản nếu KHÔNG nằm trong mc:Fallback
                anc = [etree.QName(a).localname for a in tb.iterancestors()]
                if "Fallback" in anc: continue
                out.append(" " + " ".join(_para(p, ctx)[0] for p in tb.findall("w:p", NS)) + " ")
    return "".join(out)


def _para(p, ctx):
    """Trả (text, info). Duyệt theo thứ tự thật, không duyệt lặp."""
    parts, first_fmt = [], None
    def walk(node):
        nonlocal first_fmt
        for c in node:
            t = etree.QName(c).localname
            if t == "r":
                txt = _run_text(c, ctx)
                if txt.strip() and first_fmt is None:
                    u = c.find("w:rPr/w:u", NS); col = c.find("w:rPr/w:color", NS); hl = c.find("w:rPr/w:highlight", NS)
                    first_fmt = {"u": u is not None and u.get(_w("val")) not in ("none", "0"),
                                 "color": (col.get(_w("val")) if col is not None else None),
                                 "hl": hl is not None, "txt": txt.strip()}
                parts.append(txt)
            elif t in ("oMath",):
                parts.append(" $" + omml_to_latex(c) + "$ ")
            elif t == "oMathPara":
                parts.append(" $" + " ".join(omml_to_latex(x) for x in c.findall(_m("oMath"))) + "$ ")
            elif t in ("hyperlink", "smartTag", "ins", "sdt", "sdtContent", "fldSimple", "customXml"):
                walk(c)
            elif t == "AlternateContent":
                ch = c.find("mc:Choice", NS)
                walk(ch if ch is not None else c)       # bỏ Fallback -> hết trùng
            elif t == "del":
                continue                                  # bỏ phần đã xóa (track changes)
    walk(p)
    txt = "".join(parts)
    txt = re.sub(r"[ \t\u00a0]+", " ", txt).replace(" $ $ ", " ")
    txt = re.sub(r"\$\s*\$", "", txt)
    txt = txt.replace("$ $", " ")
    return txt.strip(), first_fmt


_RED = {"FF0000", "C00000", "E00000", "FF3300"}

def extract_docx(file_bytes):
    ctx = {"warnings": set(), "img_n": 0}
    hints, images, lines = {}, [], []
    with zipfile.ZipFile(io.BytesIO(file_bytes)) as z:
        numbering = _Numbering(z)
        _raw = z.read("word/document.xml")
        mathtype_count = len(re.findall(rb'ProgID="Equation\.', _raw))
        root = etree.fromstring(_raw)
        body = root.find("w:body", NS)
        for n in sorted(x for x in z.namelist() if x.startswith("word/media/")):
            images.append((n.split("/")[-1], z.read(n)))
        cur_q = [0]

        def handle_p(p):
            lab = numbering.label(p)
            txt, ff = _para(p, ctx)
            if lab and txt and not re.match(r"^(câu|bài|[A-Da-d][\.\)])", txt, re.I):
                txt = lab + " " + txt
            elif lab and not txt:
                return
            if not txt: return
            m = re.match(r"^(?:câu|bài)\s*(\d+)", txt, re.I)
            if m: cur_q[0] = int(m.group(1))
            mo = re.match(r"^([A-D])\s*[\.\)]", txt)
            if mo and cur_q[0] and ff and (ff["u"] or ff["hl"] or (ff["color"] or "").upper() in _RED):
                if ff["txt"][:2].rstrip(".) ").upper() in ("A", "B", "C", "D"):
                    hints[cur_q[0]] = mo.group(1)
            lines.append(txt)

        def handle_tbl(tbl):
            for tr in tbl.findall("w:tr", NS):
                cells = []
                for tc in tr.findall("w:tc", NS):
                    cells.append(" ".join(_para(p, ctx)[0] for p in tc.findall(".//w:p", NS)).strip())
                if any(cells): lines.append(" | ".join(cells))

        for ch in body:
            t = etree.QName(ch).localname
            if t == "p": handle_p(ch)
            elif t == "tbl": handle_tbl(ch)
            elif t == "sdt":
                for p in ch.findall(".//w:p", NS): handle_p(p)
    text = unicodedata.normalize("NFC", "\n".join(lines))
    return {"text": text, "answer_hints": hints, "images": images,
            "warnings": sorted(ctx["warnings"]), "needs_ocr": False, "mathtype_count": mathtype_count}

# ----------------------------------------------------------------- PDF
_PUA = re.compile(r"[\ue000-\uf8ff]")

def _clean_pdf_text(t):
    t = unicodedata.normalize("NFC", t)                       # sửa dấu tiếng Việt dạng tổ hợp
    for a, b in (("ﬁ", "fi"), ("ﬂ", "fl"), ("\u00ad", ""), ("\u200b", ""), ("\uf0b7", "-")):
        t = t.replace(a, b)
    t = t.replace("−", "-").replace("–", "-")
    return t


def _columns_words(words, width):
    """words: list[(x0,top,x1,bottom,text)] -> văn bản đúng thứ tự, tự nhận đề 1 hay 2 cột."""
    if not words: return ""
    mid = width / 2
    # có khoảng trống dọc ở giữa trang + đủ chữ cả hai bên => 2 cột
    span = [w for w in words if w[0] < mid - 6 and w[2] > mid + 6 and (w[2] - w[0]) > 12]
    gap = len(span) <= max(3, 0.04 * len(words))          # vài từ tiêu đề/chân trang vắt qua giữa là bình thường
    left = [w for w in words if (w[0] + w[2]) / 2 < mid]
    right = [w for w in words if (w[0] + w[2]) / 2 >= mid]
    two = gap and len(left) > 25 and len(right) > 25 and min(len(left), len(right)) >= 0.25 * len(words)
    groups = [left, right] if two else [words]
    out = []
    for g in groups:
        g = sorted(g, key=lambda w: (round(w[1] / 3), w[0]))
        line, last_top, cur = [], None, []
        for w in g:
            if last_top is not None and abs(w[1] - last_top) > 4:
                out.append(" ".join(cur)); cur = []
            cur.append(w[4]); last_top = w[1]
        if cur: out.append(" ".join(cur))
    return "\n".join(out)


def extract_pdf(file_bytes):
    warnings, pages = [], []
    try:
        import pdfplumber
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for pg in pdf.pages:
                ws = [(w["x0"], w["top"], w["x1"], w["bottom"], w["text"]) for w in
                      pg.extract_words(keep_blank_chars=False, use_text_flow=False, x_tolerance=1.5, y_tolerance=2)]
                pages.append((pg.height, _columns_words(ws, pg.width)))
    except Exception as e:                                         # dự phòng
        try:
            import pypdf
            for p in pypdf.PdfReader(io.BytesIO(file_bytes)).pages:
                pages.append((800, p.extract_text() or ""))
            warnings.append("Đọc bằng pypdf (kém hơn): đề 2 cột có thể lẫn dòng. Nên cài pdfplumber hoặc pymupdf")
        except Exception as e2:
            warnings.append("Không đọc được PDF: %s" % e2)
    texts = [_clean_pdf_text(t) for _, t in pages]
    # bỏ dòng lặp ở đầu/cuối trang (tiêu đề, mã đề, số trang). Chỉ che SỐ TRANG, không che chữ số khác,
    # và không bao giờ xóa dòng bắt đầu bằng Câu/Bài/A./B./PHẦN.
    def _hf_key(l):
        k = re.sub(r"(?i)trang\s*\d+(\s*/\s*\d+)?", "trang #", l.strip())
        return re.sub(r"^\d+$", "#", k)
    _keep = re.compile(r"^\s*(?:câu|bài|phần|[A-Da-d][\.\)])", re.I)
    if len(texts) >= 3:
        cnt = collections.Counter()
        for t in texts:
            ls = [l.strip() for l in t.split("\n") if l.strip()]
            for l in set(ls[:2] + ls[-2:]):
                if not _keep.match(l): cnt[_hf_key(l)] += 1
        rep = {k for k, v in cnt.items() if v >= max(3, 0.6 * len(texts))}
        texts = ["\n".join(l for l in t.split("\n") if _keep.match(l) or _hf_key(l) not in rep) for t in texts]
    full = "\n".join(texts)
    full = re.sub(r"^\s*(?:trang\s*)?\d+\s*/\s*\d+\s*$|^\s*-\s*\d+\s*-\s*$|^\s*(?i:trang)\s*$", "", full, flags=re.M)
    full = re.sub(r"\n{2,}", "\n", full)
    nchar = len(re.sub(r"\s", "", full))
    needs_ocr = nchar < 80 * max(1, len(texts)) * 0.25
    if needs_ocr: warnings.append("PDF là bản scan/ảnh (gần như không có chữ) - cần OCR hoặc đưa thẳng cho AI đa phương thức")
    pua = len(_PUA.findall(full))
    if pua > 5:
        warnings.append("Có %d ký tự font toán đặc biệt - công thức PDF không đọc chính xác; nên đối chiếu hoặc dùng AI đa phương thức" % pua)
        full = _PUA.sub("", full)
    if re.search(r"\b\d+\s*\n\s*\d+\b", full) and re.search(r"[=<>]\s*$", full, re.M):
        warnings.append("Phân số/căn trong PDF thường bị tách dòng - kiểm tra lại các câu có công thức")
    return {"text": full.strip(), "answer_hints": {}, "images": [], "warnings": warnings, "needs_ocr": needs_ocr}


def extract_exam_file(file_bytes, filename):
    f = filename.lower()
    if f.endswith(".docx"): return extract_docx(file_bytes)
    if f.endswith(".pdf"): return extract_pdf(file_bytes)
    for enc in ("utf-8", "utf-16", "cp1258"):
        try:
            return {"text": unicodedata.normalize("NFC", file_bytes.decode(enc)), "answer_hints": {}, "images": [], "warnings": [], "needs_ocr": False}
        except Exception:
            continue
    return {"text": "", "answer_hints": {}, "images": [], "warnings": ["Không nhận diện được mã hóa"], "needs_ocr": False}

# ----------------------------------------------------------------- Tách câu
_PART = re.compile(r"^\s*(?:PHẦN|Phần)\s*(I{1,3}|[123])\b", re.M)
_QSTART = re.compile(r"^\s*(?:Câu|CÂU|Bài)\s*(\d+)\s*[\.\:\)]?\s*", re.M)
_OPT_SPLIT = re.compile(r"(?:(?<=\s)|^)([A-D])\s*[\.\)]\s+")
_STMT_SPLIT = re.compile(r"(?:(?<=\s)|^)([a-d])\s*\)\s+")
_ROMAN = {"I": "p1", "II": "p2", "III": "p3", "1": "p1", "2": "p2", "3": "p3"}


def split_exam_text(text, answer_hints=None):
    answer_hints = answer_hints or {}
    # cắt phần "BẢNG ĐÁP ÁN / HƯỚNG DẪN GIẢI" ở cuối nếu có
    cut = re.search(r"^\s*(?:BẢNG ĐÁP ÁN|ĐÁP ÁN|HƯỚNG DẪN GIẢI|LỜI GIẢI)\b", text, re.M | re.I)
    key_text = text[cut.start():] if cut and cut.start() > len(text) * 0.4 else ""
    body = text[:cut.start()] if key_text else text
    part_marks = [(m.start(), _ROMAN[m.group(1)]) for m in _PART.finditer(body)]
    qs = list(_QSTART.finditer(body))
    out = []
    for i, m in enumerate(qs):
        end = qs[i + 1].start() if i + 1 < len(qs) else len(body)
        block = body[m.end():end].strip()
        part = "p1"
        for pos, p in part_marks:
            if pos <= m.start(): part = p
        no = int(m.group(1))
        item = {"part": part, "no": no, "q": block, "opt": [], "stmts": [], "ans": answer_hints.get(no)}
        flat = re.sub(r"\n+", " \n", block)
        so = list(_OPT_SPLIT.finditer(flat))
        ss = list(_STMT_SPLIT.finditer(flat))
        if len(ss) >= 3 and part != "p1":
            item["q"] = flat[:ss[0].start()].strip()
            for j, s in enumerate(ss):
                e = ss[j + 1].start() if j + 1 < len(ss) else len(flat)
                item["stmts"].append({"t": flat[s.end():e].strip(), "a": None})
            item["part"] = "p2"
        elif len(so) >= 4 and [x.group(1) for x in so[:4]] == ["A", "B", "C", "D"]:
            item["q"] = flat[:so[0].start()].strip()
            for j, s in enumerate(so[:4]):
                e = so[j + 1].start() if j + 1 < 4 else len(flat)
                item["opt"].append("%s. %s" % (s.group(1), flat[s.end():e].strip()))
            item["part"] = "p1"
        elif part == "p1" and not so:
            item["part"] = "p3"
        out.append(item)
    if key_text:                                                     # đáp án dạng "1.A 2.B" hoặc "Câu 1: A"
        for no, a in re.findall(r"(?:Câu\s*)?(\d{1,2})\s*[\.\:\-\)]?\s*([A-D])\b", key_text):
            for it in out:
                if it["no"] == int(no) and not it["ans"] and it["part"] == "p1": it["ans"] = a
    return out
