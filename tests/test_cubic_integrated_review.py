import unittest
from services.curriculum_policy import repair_reviewed_cubic_question, correct_reviewed_cubic_prior_knowledge

class ReviewTests(unittest.TestCase):
    def test_duplicate_distractor_repaired_without_shuffling(self):
        q={"question":"Cho hàm số $y=x^3-3x+1$. Giá trị cực đại là:","options":["A. $3$","B. $-1$","C. $-1$","D. $1$"],"correct":"A","hint":"Xét dấu đạo hàm."}
        r=repair_reviewed_cubic_question(q,"Toán học",12)
        self.assertEqual(r["options"],["A. $3$","B. $-1$","C. $0$","D. $1$"])
        self.assertEqual(r["correct"],"A")
        self.assertEqual(r["hint"],q["hint"])
        self.assertEqual(repair_reviewed_cubic_question(r,"Toán học",12),r)
        self.assertEqual(q["options"][2],"C. $-1$")
        self.assertEqual(repair_reviewed_cubic_question(q,"Toán học",11),q)
        other=dict(q,question=q["question"].replace("-3x","-6x"))
        self.assertEqual(repair_reviewed_cubic_question(other,"Toán học",12),other)
    def test_grade_placement_is_scoped(self):
        text="Nhớ lại cách tính đạo hàm và tìm cực trị của hàm số đã học ở lớp 11."
        fixed=correct_reviewed_cubic_prior_knowledge(text,"Toán học",12,"Khảo sát hàm số bậc ba")
        self.assertIn("kiến thức lớp 12",fixed)
        self.assertEqual(correct_reviewed_cubic_prior_knowledge(text,"Ngữ văn",12,"bậc ba"),text)
    def test_three_root_key_recovered_only_for_exact_reviewed_function(self):
        q={"question":"Phương trình $x^3-3x+1=m$ có ba nghiệm phân biệt khi:","options":["A. $-1<m<3$","B. $m>3$","C. $m<-1$","D. $-1<=m<=3$"],"correct":""}
        self.assertEqual(repair_reviewed_cubic_question(q,"Toán học",12)["correct"],"A")
        other=dict(q,question=q["question"].replace("-3x","-6x"))
        self.assertEqual(repair_reviewed_cubic_question(other,"Toán học",12)["correct"],"")
    def test_increasing_intervals_key_recovered_from_exact_option(self):
        q={"question":"Hàm số $y=x^3-3x+1$ đồng biến trên khoảng nào dưới đây?","options":["A. $(-1;1)$","B. $(-\\infty;1)$","C. $(-\\infty;-1)$ và $(1;+\\infty)$","D. $(-1;+\\infty)$"],"correct":""}
        r=repair_reviewed_cubic_question(q,"Toán học",12)
        self.assertEqual(r["correct"],"C")
        self.assertIn("các khoảng",r["question"])

if __name__=="__main__": unittest.main()
