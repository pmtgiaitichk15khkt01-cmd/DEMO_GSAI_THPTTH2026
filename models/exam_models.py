# VIP 74.1 - HỆ THỐNG GIA SƯ AI THPT 2026 (CHUẨN GDPT 2018 - BẢN VÁ HOÀN THIỆN ĐA MÔN & ĐA KHỐI LỚP)
"""
MODULE QUẢN LÝ DỮ LIỆU & SCHEMA CHUẨN HÓA (DATA MODELS) - GSAI THPT 2026
Chuẩn hóa 100% cấu trúc câu hỏi và đề thi theo Quyết định 764/QĐ-BGDĐT.
Khử sạch hoàn toàn sự lỏng lẻo của dictionary tự do.
"""
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Union

@dataclass
class StatementModel:
    """Mô hình dữ liệu cho từng ý Mệnh đề trong Phần II (Đúng/Sai)."""
    text: str
    is_correct: bool = True
    explanation: Optional[str] = None

    @classmethod
    def from_raw(cls, raw: Any) -> "StatementModel":
        if isinstance(raw, dict):
            t = str(raw.get("t") or raw.get("text") or raw.get("stmt") or "").strip()
            # Xử lý các biến thể lưu trữ đáp án boolean
            ans_val = raw.get("a") if "a" in raw else raw.get("ans", True)
            if isinstance(ans_val, str):
                is_corr = ans_val.strip().lower() in ["đúng", "true", "t", "1"]
            else:
                is_corr = bool(ans_val)
            expl = raw.get("explain") or raw.get("explanation")
            return cls(text=t, is_correct=is_corr, explanation=expl)
        return cls(text=str(raw).strip(), is_correct=True)

@dataclass
class QuestionModel:
    """Mô hình dữ liệu Câu hỏi chuẩn hóa toàn diện (Universal Question Model)."""
    id: str
    q: str
    part: str = "p1"  # "p1", "p2", "p3", "nv_dh", "nv_v"
    opt: List[str] = field(default_factory=list)
    stmts: List[StatementModel] = field(default_factory=list)
    ans: str = ""
    explain: str = ""
    level: str = "TH"  # "NB", "TH", "VD", "VDC"
    topic: str = ""
    source: str = "Bộ GD&ĐT (CT GDPT 2018)"
    f: Optional[Dict[str, Any]] = None
    geom_3d: Optional[Dict[str, Any]] = None
    tikz: Optional[str] = None
    bbt: Optional[Dict[str, Any]] = None
    mslgn_data: Optional[Dict[str, Any]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any], default_part: str = "p1") -> "QuestionModel":
        """Chuyển đổi an toàn từ dictionary bất kỳ sang QuestionModel chuẩn."""
        q_text = str(data.get("q") or data.get("question") or "").strip()
        q_id = str(data.get("id") or data.get("qid") or hash(q_text))
        
        # Chuẩn hóa phương án Phần I
        raw_opts = data.get("opt") or data.get("options") or []
        opts = [str(o).strip() for o in raw_opts] if isinstance(raw_opts, list) else []
        
        # Chuẩn hóa mệnh đề Phần II
        raw_stmts = data.get("stmts") or data.get("statements") or []
        stmts = [StatementModel.from_raw(s) for s in raw_stmts] if isinstance(raw_stmts, list) else []

        # Tự động suy luận phần nếu chưa có
        part = data.get("part", default_part)
        if stmts and not opts:
            part = "p2"
        elif not opts and not stmts and data.get("ans"):
            part = "p3"

        return cls(
            id=q_id,
            q=q_text,
            part=part,
            opt=opts,
            stmts=stmts,
            ans=str(data.get("ans", "")).strip(),
            explain=str(data.get("explain") or data.get("explanation") or "").strip(),
            level=str(data.get("level", "TH")).strip(),
            topic=str(data.get("topic", "")).strip(),
            source=str(data.get("source", "Bộ GD&ĐT")).strip(),
            f=data.get("f"),
            geom_3d=data.get("geom_3d"),
            tikz=data.get("tikz"),
            bbt=data.get("bbt"),
            mslgn_data=data.get("mslgn_data")
        )

    def to_dict(self) -> Dict[str, Any]:
        """Xuất về dạng dictionary chuẩn tương thích ngược 100% với UI Streamlit."""
        res = {
            "id": self.id,
            "q": self.q,
            "part": self.part,
            "opt": self.opt,
            "ans": self.ans,
            "explain": self.explain,
            "level": self.level,
            "topic": self.topic,
            "source": self.source
        }
        if self.stmts:
            res["stmts"] = [{"t": s.text, "a": s.is_correct, "explain": s.explanation} for s in self.stmts]
        if self.f: res["f"] = self.f
        if self.geom_3d: res["geom_3d"] = self.geom_3d
        if self.tikz: res["tikz"] = self.tikz
        if self.bbt: res["bbt"] = self.bbt
        if self.mslgn_data: res["mslgn_data"] = self.mslgn_data
        return res

def normalize_exam_dict(exam: Dict[str, Any]) -> Dict[str, Any]:
    """Adapter chuẩn hóa toàn bộ đề thi về cấu trúc dữ liệu khép kín an toàn."""
    if not isinstance(exam, dict):
        return exam
    normalized = dict(exam)
    for p_key in ["p1", "p2", "p3"]:
        if p_key in normalized and isinstance(normalized[p_key], list):
            normalized[p_key] = [
                QuestionModel.from_dict(q, default_part=p_key).to_dict() 
                for q in normalized[p_key] if isinstance(q, dict)
            ]
    return normalized
