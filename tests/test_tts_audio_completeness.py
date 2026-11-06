import ast
import concurrent.futures
from pathlib import Path
import re
import unittest
from types import SimpleNamespace
from unittest.mock import Mock

class TTSAudioCompletenessTests(unittest.TestCase):
 def test_long_unpunctuated_paragraph_is_bounded_without_omission(self):
  get=Mock(return_value=SimpleNamespace(status_code=200,content=b'a'*101))
  text=' '.join(['Ngữ liệu khoa học dùng chung mọi môn lớp']*30)
  self.assertTrue(self.load(get)(text))
  sent=[c.kwargs['params']['q'] for c in get.call_args_list]
  self.assertTrue(all(len(c)<=160 for c in sent))
  from collections import Counter
  self.assertEqual(Counter(' '.join(sent).split()),Counter(text.split()))
 def load(self, get):
  tree=ast.parse(Path('app.py').read_text(encoding='utf-8'))
  node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='generate_pedagogical_tts_audio_bytes')
  node.decorator_list=[]
  env={'requests':SimpleNamespace(get=get),'re':re,'concurrent':concurrent}
  exec(compile(ast.Module(body=[node],type_ignores=[]),'actual-tts','exec'),env)
  return env[node.name]
 def test_long_lecture_includes_final_sentence_beyond_18_chunks(self):
  get=Mock(return_value=SimpleNamespace(status_code=200,content=b'a'*101))
  text=' '.join(('Đây là câu thứ '+str(i)+' có nhiều nội dung cần đọc cho học sinh. ')*3 for i in range(35))+' KẾT THÚC BÀI.'
  audio=self.load(get)(text)
  sent=[c.kwargs['params']['q'] for c in get.call_args_list]
  self.assertGreater(len(sent),18)
  self.assertIn('KẾT THÚC BÀI.', ' '.join(sent))
  self.assertEqual(len(audio),101*len(sent))
 def test_partial_network_failure_is_not_successful_partial_lecture(self):
  def get(*a,**kw):
   if 'THẤT BẠI' in kw['params']['q']:raise RuntimeError('offline')
   return SimpleNamespace(status_code=200,content=b'a'*101)
  text='Một đoạn dài. '*20+'THẤT BẠI. '+'Đoạn kết. '*20
  self.assertEqual(self.load(get)(text),b'')
 def test_decimal_and_sentence_punctuation_are_preserved(self):
  get=Mock(return_value=SimpleNamespace(status_code=200,content=b'a'*101))
  self.load(get)('Giá trị là 3.14. Em hãy kiểm tra!')
  sent=' '.join(c.kwargs['params']['q'] for c in get.call_args_list)
  self.assertIn('3.14.',sent)
  self.assertIn('kiểm tra!',sent)
