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
    SAVE_USER = '/save_user'
    CHECK_EXIST_USER = '/check_exist_user'
    GET_ROLE = '/get_role'
    DELETE_USER = '/del_user'
    GET_USER = '/get_user'
    GET_PLATOON_COMMANDER = '/get_platoon_commander'
    GET_PLATOON = '/get_platoon'
    GET_COUNT_PLATOON_SQUAD = '/get_count_squad_in_platoon'
    SET_PLATOON_SQUAD_OF_USER = '/set_squad_in_platoon_of_user'
    ATTACH_USER_ATTENDANCE = '/attach_user_to_attendance'
    UPDATE_ATTENDANCE_USER = '/add_visit_user'
