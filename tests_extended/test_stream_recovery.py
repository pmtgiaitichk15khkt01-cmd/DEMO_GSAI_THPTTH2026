"""A broken stream must not append a new, duplicated model answer."""
import ast
import time
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock


class TestStreamRecovery(unittest.TestCase):
    def test_partial_answer_stops_without_restarting(self):
        source = Path(__file__).resolve().parents[1].joinpath("app.py").read_text(encoding="utf-8")
        tree = ast.parse(source)
        function = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "stream_gemini_with_fallback")
        state = SimpleNamespace(get=lambda key: None)

        def broken_stream(**kwargs):
            yield SimpleNamespace(text="Phần trả lời đã nhận")
            raise ConnectionError("connection lost")

        client = Mock()
        client.__enter__ = Mock(return_value=client)
        client.__exit__ = Mock(return_value=False)
        client.models.generate_content_stream.side_effect = broken_stream
        fallback = Mock(return_value="duplicate answer")
        namespace = {"get_active_model_queue": lambda: ["gemini-2-test"],
                     "active_keys_pool": ["test-only"], "st": SimpleNamespace(session_state=state),
                     "time": time, "DEFAULT_PEDAGOGICAL_SYSTEM_INSTRUCTION": "test",
                     "types": SimpleNamespace(GenerateContentConfig=lambda **kwargs: SimpleNamespace(**kwargs),
                                              HttpOptions=lambda **kwargs: kwargs),
                     "genai": SimpleNamespace(Client=Mock(return_value=client)),
                     "call_gemini_with_fallback": fallback}
        exec(compile(ast.Module(body=[function], type_ignores=[]), "stream-test", "exec"), namespace)
        stream = namespace[function.name]("test")
        self.assertEqual(next(stream), "Phần trả lời đã nhận")
        with self.assertRaisesRegex(RuntimeError, "gián đoạn"):
            next(stream)
        fallback.assert_not_called()
