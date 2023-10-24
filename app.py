from flask import Flask, request
from config import EndPoint, LEN_TOKEN
from utils.database.database_worker import DatabaseWorker

app = Flask(__name__)
db = DatabaseWorker()


@app.route('/')
def main():
    return 'Hello World!'


@app.route(EndPoint.GET_LEN_TOKEN)
def get_len_token():
    return str(LEN_TOKEN)


@app.route(EndPoint.SAVE_USER)
def save_user():
    name = request.args.get('name')
    date_of_brith = request.args.get('date_of_brith')
    phone_number = request.args.get('phone_number')
    mail = request.args.get('mail')
    address = request.args.get('address')
    institute = request.args.get('institute')
    direction_of_study = request.args.get('direction_of_study')
    group_study = request.args.get('group_study')
    course_number = request.args.get('course_number')
    vus = request.args.get('vus')
    platoon = request.args.get('platoon')
    squad = request.args.get('squad')
    telegram_id = request.args.get('telegram_id')
    role = request.args.get('role')

    db.save_user(
        name, date_of_brith, phone_number, mail,
        address, institute, direction_of_study, group_study,
        course_number, vus, platoon, squad, telegram_id, role
    )

    return '0'


@app.route(EndPoint.GET_ROLE)
def get_role():
    telegram_id = request.args.get('telegram_id')
    return db.get_role_by_telegram_id(int(telegram_id))


@app.route(EndPoint.ATTACH_TOKEN)
def attach_token_to_user():
    telegram_id = request.args.get('telegram_id')
    token = request.args.get('token')
    return db.attach_user_to_token(int(telegram_id), token)


@app.route(EndPoint.BAN_USER)
def ban_user():
    telegram_id = request.args.get('telegram_id')
    return db.ban_user_from_tokens(int(telegram_id))


@app.route(EndPoint.GET_USER)
def get_user():
    telegram_id = request.args.get('telegram_id')
    return db.get_user(int(telegram_id))


@app.route(EndPoint.GET_ADMINS)
def get_admins():
    return db.get_admins_user()


@app.route(EndPoint.DELETE_USER)
def delete_user():
    telegram_id = request.args.get('telegram_id')
    return db.delete_user(int(telegram_id))


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
