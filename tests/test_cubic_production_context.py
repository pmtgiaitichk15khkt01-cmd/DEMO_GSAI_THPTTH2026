import unittest
from services.curriculum_policy import correct_reviewed_cubic_production_context as repair

class CubicProductionContextTests(unittest.TestCase):
 def test_observed_profit_task_has_nonnegative_model_and_no_invented_units(self):
  src=r"Hàm lợi nhuận $L(x)=-x^3+9x^2+21x$ (với $x$ là đơn vị sản lượng). Hãy tìm mức sản lượng."
  fixed=repair(src,'Toán học',12,'Tính đơn điệu và cực trị hàm số bậc ba Toán12 KNTT')
  self.assertIn('giả sử xét sản lượng không âm trong mô hình liên tục',fixed)
  self.assertIn('chưa quy định đơn vị',fixed)
  self.assertIn(r'$L(x)=-x^3+9x^2+21x$',fixed)
  self.assertEqual(repair(fixed,'Toán học',12,'Hàm số bậc ba'),fixed)
  for subject,grade,topic in [('Toán học',11,'Hàm số bậc ba'),('Vật lý',12,'Hàm số bậc ba'),('Toán học',12,'Hàm số bậc hai')]:
   self.assertEqual(repair(src,subject,grade,topic),src)
 def test_code_and_math_are_preserved(self):
  src='lợi nhuận\n```text\nlà đơn vị sản lượng\n```\n$là đơn vị sản lượng$'
  self.assertEqual(repair(src,'Toán học',12,'Hàm số bậc ba'),src)
