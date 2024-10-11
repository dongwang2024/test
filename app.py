
from flask import Flask, render_template, request, redirect, url_for ,session,flash

import random  

    

app = Flask(__name__)  

    

# 生成一个1到100之间的随机数，并保存在会话中  

@app.before_request  

def setup():  

    if not 'target_number' in session:  

        session['target_number'] = random.randint(1, 100)  

    if not 'attempts' in session:  

        session['attempts'] = 6  

    if not 'guesses' in session:  

        session['guesses'] = []  

    

# 设置会话密钥，以便Flask可以记住用户的数据  

app.secret_key = '123'  # 请替换为你的密钥  

    

@app.route('/')  

def index():  

    attempts = session['attempts']  

    guesses = session['guesses']  

    return render_template('index.html', attempts=attempts, guesses=guesses)  

    

@app.route('/guess', methods=['POST'])  

def guess():  

    guess = request.form['guess']  

    

    # 检查输入是否为数字  

    if not guess.isdigit():  

        flash('请输入一个有效的数字！', 'error')  

        return redirect(url_for('index'))  

    

    guess = int(guess)  

    target_number = session['target_number']  

    attempts = session['attempts']  

    guesses = session['guesses']  

    

    guesses.append(guess)  

    session['guesses'] = guesses  

    

    if guess < target_number:  

        flash('小了！', 'info')  

    elif guess > target_number:  

        flash('大了！', 'info')  

    else:  

        flash(f'恭喜你，猜中了！数字是 {target_number}。', 'success')  

        session.pop('target_number', None)  # 重置游戏  

        session.pop('attempts', None)  

        session.pop('guesses', None)  

        return redirect(url_for('index'))  # 重定向到主页以开始新游戏  

    

    # 减少尝试次数  

    attempts -= 1  

    if attempts <= 0:  

        flash(f'很遗憾，你用完了所有的机会。数字是 {target_number}。', 'danger')  

        session.pop('target_number', None)  # 重置游戏  

        session.pop('attempts', None)  

        session.pop('guesses', None)  

    else:  

        session['attempts'] = attempts  

    

    return redirect(url_for('index'))  

    

if __name__ == '__main__':  

    app.run(debug=True)