import importlib.util
import json
import lzma
from pathlib import Path
import tempfile
import unittest
from dedupe_bank import q_fingerprint, run
from contextlib import redirect_stdout
import io

spec = importlib.util.spec_from_file_location('corpus_audit', Path('scripts/audit_exam_corpus.py'))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class CorpusAuditTests(unittest.TestCase):
    def test_production_pack_roundtrip_near_conflicts_passages_and_provenance(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            def exam(code, text, answer='A', passage='Văn bản 1'):
                return {'code': code, 'subject': 'Ngữ văn', 'grade': 9, 'url': 'https://example.org/' + code,
                    'part_doc_hieu': {'passage': passage, 'questions': [{'q': text, 'ans': answer}]}}
            exams = [exam('1', 'Chi tiết này đúng'), exam('2', 'Chi tiết này đúng'),
                     exam('3', 'Chi tiết này không đúng'), exam('4', 'Chi tiết này đúng', 'B'),
                     exam('5', 'Chi tiết này đúng', passage='Văn bản 2')]
            path = root / 'input.json.xz'
            with lzma.open(path, 'wt', encoding='utf-8') as stream:
                json.dump({'exams': exams}, stream)
            original = path.read_bytes()
            with redirect_stdout(io.StringIO()):
                bank = run(str(path), str(root / 'output'))
            self.assertEqual(bank['total'], 4)
            with lzma.open(root / 'output/unique_questions.json.xz', 'rt', encoding='utf-8') as stream:
                self.assertEqual(json.load(stream), bank)
            pool = bank['questions']['Ngữ văn']['9']
            duplicate = next(q for q in pool if q['dup_count'] == 2)
            self.assertEqual({p['exam_code'] for p in duplicate['provenance_occurrences']}, {'1', '2'})
            self.assertEqual(duplicate['shared_context']['part_context']['passage'], 'Văn bản 1')
            self.assertEqual(path.read_bytes(), original)

    def test_distinct_science_code_answers_and_passages_are_not_deleted(self):
        base = {'subject': 'Toán học', 'grade': 10, 'part': 'p1', 'shared': {}}
        for left, right in [('x^2', 'x2'), ('(a+b)*c', 'a+b*c'),
                            ('if x:\n  print(x)', 'if x:\nprint(x)'), ('Co', 'CO')]:
            self.assertNotEqual(module.fingerprint({'q': left}, base), module.fingerprint({'q': right}, base))
            self.assertNotEqual(q_fingerprint({'q': left}), q_fingerprint({'q': right}))
        self.assertNotEqual(q_fingerprint({'q': 'q', 'ans': 'A'}), q_fingerprint({'q': 'q', 'ans': 'B'}))
        self.assertNotEqual(module.fingerprint({'q': 'q', 'ans': 'A'}, base), module.fingerprint({'q': 'q', 'ans': 'B'}, base))
        other = dict(base, shared={'text': 'Ngữ liệu khác'})
        self.assertNotEqual(module.fingerprint({'q': 'q'}, base), module.fingerprint({'q': 'q'}, other))

    def test_provenance_duplicates_reported_without_mutating_original_xz(self):
        with tempfile.TemporaryDirectory() as directory:
            p = Path(directory) / 'bank.json.xz'
            exams = [{'code': str(i), 'subject': 'Toán học', 'grade': 10,
                      'p1': [{'q': 'x^2', 'ans': 'A', 'source': str(i)}]} for i in range(2)]
            with lzma.open(p, 'wt', encoding='utf-8') as stream:
                json.dump({'exams': exams}, stream)
            original = p.read_bytes()
            report = module.audit([p], Path(directory) / 'audit.json')
            self.assertEqual(report['totals']['unique_exact'], 1)
            self.assertEqual(report['totals']['duplicate_exact_occurrences'], 1)
            self.assertEqual(p.read_bytes(), original)
