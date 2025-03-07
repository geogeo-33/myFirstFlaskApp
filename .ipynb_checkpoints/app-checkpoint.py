from flask import Flask, request, render_template, session, jsonify
import random
import sqlite3

app = Flask(__name__)
app.secret_key = "supersecretkey"

@app.route('/')
def home():
    session['next_number'] = 1
    nums = random.sample(range(1, 10), 9)

    top_scores = get_top_scores()
    
    return render_template('index.html', nums=nums, top_scores=top_scores)

@app.route('/click', methods=['GET'])
def button_click():
    number = int(request.args.get('number'))
    next_number = session.get('next_number', 1)

    if number == next_number:
        session['next_number'] += 1
        if next_number == 9:
            return '<p>★ゲームクリア★</p><a href="/">もう一度！</a>'
        return f'OK！次は{next_number + 1}を押してね'
    else:
        session['next_number'] = 1
        return '<p>違うよ〜また挑戦してね</p><a href="/">もう一度</a>'

@app.route('/save_time', methods=['POST'])
def save_time():
    data = request.get_json()
    final_time = data.get('final_time')

    if final_time is None:
        return jsonify({'error': 'Invalid time'}), 400

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('INSERT INTO scores (final_time) VALUES (?)', (final_time,))
    conn.commit()
    conn.close()

    
    return jsonify({'message': 'タイムが保存されました！'}), 200

def get_top_scores():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM scores ORDER BY final_time ASC LIMIT 10')
        top_scores = cursor.fetchall()
    return top_scores


if __name__ == '__main__':
    app.run(debug=True)