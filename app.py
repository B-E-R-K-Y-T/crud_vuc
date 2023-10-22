from flask import Flask
from config import EndPoint

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route(EndPoint.TEST)
def test():  # put application's code here
    return 'TEST'


if __name__ == '__main__':
    app.run()
