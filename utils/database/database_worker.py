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

    def get_free_tokens(self, amount: int, role: str):
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
            cur.execute('SELECT telegram_id_user FROM tokens WHERE telegram_id_user IS NOT NULL')
            self.conn.commit()

            res = cur.fetchall()

        res = [value[0] for value in res]

        return ''.join(f'{token}&' for token in res)

    def attach_user_to_token(self, telegram_id: int, token: str):
        with self.conn.cursor() as cur:
            cur.execute('UPDATE tokens SET (telegram_id_user, token) = (%s, %s) WHERE token = %s',
                        [telegram_id, token, token])
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

    print(dw.get_free_tokens(1, 'Командир отделения'))
    print(dw.get_logins_user(), 123)
    dw.attach_user_to_token(123, ';ва')

