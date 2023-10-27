"""Этот модуль предоставляет класс `DatabaseWorker` для управления базой данных.

Подключение к базе данных осуществляется с использованием модуля `psycopg2`, а также импортируются классы `DatabaseConf` и `TokenWorker` из модулей `config` и `utils.token_worker` соответственно.

Функции-декораторы:

- `_rollback_if_error`: Внутренний декоратор, который автоматически откатывает транзакцию в случае возникновения исключения `psycopg2.Error`. Это обеспечивает надежность выполнения операций с базой данных.

Классы:

- `DatabaseWorker`: Класс, представляющий воркер для работы с базой данных. Он предоставляет методы для выполнения различных операций с таблицами базы данных. Класс имеет следующие методы:

  - `__init__(self)`: Конструктор класса, который устанавливает соединение с базой данных, используя параметры, определенные в классе `DatabaseConf`. В случае ошибки подключения, выводится сообщение об ошибке и соединение закрывается.

  - `get_all_free_tokens(self)`: Получает все свободные токены из таблицы `tokens`, где `telegram_id_user` равно `NULL`. Возвращает строку, содержащую все токены, разделенные символом '&'.

  - `set_squad_of_user(self, squad_number: int, telegram_id: int)`: Устанавливает номер отделения (`squad_number`) для пользователя с заданным `telegram_id` в таблице `students`.

  - `get_count_squad_in_platoon(self, platoon_number: int)`: Получает количество отделений во взводе с заданным номером (`platoon_number`) в таблице `students`. Возвращает строку с количеством отделений.

  - `get_platoon(self, platoon_number: int)`: Получает всех студентов из таблицы `students` с заданным номером взвода (`platoon_number`). Возвращает строку, содержащую информацию о студентах, разделенную символом '%', а каждое поле информации - символом '&'.

  - `get_free_tokens_limit(self, amount: int, role: str)`: Получает заданное количество свободных токенов из таблицы `tokens`, где `telegram_id_user` равно `NULL`, `role` соответствует заданной роли (`role`) и длина токена равна `LEN_TOKEN`. Если доступных токенов недостаточно, генерирует новые токены и добавляет их в таблицу. Возвращает строку, содержащую все токены, разделенные символом '&'.

  - `add_token_to_db(self, token: str, role: str)`: Добавляет новый токен (`token`) с указанной ролью (`role`) в таблицу `tokens`.

  - `attach_user_to_attendance(self, telegram_id: int)`: Добавляет пользователя с заданным `telegram_id` в таблицу `attendance`.

  - `add_visit_user(self, date_v: str, visiting: int, telegram_id: int)`: Добавляет посещение пользователя с заданным `telegram_id` в таблицу `attendance` с указанной датой (`date_v`) и посещением (`visiting`).

  - `get_platoon_commander(self, platoon_number: int)`: Получает `telegram_id` командира взвода с заданным номером (`platoon_number`) из таблицы `students`. Возвращает строку с `telegram_id`.

  - `get_logins_user(self)`: Получает все `telegram_id_user` из таблицы `tokens`, где `telegram_id_user` не равно `NULL` и роль (`role`) не равна 'Admin'. Возвращает строку, содержащую все `telegram_id_user`, разделенные символом '&'.

  - `get_admins_user(self)`: Получает все `telegram_id_user` из таблицы `tokens`, где `telegram_id_user` не равно `NULL` и роль (`role`) равна 'Admin'. Возвращает строку, содержащую все `telegram_id_user`, разделенные символом '&'.

  - `get_user(self, telegram_id: int)`: Получает информацию о пользователе с заданным `telegram_id` из таблицы `students`. Возвращает строку с информаци
"""

import psycopg2

from config import DatabaseConf, LEN_TOKEN
from utils.token_worker import TokenWorker


def _rollback_if_error(func):
    def wrapper(self, *args, **kwargs):
        try:
            res = func(self, *args, **kwargs)
        except psycopg2.Error as _:
            self.conn.rollback()
        else:
            return res

    return wrapper


class DatabaseWorker:
    def __init__(self):
        try:
            # пытаемся подключиться к базе данных
            self.conn = psycopg2.connect(dbname=DatabaseConf.DBNAME, user=DatabaseConf.USER,
                                         password=DatabaseConf.PASSWORD, host=DatabaseConf.HOST)
        except Exception as e:
            # в случае сбоя подключения будет выведено сообщение в STDOUT
            print(f'Can`t establish connection to database: {e}')
            self.conn.close()

    @_rollback_if_error
    def get_all_free_tokens(self):
        with self.conn.cursor() as cur:
            cur.execute('SELECT token FROM tokens WHERE telegram_id_user IS NULL')
            self.conn.commit()

            res = cur.fetchall()

        res = [value[0] for value in res]

        return ''.join(f'{token}&' for token in res)

    @_rollback_if_error
    def set_squad_of_user(self, squad_number: int, telegram_id: int):
        with self.conn.cursor() as cur:
            cur.execute('UPDATE students SET squad_number = %s WHERE telegram_id = %s',
                        [squad_number, telegram_id])
            self.conn.commit()

            return '0'

    @_rollback_if_error
    def get_count_squad_in_platoon(self, platoon_number: int):
        with self.conn.cursor() as cur:
            cur.execute('SELECT sum(1) FROM (SELECT 1 '
                        'FROM students '
                        'WHERE platoon_number = %s AND ARRAY[squad_number] <@ ARRAY[1, 2, 3] '
                        'GROUP BY squad_number) as sub_q; ', [platoon_number])
            self.conn.commit()

            res = cur.fetchall()

            return str(res[0][0])

    @_rollback_if_error
    def get_platoon(self, platoon_number: int):
        with self.conn.cursor() as cur:
            cur.execute('SELECT * FROM students WHERE platoon_number = %s', [platoon_number])
            self.conn.commit()

            res = cur.fetchall()

            seq_users = ''

            for user in res:
                seq_users += '%%'
                for attr in user:
                    seq_users += f'{attr}&'

            return seq_users

    @_rollback_if_error
    def get_free_tokens_limit(self, amount: int, role: str):
        with self.conn.cursor() as cur:
            cur.execute('SELECT token FROM tokens '
                        'WHERE telegram_id_user IS NULL AND role = %s AND length(token) = %s '
                        'LIMIT %s',
                        [role, LEN_TOKEN, amount])
            self.conn.commit()

            res = cur.fetchall()

        res = [value[0] for value in res]

        if not (res and len(res) == amount):
            for _ in range(amount - len(res)):
                token = TokenWorker().generate_new_token()
                res.append(token)
                self.add_token_to_db(token, role)

        return ''.join(f'{token}&' for token in res)

    @_rollback_if_error
    def add_token_to_db(self, token: str, role: str):
        with self.conn.cursor() as cur:
            cur.execute('INSERT INTO tokens (token, role) VALUES(%s, %s)', [token, role])
            self.conn.commit()

    @_rollback_if_error
    def attach_user_to_attendance(self, telegram_id: int):
        with self.conn.cursor() as cur:
            cur.execute('INSERT INTO attendance (telegram_id) VALUES(%s)', [telegram_id])
            self.conn.commit()

            return '0'

    @_rollback_if_error
    def add_visit_user(self, date_v: str, visiting: int, telegram_id: int):
        with self.conn.cursor() as cur:
            cur.execute("SELECT EXISTS(SELECT id FROM attendance where telegram_id = %s AND date_v = %s)",[telegram_id,date_v])
            self.conn.commit()
            res = cur.fetchone()[0]
            if res:
                cur.execute("UPDATE attendance SET date_v = %s, visiting = %s WHERE telegram_id = %s",[date_v,visiting,telegram_id])
            else:
                cur.execute("INSERT INTO attendance(telegram_id,date_v,visiting) values(%s,%s,%s)",[telegram_id,date_v,visiting])
            return '0'

    @_rollback_if_error
    def get_platoon_commander(self, platoon_number: int):
        with self.conn.cursor() as cur:
            cur.execute('SELECT telegram_id FROM students WHERE platoon_number = %s', [platoon_number])
            self.conn.commit()

            res = cur.fetchall()

            if res:
                return str(res[0][0])
            else:
                return ''

    @_rollback_if_error
    def get_logins_user(self):
        with self.conn.cursor() as cur:
            cur.execute('SELECT telegram_id_user FROM tokens WHERE telegram_id_user IS NOT NULL AND role != \'Admin\'')
            self.conn.commit()

            res = cur.fetchall()

            res = [value[0] for value in res]

            return ''.join(f'{token}&' for token in res)

    @_rollback_if_error
    def get_admins_user(self):
        with self.conn.cursor() as cur:
            cur.execute('SELECT telegram_id_user FROM tokens WHERE telegram_id_user IS NOT NULL AND role = \'Admin\'')
            self.conn.commit()

            res = cur.fetchall()

            res = [value[0] for value in res]

            return ''.join(f'{token}&' for token in res)

    @_rollback_if_error
    def get_user(self, telegram_id: int):
        with self.conn.cursor() as cur:
            cur.execute('SELECT '
                        'name, date_of_brith, phone_number, mail, '
                        'address, institute, direction_of_study, group_study, '
                        'course_number, vus, platoon_number, squad_number '
                        'FROM students '
                        'WHERE telegram_id = %s', [telegram_id])
            self.conn.commit()

            res = cur.fetchall()

            if res:
                return ''.join(f'{token}&' for token in res[0])
            else:
                return ''

    @_rollback_if_error
    def attach_user_to_token(self, telegram_id: int, token: str):
        with self.conn.cursor() as cur:
            try:
                cur.execute('UPDATE tokens SET (telegram_id_user, token) = (%s, %s) WHERE token = %s',
                            [telegram_id, token, token])
                self.conn.commit()

                return '0'
            except psycopg2.errors.UniqueViolation as _:
                return '-1'

    @_rollback_if_error
    def delete_user(self, telegram_id: int):
        with self.conn.cursor() as cur:
            cur.execute('DELETE FROM students WHERE telegram_id = %s', [telegram_id])
            cur.execute('DELETE FROM platoon WHERE student_t_id = %s', [telegram_id])
            cur.execute('DELETE FROM tokens WHERE telegram_id_user = %s', [telegram_id])
            cur.execute('DELETE FROM attendance WHERE telegram_id = %s', [telegram_id])
            self.conn.commit()

    @_rollback_if_error
    def ban_user_from_tokens(self, telegram_id: int):
        with self.conn.cursor() as cur:
            try:
                cur.execute('DELETE FROM tokens WHERE telegram_id_user = %s', [telegram_id])
                self.conn.commit()

                return '0'
            except psycopg2.errors.UniqueViolation as _:
                return '-1'

    @_rollback_if_error
    def get_role_by_telegram_id(self, telegram_id):
        with self.conn.cursor() as cur:
            cur.execute('SELECT role FROM tokens WHERE telegram_id_user = %s', [telegram_id])
            self.conn.commit()

            res = cur.fetchall()

            res = [value[0] for value in res]

            return str(res[0])

    @_rollback_if_error
    def save_user(self, *data):
        with self.conn.cursor() as cur:
            cur.execute('SELECT telegram_id FROM students WHERE telegram_id = %s', [data[-2]])
            self.conn.commit()

            res = cur.fetchall()

            if not res:
                self.add_user_id_to_platoon(data[-4], data[-2])

                cur.execute('INSERT INTO students ('
                            'name, date_of_brith, phone_number, mail, '
                            'address, institute, direction_of_study, group_study, '
                            'course_number, vus, platoon_number, squad_number, telegram_id, role) '
                            'VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', data)
            else:
                cur.execute('UPDATE students SET ('
                            'name, date_of_brith, phone_number, mail, '
                            'address, institute, direction_of_study, group_study, '
                            'course_number, vus, platoon_number, squad_number, telegram_id, role) ='
                            '(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) WHERE telegram_id = %s',
                            [*data, data[-2]])

            self.conn.commit()

    @_rollback_if_error
    def add_user_id_to_platoon(self, platoon_number: int, telegram_id: int):
        with self.conn.cursor() as cur:
            cur.execute('INSERT INTO platoon (student_t_id, platoon_number) VALUES (%s, %s)',
                        [telegram_id, platoon_number])
            self.conn.commit()

    def __del__(self):
        self.conn.close()


if __name__ == '__main__':
    dw = DatabaseWorker()

    print(dw.get_free_tokens_limit(1, 'Командир отделения'))
    print(dw.get_logins_user())
    print(dw.attach_user_to_token(12323, '3onJJtt8ItapyTkbU75le8u4l'))
