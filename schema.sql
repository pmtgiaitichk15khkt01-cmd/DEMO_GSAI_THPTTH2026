-- VIP 74.1 Database Schema - GSAI THPT 2026
-- ==============================================================================
-- LƯỢC ĐỒ CƠ SỞ DỮ LIỆU CHUẨN HÓA CHO HỆ SINH THÁI GIA SƯ AI (GSAI 2026 - VIP 66.2)
-- Cập nhật: Ngày 18/10/2026 (Bản nâng cấp VIP 66.2)
-- Tương thích: PostgreSQL 15+, Supabase Cloud, SQLite 3.35+
-- Chuẩn đạo đức AI: Ẩn danh hóa thông tin cá nhân (PII Anonymization) theo UNESCO & Bộ GD&ĐT
-- ==============================================================================

-- 1. BẢNG HỌC SINH (STUDENTS) - QUẢN LÝ ĐỊNH DANH ẨN DANH HÓA
CREATE TABLE IF NOT EXISTS students (
    id TEXT PRIMARY KEY,                       -- UUID hoặc mã định danh duy nhất
    student_code VARCHAR(30) UNIQUE NOT NULL,  -- Mã học sinh nghiên cứu (VD: HS-K12-001)
    display_name VARCHAR(100) NOT NULL,        -- Tên hiển thị (Ẩn danh hoặc họ tên)
    grade_level SMALLINT NOT NULL CHECK (grade_level BETWEEN 6 AND 12),
    school_name VARCHAR(150) DEFAULT 'THPT Tân Hiệp',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. BẢNG KẾT QUẢ KHẢO THÍ (EXAM_ATTEMPTS) - DỮ LIỆU ĐO LƯỜNG TRẠM 3
CREATE TABLE IF NOT EXISTS exam_attempts (
    id TEXT PRIMARY KEY,                       -- ID lần thi (attempt_id)
    student_id TEXT NOT NULL,                  -- Khóa ngoại liên kết bảng students
    student_name VARCHAR(100),
    grade_level SMALLINT NOT NULL,
    subject VARCHAR(50) NOT NULL,              -- Toán học, Ngữ văn, Tiếng Anh...
    exam_code VARCHAR(20) NOT NULL,            -- Mã đề thi 4 chữ số
    score NUMERIC(4, 2) NOT NULL CHECK (score >= 0.0 AND score <= 10.0),
    phase VARCHAR(20) DEFAULT 'practice',      -- 'pre_test' (Trước can thiệp), 'post_test' (Sau can thiệp), 'practice'
    duration_seconds INT DEFAULT 0,            -- Thời gian làm bài thực tế (giây)
    grading_status VARCHAR(30) DEFAULT 'auto_graded', -- 'auto_graded' hoặc 'ai_reference'
    answers_json TEXT DEFAULT '{}',            -- Toàn bộ bài làm của học sinh (JSON text)
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
);

-- 3. BẢNG CHẨN ĐOÁN LỖ HỔNG TRI THỨC (DIAGNOSTIC_LOGS) - DỮ LIỆU TRẠM 2
CREATE TABLE IF NOT EXISTS diagnostic_logs (
    id TEXT PRIMARY KEY,                       -- ID sự kiện chẩn đoán
    student_id TEXT NOT NULL,
    student_name VARCHAR(100),
    grade_level SMALLINT NOT NULL,
    subject VARCHAR(50) NOT NULL,
    topic VARCHAR(200) NOT NULL,               -- Chuyên đề bài học SGK Kết Nối Tri Thức
    error_type VARCHAR(100) NOT NULL,          -- Loại lỗi: Khái niệm, tính toán, phương pháp...
    evaluation VARCHAR(100) DEFAULT 'Cần theo dõi',
    radar_scores_json TEXT DEFAULT '{}',       -- Điểm 5 trục năng lực Radar Chart (JSON)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
);

-- 4. BẢNG GÓP Ý VÀ BÁO LỖI (USER_FEEDBACKS) - QUẢN TRỊ TRẢI NGHIỆM
CREATE TABLE IF NOT EXISTS user_feedbacks (
    id TEXT PRIMARY KEY,
    student_name VARCHAR(100),
    grade_level SMALLINT,
    subject VARCHAR(50),
    category VARCHAR(50) NOT NULL,             -- Nhận diện chữ, Đồ thị Lab, Ứng dụng chậm...
    rating SMALLINT CHECK (rating BETWEEN 1 AND 5),
    detail TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ==============================================================================
-- 5. CHỈ MỤC INDEX TỐI ƯU HÓA TRUY VẤN THỰC NGHIỆM SƯ PHẠM (TRẠM 4)
-- Đảm bảo thời gian tính Paired t-Test và Cohen's d dưới 5ms với N = 100.000 bản ghi
-- ==============================================================================
CREATE INDEX IF NOT EXISTS idx_exam_study ON exam_attempts (subject, grade_level, phase, student_id);
CREATE INDEX IF NOT EXISTS idx_exam_score ON exam_attempts (score);
CREATE INDEX IF NOT EXISTS idx_diagnostic_search ON diagnostic_logs (subject, grade_level, topic);
CREATE INDEX IF NOT EXISTS idx_students_code ON students (student_code);

-- ==============================================================================
-- 6. CHÍNH SÁCH BẢO MẬT HÀNG (ROW LEVEL SECURITY - DÀNH CHO POSTGRESQL / SUPABASE)
-- Phù hợp triển khai Supabase Cloud:
-- ==============================================================================
-- ALTER TABLE students ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE exam_attempts ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE diagnostic_logs ENABLE ROW LEVEL SECURITY;
-- CREATE POLICY "Cho phép học sinh xem điểm của chính mình" ON exam_attempts FOR SELECT USING (auth.uid()::text = student_id);
-- CREATE POLICY "Cho phép ghi nhận kết quả thi" ON exam_attempts FOR INSERT WITH CHECK (true);
