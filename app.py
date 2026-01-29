from flask import Flask, render_template, request, jsonify, session
import mysql.connector
import random

app = Flask(__name__)
app.secret_key = 'rung_chuong_vang_secret_key' # Needed for session

# Cấu hình kết nối MySQL
db_config = {
    'user': 'root',
    'password': 'Thoai12345',
    'host': 'localhost',
    'database': 'rung_chuong_vang'
}

def get_db_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/quiz')
def quiz():
    return render_template('quiz.html')

@app.route('/leaderboard')
def leaderboard_page():
    return render_template('leaderboard.html')

# --- API Endpoints ---

@app.route('/api/questions', methods=['GET'])
def get_questions():
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    cursor = conn.cursor(dictionary=True)
    # Get all questions or limit them. For now, get 20 random questions.
    query = "SELECT * FROM questions ORDER BY RAND() LIMIT 20"
    cursor.execute(query)
    questions = cursor.fetchall()
    
    # Process options if stored as string "A. ...; B. ..."
    # Assuming the options in DB are stored as a single string like "A. Val; B. Val"
    # or just returning them as is for frontend to parse. 
    # Based on init_db.py, they are strings like "A. ...; B. ..."
    
    cursor.close()
    conn.close()
    return jsonify(questions)

@app.route('/api/submit', methods=['POST'])
def submit_result():
    data = request.json
    name = data.get('name')
    group = data.get('group') # Lớp
    score = data.get('score')
    time_spent = data.get('time_spent')
    
    if not name or not group:
         return jsonify({'error': 'Missing name or class'}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
        
    cursor = conn.cursor()
    query = "INSERT INTO exam_results (student_name, class_name, score, total_time) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (name, group, score, time_spent))
    conn.commit()
    
    cursor.close()
    conn.close()
    return jsonify({'message': 'Result saved successfully'})

@app.route('/api/leaderboard', methods=['GET'])
def get_leaderboard():
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
        
    cursor = conn.cursor(dictionary=True)
    # Order by Score DESC, then Time ASC
    query = "SELECT student_name, class_name, score, total_time, created_at FROM exam_results ORDER BY score DESC, total_time ASC LIMIT 10"
    cursor.execute(query)
    results = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
