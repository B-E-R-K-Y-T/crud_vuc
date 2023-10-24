"""Модуль `app.py` представляет собой Flask-приложение, которое использует класс `DatabaseWorker` из модуля `database_worker` для взаимодействия с базой данных.

Функции маршрутизации (`route`) определяют обработчики для различных URL-адресов. Каждый обработчик получает параметры из запроса, выполняет операции с базой данных с помощью экземпляра `db` класса `DatabaseWorker` и возвращает результат в виде строки.

Обработчики маршрутов:

- `main()`: Обработчик для корневого URL-адреса `'/'`. Возвращает строку `'Hello World!'`.

- `get_len_token()`: Обработчик для URL-адреса `'/get-len-token'`. Возвращает длину токена (`LEN_TOKEN`).

- `save_user()`: Обработчик для URL-адреса `'/save-user'`. Получает параметры пользователя из запроса и вызывает метод `save_user()` экземпляра `db` для сохранения информации о пользователе в базе данных. Возвращает строку `'0'`.

- `get_role()`: Обработчик для URL-адреса `'/get-role'`. Получает `telegram_id` из запроса и вызывает метод `get_role_by_telegram_id()` экземпляра `db` для получения роли пользователя по `telegram_id`. Возвращает роль пользователя.

- `get_platoon()`: Обработчик для URL-адреса `'/get-platoon'`. Получает номер взвода (`platoon_number`) из запроса и вызывает метод `get_platoon()` экземпляра `db` для получения информации о студентах взвода с заданным номером. Возвращает информацию о студентах.

- `get_count_platoon_squad()`: Обработчик для URL-адреса `'/get-count-platoon-squad'`. Получает номер взвода (`platoon_number`) из запроса и вызывает метод `get_count_squad_in_platoon()` экземпляра `db` для получения количества отделений во взводе с заданным номером. Возвращает количество отделений.

- `get_platoon_commander()`: Обработчик для URL-адреса `'/get-platoon-commander'`. Получает номер взвода (`platoon_number`) из запроса и вызывает метод `get_platoon_commander()` экземпляра `db` для получения `telegram_id` командира взвода. Возвращает `telegram_id` командира.

- `attach_token_to_user()`: Обработчик для URL-адреса `'/attach-token'`. Получает `telegram_id` и токен (`token`) из запроса и вызывает метод `attach_user_to_token()` экземпляра `db` для привязки пользователя к токену. Возвращает результат операции.

- `ban_user()`: Обработчик для URL-адреса `'/ban-user'`. Получает `telegram_id` из запроса и вызывает метод `ban_user_from_tokens()` экземпляра `db` для блокировки пользователя. Возвращает результат операции.

- `set_squad_of_user()`: Обработчик для URL-адреса `'/set-platoon-squad-of-user'`. Получает номер отделения (`squad_number`) и `telegram_id` из запроса и вызывает метод `set_squad_of_user()` экземпляра `db` для установки номера отделения для пользователя. Возвращает результат операции.

- `get_admins()`: Обработчик для URL-адреса `'/get-admins'`. Вызывает метод `get_admins_user()` экземпляра `db` для получения всех администраторов из базы данных. Возвращает их `telegram_id`.

- `delete_user()`: Обработчик для URL-адреса `'/delete-user'`. Получает `telegram_id` из запроса и вызывает метод `delete_user()` экземпляра `db` для удаления пользователя из базы данных. Возвращает результат операции.

- `get_user()`: Обработчик для URL-адреса `'/get-user'`. Получает `telegram_id` из запроса и вызывает метод `get_user()` экземпляра `db` для получения информации о пользователе. Возвращает информацию о пользователе.

- `attach_user_to_attendance()`: Обработчик для URL-адреса `'/attach-user-attendance'`. Получает `telegram_id` из запроса и вызывает метод `attach_user_to_attendance()` экземпляра `db` для привязки пользователя к таблице посещаемости. Возвращает результат операции.

- `add_visit_user()`: Обработчик для URL-адреса `'/update-attendance-user'`. Получает дату (`date_v`), посещение (`visiting`) и `telegram_id` из запроса и вызывает метод `add_visit_user()` экземпляра `db` для добавления информации о посещении пользователя в таблицу посещаемости. Возвращает результат операции.

- `get_token()`: Обработчик для URL-адреса `'/get-token'`. Получает количество токенов (`amount`) и роль (`role`) из запроса и вызывает метод `get_free_tokens_limit()` экземпляра `db` для получения заданного количества свободных токенов с заданной ролью. Возвращает токены.

- `get_free_token()`: Обработчик для URL-адреса `'/get-free-token'`. Вызывает метод `get_all_free_tokens()` экземпляра `db` для получения всех свободных токенов. Возвращает токены.

- `get_logins()`: Обработчик для URL-адреса `'/get-logins'`. Вызывает метод `get_logins_user()` экземпляра `db` для получения всех `telegram_id_user` из базы данных. Возвращает `telegram_id_user`.

Запуск приложения осуществляется с использованием стандартного шаблона:

```python
if __name__ == '__main__':
    app.run()
```

При запуске приложение будет запущено на локальном сервере и готово к обработке HTTP-запросов.


"""

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


@app.route(EndPoint.GET_PLATOON)
def get_platoon():
    platoon_number = request.args.get('platoon_number')
    return db.get_platoon(int(platoon_number))


@app.route(EndPoint.GET_COUNT_PLATOON_SQUAD)
def get_count_platoon_squad():
    platoon_number = request.args.get('platoon_number')
    return db.get_count_squad_in_platoon(int(platoon_number))


@app.route(EndPoint.GET_PLATOON_COMMANDER)
def get_platoon_commander():
    platoon_number = request.args.get('platoon_number')
    return db.get_platoon_commander(int(platoon_number))


@app.route(EndPoint.ATTACH_TOKEN)
def attach_token_to_user():
    telegram_id = request.args.get('telegram_id')
    token = request.args.get('token')
    return db.attach_user_to_token(int(telegram_id), token)


@app.route(EndPoint.BAN_USER)
def ban_user():
    telegram_id = request.args.get('telegram_id')
    return db.ban_user_from_tokens(int(telegram_id))


@app.route(EndPoint.SET_PLATOON_SQUAD_OF_USER)
def set_squad_of_user():
    squad_number = request.args.get('squad_number')
    telegram_id = request.args.get('telegram_id')
    return db.set_squad_of_user(int(squad_number), int(telegram_id))


@app.route(EndPoint.GET_ADMINS)
def get_admins():
    return db.get_admins_user()


@app.route(EndPoint.DELETE_USER)
def delete_user():
    telegram_id = request.args.get('telegram_id')
    return db.delete_user(int(telegram_id))


@app.route(EndPoint.GET_USER)
def get_user():
    telegram_id = request.args.get('telegram_id')
    return db.get_user(int(telegram_id))


@app.route(EndPoint.ATTACH_USER_ATTENDANCE)
def attach_user_to_attendance():
    telegram_id = request.args.get('telegram_id')
    return db.attach_user_to_attendance(int(telegram_id))


@app.route(EndPoint.UPDATE_ATTENDANCE_USER)
def add_visit_user():
    date_v = request.args.get('date_v')
    visiting = request.args.get('visiting')
    telegram_id = request.args.get('telegram_id')
    return db.add_visit_user(date_v, int(visiting), int(telegram_id))


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
