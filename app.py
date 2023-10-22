from flask import Flask
from config import EndPoint
from utils.database.database_worker import DatabaseWorker

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route(EndPoint.TEST)
def test():  # put application's code here
    dw = DatabaseWorker()
    return dw.test()


if __name__ == '__main__':
    app.run()
