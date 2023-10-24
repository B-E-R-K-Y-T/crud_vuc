import random
import string

from config import LEN_TOKEN


class TokenWorker:
    def __init__(self):
        ...

    @staticmethod
    def generate_new_token():
        alphabet = string.ascii_letters + string.digits
        list_password = [random.choice(alphabet) for _ in range(LEN_TOKEN)]

        return ''.join(list_password)
