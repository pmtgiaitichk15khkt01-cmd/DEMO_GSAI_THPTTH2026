"""Run with the optional voice runtime (FastAPI is not an app dependency)."""
import concurrent.futures
import importlib.util
import os
from pathlib import Path
import tempfile
import time
import unittest
from unittest.mock import patch

try:
    from fastapi.testclient import TestClient
except ImportError:
    TestClient = None

if TestClient is not None:
    spec = importlib.util.spec_from_file_location(
        "local_voice_server", Path(__file__).parents[1] / "scripts/local_voice_server.py")
    worker = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(worker)


@unittest.skipIf(TestClient is None, "Requires the separate optional voice runtime")
class VoiceWorkerTests(unittest.TestCase):
    def test_reader_voice_text_and_reference_invalidate_cache(self):
        request = worker.SpeechRequest(text="Một bài học.", voice="nam_bo", reader_revision="1")
        key = worker.cache_key(request)
        for change in ({"text": "Bài khác."}, {"voice": "thay_tri"}):
            self.assertNotEqual(key, worker.cache_key(request.model_copy(update=change)))
        self.assertEqual(key, worker.cache_key(request.model_copy(update={"reader_revision": "2"})))
        self.assertNotEqual(worker.cache_key(request, "a"), worker.cache_key(request, "b"))

    def test_concurrent_identical_requests_generate_once(self):
        class Engine:
            calls = 0
            def infer(self, text, **options):
                self.calls += 1
                time.sleep(.05)
                return [1]
            def save(self, audio, path):
                Path(path).write_bytes(b"RIFF-complete-test-audio")
        engine = Engine()
        with tempfile.TemporaryDirectory() as cache, patch.dict(os.environ, GSAI_VOICE_CACHE=cache, GSAI_APPROVED_SOUTHERN_PRESET="reviewed-test-voice"), patch.object(worker, "_engine", engine):
            def send(_):
                with TestClient(worker.app) as client:
                    return client.post("/speech", json={"text": "Bài học", "voice": "nam_bo", "reader_revision": "1"})
            with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
                responses = list(pool.map(send, range(3)))
            self.assertEqual(engine.calls, 1)
            self.assertTrue(all(r.status_code == 200 and r.content == b"RIFF-complete-test-audio" for r in responses))

    def test_failed_generation_never_publishes_partial_file(self):
        class Engine:
            def infer(self, *args, **kwargs):
                return [1]
            def save(self, audio, path):
                Path(path).write_bytes(b"partial")
                raise RuntimeError("failure")
        with tempfile.TemporaryDirectory() as cache, patch.dict(os.environ, GSAI_VOICE_CACHE=cache, GSAI_APPROVED_SOUTHERN_PRESET="reviewed-test-voice"), patch.object(worker, "_engine", Engine()):
            with TestClient(worker.app) as client:
                response = client.post("/speech", json={"text": "Bài học", "voice": "nam_bo", "reader_revision": "1"})
            self.assertEqual(response.status_code, 503)
            self.assertEqual(list(Path(cache).iterdir()), [])

    def test_unreviewed_southern_voice_cannot_reuse_old_audio(self):
        with patch.dict(os.environ, {"GSAI_APPROVED_SOUTHERN_PRESET": ""}):
            with TestClient(worker.app) as client:
                response = client.post("/speech", json={"text": "Bài học", "voice": "nam_bo", "reader_revision": "1"})
                health = client.get("/health").json()
            self.assertEqual(response.status_code, 503)
            self.assertNotIn("nam_bo", health["available_voices"])

    def test_rejected_owner_clone_is_not_available(self):
        with patch.dict(os.environ, {"GSAI_APPROVED_OWNER_VOICE": "", "GSAI_OWNER_VOICE_PREVIEW": ""}):
            with TestClient(worker.app) as client:
                response = client.post("/speech", json={"text": "Bài học", "voice": "thay_tri", "reader_revision": "1"})
                health = client.get("/health").json()
            self.assertEqual(response.status_code, 503)
            self.assertNotIn("thay_tri", health["available_voices"])

    def test_owner_preview_is_distinct_from_final_approval(self):
        with patch.dict(os.environ, {"GSAI_APPROVED_OWNER_VOICE": "", "GSAI_OWNER_VOICE_PREVIEW": "1", "GSAI_THAY_TRI_REFERENCE": "configured-reference"}):
            with TestClient(worker.app) as client:
                health = client.get("/health").json()
            self.assertEqual(health["owner_voice_state"], "preview_B")
            self.assertIn("thay_tri", health["available_voices"])

    def test_owner_preview_uses_configured_reference_and_B_denoise(self):
        class Engine:
            received = None
            def infer(self, text, **options):
                self.received = options
                return [1]
            def save(self, audio, path):
                Path(path).write_bytes(b"complete-preview-test")
        engine = Engine()
        with tempfile.TemporaryDirectory() as folder:
            reference = Path(folder) / "reference-B.wav"
            reference.write_bytes(b"reference-content-for-cache-identity")
            env = {"GSAI_APPROVED_OWNER_VOICE": "", "GSAI_OWNER_VOICE_PREVIEW": "1",
                   "GSAI_THAY_TRI_REFERENCE": str(reference), "GSAI_VOICE_CACHE": str(Path(folder) / "cache")}
            with patch.dict(os.environ, env), patch.object(worker, "_engine", engine):
                with TestClient(worker.app) as client:
                    response = client.post("/speech", json={"text": "Bài học", "voice": "thay_tri", "reader_revision": "20261102.1"})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(engine.received, {"ref_audio": str(reference), "denoise": True})

    def test_identical_legacy_spoken_audio_reused_without_engine(self):
        import hashlib
        import json
        request = worker.SpeechRequest(text="Bài học đã đọc chính xác.", voice="nam_bo", reader_revision="20261102.2")
        digest = "preset:reviewed-test-voice"
        payload = [worker.MODEL_REVISION, "20261102.1", request.voice, request.text, digest]
        old_key = hashlib.sha256(json.dumps(payload, ensure_ascii=False).encode()).hexdigest()
        with tempfile.TemporaryDirectory() as folder:
            (Path(folder) / (old_key + ".wav")).write_bytes(b"complete-legacy-audio")
            with patch.dict(os.environ, GSAI_VOICE_CACHE=folder, GSAI_APPROVED_SOUTHERN_PRESET="reviewed-test-voice"), patch.object(worker, "_engine", None):
                with TestClient(worker.app) as client:
                    response = client.post("/speech", json=request.model_dump())
                self.assertIsNone(worker._engine)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content, b"complete-legacy-audio")


if __name__ == "__main__":
    unittest.main()
