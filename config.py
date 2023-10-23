import os

# Максимальная длина токена(Больше ставить не рекомендуется)
LEN_TOKEN = int(os.getenv('LEN_TOKEN'))


class DatabaseConf:
    DBNAME = 'vuc_database'
    USER = 'postgres'
    PASSWORD = 'admin'
    HOST = '127.0.0.1'


class EndPoint:
    TEST = '/test'
    GET_TOKEN = '/get_token'
    GET_FREE_TOKEN = '/get_free_token'
    GET_LOGINS = '/get_login_users'
    GET_ADMINS = '/get_admins_users'
    LOGIN = '/login'
    ATTACH_TOKEN = '/attach_token'
    BAN_USER = '/ban_user'
    GET_LEN_TOKEN = '/get_len_token'
