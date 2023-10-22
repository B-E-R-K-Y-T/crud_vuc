import psycopg2


class DatabaseWorker:
    def __init__(self):


        try:
            # пытаемся подключиться к базе данных
            conn = psycopg2.connect(dbname='postgres', user='postgres', password='admin', host='127.0.0.1')
        except:
            # в случае сбоя подключения будет выведено сообщение в STDOUT
            print('Can`t establish connection to database')

        # получение объекта курсора
        cursor = conn.cursor()
        # Получаем список всех пользователей
        cursor.execute('SELECT * FROM test')
        all_users = cursor.fetchall()
        print(all_users)
        cursor.close()  # закрываем курсор
        conn.close()  # закрываем соединение


if __name__ == '__main__':
    dw = DatabaseWorker()


