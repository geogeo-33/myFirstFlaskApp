from flask import Flask, request, render_template, session
import random

app = Flask(__name__)
app.secret_key = "supersecretkey"

@app.route('/')
def home():
    session['next_number'] = 1
    nums = random.sample(range(1, 10), 9)
    return render_template('index.html', nums=nums)

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
        

if __name__ == '__main__':
    app.run(debug=True)