from flask import Flask, render_template

app = Flask(__name__)


@app.route('/join') # регистрация
def join():
    pass

@app.route('/login') # вход
def login():
    pass

@app.route('/index') # страничка для пользователей
def index():
    return render_template('index.html')

@app.route('/base')
def base():
    return render_template('base.html')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')