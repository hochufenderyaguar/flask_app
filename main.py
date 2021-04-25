from flask import Flask
from waitress import serve

app = Flask(__name__)


@app.route('/')
def index():
    return 'alkdjfla;kdjf'


if __name__ == '__main__':
    # app.run(port=8080, host='127.0.0.1')
    serve(app, host='127.0.0.1', port=8080)
