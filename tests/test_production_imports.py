"""Production imports must remain stable across concurrent student sessions."""
import subprocess
import sys
import unittest
from pathlib import Path


class TestProductionImports(unittest.TestCase):
    root = Path(__file__).resolve().parents[1]

    def run_python(self, source):
        result = subprocess.run([sys.executable, "-c", source], cwd=self.root,
                                capture_output=True, text=True, timeout=45)
        self.assertEqual(result.returncode, 0, result.stderr[-4000:])
        return result.stdout

    def test_production_disables_source_module_eviction(self):
        output = self.run_python('''
from streamlit import config
from streamlit.watcher.path_watcher import get_default_path_watcher_class, NoOpPathWatcher
assert config.get_option("server.fileWatcherType") == "none"
assert config.get_option("server.runOnSave") is False
assert get_default_path_watcher_class() is NoOpPathWatcher
print("watcher disabled")
''')
        self.assertIn("watcher disabled", output)

    def test_concurrent_service_imports_finish_with_valid_context(self):
        output = self.run_python('''
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
barrier = Barrier(8)
def load(_):
    barrier.wait(timeout=15)
    from services.context_recovery import repair_exam_context
    from services.academic_context import academic_context
    from services.curriculum_policy import validate_lesson_policy
    assert callable(repair_exam_context) and callable(validate_lesson_policy)
    return academic_context("Toán", 6)
with ThreadPoolExecutor(max_workers=8) as pool:
    assert list(pool.map(load, range(8))) == [("Toán học", 6)] * 8
print("eight concurrent imports passed")
''')
        self.assertIn("eight concurrent imports passed", output)
