import os

from flask import Flask
from waitress import serve

app = Flask(__name__)


@app.route('/')
def index():
    return 'alkdjfla;kdjf'


if __name__ == '__main__':
    # app.run(port=8080, host='127.0.0.1')
    # serve(app, host='0.0.0.0', port=5000)
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
