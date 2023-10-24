import random
import string
import psycopg2

from config import DatabaseConf, LEN_TOKEN


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

    def get_all_free_tokens(self):
        with self.conn.cursor() as cur:
            cur.execute('SELECT token FROM tokens WHERE telegram_id_user IS NULL')
            self.conn.commit()

            res = cur.fetchall()

        res = [value[0] for value in res]

        return ''.join(f'{token}&' for token in res)

    def get_free_tokens_limit(self, amount: int, role: str):
        with self.conn.cursor() as cur:
            cur.execute('SELECT token FROM tokens WHERE telegram_id_user IS NULL AND role = %s LIMIT %s',
                        [role, amount])
            self.conn.commit()

            res = cur.fetchall()

        res = [value[0] for value in res]

        if not (res and len(res) == amount):
            for _ in range(amount - len(res)):
                token = self.__generate_new_token()
                res.append(token)
                self.add_token_to_db(token, role)

        return ''.join(f'{token}&' for token in res)

    def add_token_to_db(self, token: str, role: str):
        with self.conn.cursor() as cur:
            cur.execute('INSERT INTO tokens (token, role) VALUES(%s, %s)', [token, role])
            self.conn.commit()

    def get_logins_user(self):
        with self.conn.cursor() as cur:
            cur.execute('SELECT telegram_id_user FROM tokens WHERE telegram_id_user IS NOT NULL AND role != \'Admin\'')
            self.conn.commit()

            res = cur.fetchall()

            res = [value[0] for value in res]

            return ''.join(f'{token}&' for token in res)

    def get_admins_user(self):
        with self.conn.cursor() as cur:
            cur.execute('SELECT telegram_id_user FROM tokens WHERE telegram_id_user IS NOT NULL AND role = \'Admin\'')
            self.conn.commit()

            res = cur.fetchall()

            res = [value[0] for value in res]

            return ''.join(f'{token}&' for token in res)

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

            return ''.join(f'{token}&' for token in res[0])

    def attach_user_to_token(self, telegram_id: int, token: str):
        with self.conn.cursor() as cur:
            try:
                cur.execute('UPDATE tokens SET (telegram_id_user, token) = (%s, %s) WHERE token = %s',
                            [telegram_id, token, token])
                self.conn.commit()

                return '0'
            except psycopg2.errors.UniqueViolation as _:
                return '-1'

    def delete_user(self, telegram_id: int):
        with self.conn.cursor() as cur:
            cur.execute('DELETE FROM students WHERE telegram_id = %s', [telegram_id])
            cur.execute('DELETE FROM platoon WHERE student_t_id = %s', [telegram_id])
            cur.execute('DELETE FROM tokens WHERE telegram_id_user = %s', [telegram_id])
            self.conn.commit()

    def ban_user_from_tokens(self, telegram_id: int):
        with self.conn.cursor() as cur:
            try:
                cur.execute('DELETE FROM tokens WHERE telegram_id_user = %s', [telegram_id])
                self.conn.commit()

                return '0'
            except psycopg2.errors.UniqueViolation as _:
                return '-1'

    def get_role_by_telegram_id(self, telegram_id):
        with self.conn.cursor() as cur:
            cur.execute('SELECT role FROM tokens WHERE telegram_id_user = %s', [telegram_id])
            self.conn.commit()

            res = cur.fetchall()

            res = [value[0] for value in res]

            return str(res[0])

    def save_user(self, *data):
        with self.conn.cursor() as cur:
            self.add_user_id_to_platoon(data[-4], data[-2])

            cur.execute('INSERT INTO students ('
                        'name, date_of_brith, phone_number, mail, '
                        'address, institute, direction_of_study, group_study, '
                        'course_number, vus, platoon_number, squad_number, telegram_id, role) '
                        'VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', data)
            self.conn.commit()

    def add_user_id_to_platoon(self, platoon_number: int, telegram_id: int):
        with self.conn.cursor() as cur:
            cur.execute('INSERT INTO platoon (student_t_id, platoon_number) VALUES (%s, %s)',
                        [telegram_id, platoon_number])
            self.conn.commit()

    @staticmethod
    def __generate_new_token():
        alphabet = string.ascii_letters + string.digits
        list_password = [random.choice(alphabet) for _ in range(LEN_TOKEN)]

        return ''.join(list_password)

    def __del__(self):
        self.conn.close()


if __name__ == '__main__':
    dw = DatabaseWorker()

    print(dw.get_free_tokens_limit(1, 'Командир отделения'))
    print(dw.get_logins_user())
    print(dw.attach_user_to_token(12323, '3onJJtt8ItapyTkbU75le8u4l'))
