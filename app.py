from flask import Flask, request
from config import EndPoint, LEN_TOKEN
from utils.database.database_worker import DatabaseWorker

app = Flask(__name__)
db = DatabaseWorker()


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route(EndPoint.GET_LEN_TOKEN)
def get_len_token():
    return str(LEN_TOKEN)


@app.route(EndPoint.ATTACH_TOKEN)
def attach_token_to_user():
    telegram_id = request.args.get('telegram_id')
    token = request.args.get('token')
    return db.attach_user_to_token(int(telegram_id), token)


@app.route(EndPoint.BAN_USER)
def ban_user():
    # 1300173322
    telegram_id = request.args.get('telegram_id')
    return db.delete_user_from_tokens(int(telegram_id))


@app.route(EndPoint.GET_ADMINS)
def get_admins():
    return db.get_admins_user()


@app.route(EndPoint.GET_TOKEN)
def get_token():
    amount = request.args.get('amount')
    role = request.args.get('role')
    return db.get_free_tokens_limit(int(amount), role)


@app.route(EndPoint.GET_FREE_TOKEN)
def get_free_token():
    return db.get_all_free_tokens()


@app.route(EndPoint.GET_LOGINS)
def get_logins():
    return db.get_logins_user()


if __name__ == '__main__':
    app.run()
