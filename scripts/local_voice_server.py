"""Optional CPU voice worker. Run with the separate voice runtime, not Streamlit.

Audio, models and the owner's reference remain outside the repository. The
default listener is loopback only; public hosting needs an authenticated proxy.
"""
import hashlib
import json
import os
from pathlib import Path
import shutil
import threading

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field


MODEL_REVISION = "vieneu-3.8.3-v3turbo-fp32"
app = FastAPI(docs_url=None, redoc_url=None)
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.environ.get(
        "GSAI_VOICE_ORIGINS", "http://127.0.0.1:8509,http://127.0.0.1:8506,http://127.0.0.1:8505"
    ).split(","),
    allow_methods=["POST", "GET"], allow_headers=["Content-Type"],
)
_lock = threading.Lock()
_engine = None


class SpeechRequest(BaseModel):
    text: str = Field(min_length=1, max_length=120000)
    voice: str
    reader_revision: str = Field(min_length=1, max_length=100)


def cache_key(request, reference_digest=""):
    # Text is already verbalised. A parser update that leaves this exact text
    # unchanged should not regenerate several minutes of identical narration.
    payload = [MODEL_REVISION, request.voice, request.text, reference_digest]
    return hashlib.sha256(json.dumps(payload, ensure_ascii=False).encode()).hexdigest()


def legacy_audio(cache, request, digest):
    for revision in ("20261025.2", "20261102.1", "manual-reviewed-sample-1"):
        payload = [MODEL_REVISION, revision, request.voice, request.text, digest]
        key = hashlib.sha256(json.dumps(payload, ensure_ascii=False).encode()).hexdigest()
        candidate = cache / (key + ".wav")
        if candidate.is_file():
            return candidate
    return None


def reference_path():
    configured = os.environ.get("GSAI_THAY_TRI_REFERENCE", "")
    if not configured or not Path(configured).is_file():
        raise HTTPException(503, "Giọng Thầy Trí chưa được thiết lập.")
    return Path(configured)


def owner_voice_state():
    if os.environ.get("GSAI_APPROVED_OWNER_VOICE") == "1":
        return "approved"
    if os.environ.get("GSAI_OWNER_VOICE_PREVIEW") == "1":
        return "preview_B"
    return "unavailable"


@app.get("/health")
def health():
    return {"status": "ready" if _engine is not None else "not_loaded",
            "model": MODEL_REVISION,
            "available_voices": (["nam_bo"] if (os.environ.get("GSAI_MALE_PRESET") or os.environ.get("GSAI_APPROVED_SOUTHERN_PRESET")) else [])
            + (["thay_tri"] if os.environ.get("GSAI_THAY_TRI_REFERENCE") and owner_voice_state() != "unavailable" else []),
            "owner_voice_state": owner_voice_state()}


@app.post("/speech")
def speech(request: SpeechRequest):
    global _engine
    if request.voice not in {"nam_bo", "thay_tri"}:
        raise HTTPException(422, "Giọng đọc không được hỗ trợ.")
    if not request.text.strip():
        raise HTTPException(422, "Nội dung đọc đang trống.")
    male_preset = os.environ.get("GSAI_MALE_PRESET") or os.environ.get("GSAI_APPROVED_SOUTHERN_PRESET", "")
    if request.voice == "nam_bo" and not male_preset:
        raise HTTPException(503, "Giọng nam chưa được kết nối.")
    if request.voice == "thay_tri" and owner_voice_state() == "unavailable":
        raise HTTPException(503, "Giọng cá nhân chưa đạt thẩm định; chưa phát dưới tên Thầy Trí.")
    reference = reference_path() if request.voice == "thay_tri" else None
    digest = hashlib.sha256(reference.read_bytes()).hexdigest() if reference else "preset:" + male_preset
    configured = os.environ.get("GSAI_VOICE_CACHE", "")
    if not configured:
        raise HTTPException(503, "Chưa cấu hình nơi lưu âm thanh ngoài dự án.")
    cache = Path(configured)
    cache.mkdir(parents=True, exist_ok=True)
    target = cache / (cache_key(request, digest) + ".wav")
    # One model worker; identical concurrent requests recheck after acquiring
    # the lock. Publish only complete files, never partially generated audio.
    with _lock:
        if not target.is_file():
            old = legacy_audio(cache, request, digest)
            if old:
                temporary = target.with_suffix(".pending.wav")
                try:
                    shutil.copyfile(old, temporary)
                    temporary.replace(target)
                finally:
                    temporary.unlink(missing_ok=True)
        if not target.is_file():
            if _engine is None:
                from vieneu import Vieneu
                _engine = Vieneu(backend="onnx", precision="fp32", babble_retries=0)
            options = {"ref_audio": str(reference), "denoise": True} if reference else {"voice": male_preset}
            temporary = target.with_suffix(".pending.wav")
            try:
                audio = _engine.infer(request.text, **options)
                if len(audio) == 0:
                    raise ValueError("empty audio")
                _engine.save(audio, str(temporary))
                temporary.replace(target)
            except Exception:
                temporary.unlink(missing_ok=True)
                raise HTTPException(503, "Chưa tạo được âm thanh đầy đủ; vui lòng thử lại sau.")
    return FileResponse(target, media_type="audio/wav", headers={"Cache-Control": "private, max-age=86400"})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=int(os.environ.get("GSAI_VOICE_PORT", "8510")))
