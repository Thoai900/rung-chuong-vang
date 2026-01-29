import mysql.connector

db_config = {
    'user': 'root',
    'password': 'Thoai12345',
    'host': 'localhost',
    'database': 'rung_chuong_vang'
}

def init_db():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Create exam_results table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS exam_results (
        id INT AUTO_INCREMENT PRIMARY KEY,
        student_name VARCHAR(100) NOT NULL,
        class_name VARCHAR(50) NOT NULL,
        score INT NOT NULL,
        total_time INT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    print("Table 'exam_results' created or checked.")

    # Create questions table 
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS questions (
        id INT AUTO_INCREMENT PRIMARY KEY,
        category VARCHAR(50),
        content TEXT NOT NULL,
        options TEXT,
        answer TEXT NOT NULL,
        type VARCHAR(20)
    )
    """)
    print("Table 'questions' created or checked.")
    
    # Clear existing questions to avoid duplicates for this setup
    cursor.execute("TRUNCATE TABLE questions")

    # Sample data
    questions = [
        ('Văn hóa', "Theo chiết tự chữ Hán, ý nghĩa của cụm từ 'Tết Nguyên Đán' là gì?", "A. Đêm trăng tròn đầu tiên; B. Buổi sáng đầu tiên của năm mới; C. Ngày hội sum họp gia đình; D. Lễ hội đón mùa xuân", "B. Buổi sáng đầu tiên của năm mới", "trac_nghiem"),
        ('Ẩm thực', "Món 'Canh khổ qua' trong mâm cỗ Tết miền Nam mang ý nghĩa gì?", "A. Mong mọi sự sung túc; B. Giải nhiệt cơ thể; C. Cầu mong cái khổ đi qua; D. Nhắc nhở sự chịu thương chịu khó", "C. Cầu mong cái khổ đi qua", "trac_nghiem"),
        ('Phong tục', "Miền Nam thường kiêng loại quả nào trong mâm ngũ quả?", "A. Quả Lựu; B. Quả Chuối; C. Quả Xoài; D. Quả Dừa", "B. Quả Chuối", "trac_nghiem"),
        ('Tín ngưỡng', "Tại sao người Việt thường chưng hoa Đào ngày Tết?", "A. Để cầu tình duyên; B. Để xua đuổi tà ma; C. Để thể hiện giàu sang; D. Để báo hiệu mùa xuân", "B. Để xua đuổi tà ma", "trac_nghiem"),
        ('Ẩm thực', "Món 'Thịt kho tàu' với trứng thể hiện triết lý gì?", "A. Tiết kiệm thực phẩm; B. Giao thoa văn hóa phương Tây; C. Hài hòa âm dương, vuông tròn; D. Sự đoàn kết xóm làng", "C. Hài hòa âm dương, vuông tròn", "trac_nghiem"),
        ('Tín ngưỡng', "Ngày 23 tháng Chạp là ngày lễ gì?", "A. Cúng Tất niên; B. Đưa ông Táo về trời; C. Dựng cây Nêu; D. Cúng Giao thừa", "B. Đưa ông Táo về trời", "trac_nghiem"),
        ('Tục ngữ', "Điền vào câu tục ngữ: 'Mùng một Tết cha, mùng hai Tết mẹ, mùng ba...'", "A. Tết bạn; B. Tết thầy; C. Tết vợ; D. Tết con", "B. Tết thầy", "trac_nghiem"),
        ('Kiêng kỵ', "Kiêng kỵ nào thường được thực hiện vào sáng mùng 1 Tết?", "A. Không tắm gội; B. Không quét nhà; C. Không ăn cơm; D. Không ra khỏi nhà", "B. Không quét nhà", "trac_nghiem"),
        ('12 Con Giáp', "Con giáp nào đứng đầu trong 12 con giáp?", "A. Sửu (Trâu); B. Dần (Hổ); C. Thìn (Rồng); D. Tý (Chuột)", "D. Tý (Chuột)", "trac_nghiem"),
        ('Địa lý', "Lễ hội Chùa Hương thuộc tỉnh/thành nào?", "A. Ninh Bình; B. Hà Nội; C. Bắc Ninh; D. Quảng Ninh", "B. Hà Nội", "trac_nghiem")
    ]

    sql = "INSERT INTO questions (category, content, options, answer, type) VALUES (%s, %s, %s, %s, %s)"
    cursor.executemany(sql, questions)
    conn.commit()
    print(f"Inserted {cursor.rowcount} questions.")

    cursor.close()
    conn.close()

if __name__ == '__main__':
    init_db()
