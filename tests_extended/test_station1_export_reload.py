"""Reproduce Cloud retaining an older imported HTML builder after app update."""
import ast
import re
import unittest
from unittest.mock import patch
from pathlib import Path


class Station1ExportReloadTests(unittest.TestCase):
    topic = 'Hàm 2/1 y=(x^2-2x+2)/(x-1).'
    old_page = '<html><style>.paper{color:black}</style><body class="monochrome"><article id="lesson"><p>KEEP SOURCE</p><table><tr><td>x</td></tr><tr><td>y′</td></tr><tr><td>y</td></tr></table></article></body></html>'

    def namespace(self):
        tree = ast.parse((Path(__file__).resolve().parents[1] / 'app.py').read_text(encoding='utf-8'))
        scope = {'re': re}
        for node in tree.body:
            if isinstance(node, ast.FunctionDef) and node.name in ('_sync_t1_function_export', '_t1_with_function_visuals', '_refresh_t1_context_services'):
                exec(compile(ast.Module(body=[node], type_ignores=[]), 'app-export-helper', 'exec'), scope)
        return tree, scope

    def test_retained_policy_and_source_modules_refresh_in_dependency_order(self):
        from services import curriculum_policy, lesson_sources
        _, scope = self.namespace()
        with patch.object(curriculum_policy, 'T1_CONTEXT_REVISION', 0), patch.object(lesson_sources, 'T1_CONTEXT_REVISION', 0):
            with patch('importlib.reload', wraps=__import__('importlib').reload) as refresh:
                scope['_refresh_t1_context_services']()
                self.assertEqual([call.args[0] for call in refresh.call_args_list], [lesson_sources, curriculum_policy])
                self.assertIn('SGK chỉnh sửa năm 2026', curriculum_policy.policy_prompt('Địa lý', 12, 1))
                scope['_refresh_t1_context_services']()
                self.assertEqual(refresh.call_count, 2)

    def test_cached_approximate_section_is_replaced_once(self):
        _, scope = self.namespace()
        old = self.old_page.replace('<p>KEEP SOURCE</p>', '<p>KEEP SOURCE</p><section class="verified-function-visuals"><svg><text>≈1.414</text></svg></section>')
        result = scope['_sync_t1_function_export'](old, 'Toán học', 'y=x^3-2x.', 'KEEP SOURCE')
        self.assertNotIn('≈1.414', result)
        self.assertEqual(result.count('<section class="verified-function-visuals"'), 1)
        self.assertIn('data-function-renderer="2026110510"', result)
        self.assertIn('KEEP SOURCE', result)

    def test_old_module_is_refreshed_but_current_module_is_not_reloaded(self):
        from services import function_visuals
        _, scope = self.namespace()
        render = scope['_t1_with_function_visuals']
        with patch('importlib.reload', side_effect=AssertionError('current renderer must not reload')):
            self.assertIn('data-function-renderer="2026110510"', render('', 'y=x^3-2x.'))
        with patch.object(function_visuals, 'RENDER_REVISION', 0):
            with patch('importlib.reload', wraps=__import__('importlib').reload) as refresh:
                self.assertIn('data-function-renderer="2026110510"', render('', 'y=x^3-2x.'))
                refresh.assert_called_once_with(function_visuals)

    def test_actual_app_export_assignments_repair_a_cached_old_builder(self):
        tree, scope = self.namespace()
        scope.update(build_lesson_html=lambda *args: self.old_page, subject='Toán học', grade_num=12,
                     current_topic_name=self.topic, cleaned_p1='KEEP SOURCE', export_style='monochrome')
        assignments = [node for node in ast.walk(tree) if isinstance(node, ast.Assign) and
                       any(isinstance(target, ast.Name) and target.id == 'export_html' for target in node.targets)]
        for node in sorted(assignments, key=lambda item: item.lineno):
            exec(compile(ast.Module(body=[node], type_ignores=[]), 'actual-app-export', 'exec'), scope)
        self.assertEqual(scope['export_html'].count('<section class="verified-function-visuals"'), 1)
        self.assertIn('aria-label="Đồ thị y=', scope['export_html'])
        self.assertIn('KEEP SOURCE', scope['export_html'])

    def test_repair_is_idempotent_and_preserves_monochrome(self):
        _, scope = self.namespace()
        repair = scope['_sync_t1_function_export']
        first = repair(self.old_page, 'Toán học', self.topic, 'KEEP SOURCE')
        self.assertEqual(repair(first, 'Toán học', self.topic, 'KEEP SOURCE'), first)
        self.assertIn('.monochrome .verified-function-visuals polyline{stroke:#111}', first)

    def test_other_subjects_and_ambiguous_functions_are_unchanged(self):
        _, scope = self.namespace()
        repair = scope['_sync_t1_function_export']
        self.assertEqual(repair(self.old_page, 'Tin học', self.topic, 'KEEP SOURCE'), self.old_page)
        self.assertEqual(repair(self.old_page, 'Toán học', 'Nhiều hàm', ''), self.old_page)
        self.assertEqual(repair('<p>Missing article</p>', 'Toán học', self.topic, ''), '<p>Missing article</p>')


if __name__ == '__main__':
    unittest.main()
