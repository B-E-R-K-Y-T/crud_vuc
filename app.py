from flask import Flask, request
from config import EndPoint
from utils.database.database_worker import DatabaseWorker

app = Flask(__name__)
db = DatabaseWorker()


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/')
def attach_token(self, token, telegram_id):
    ...


@app.route(EndPoint.GET_TOKEN)
def get_token():
    amount = request.args.get('amount')
    role = request.args.get('role')
    return db.get_free_tokens(int(amount), role)


if __name__ == '__main__':
    app.run()
