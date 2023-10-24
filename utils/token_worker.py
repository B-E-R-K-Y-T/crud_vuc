import random
import string

from config import LEN_TOKEN


class TokenWorker:
    def __init__(self):
        self.alphabet = string.ascii_letters + string.digits

    def generate_new_token(self):
        list_password = [random.choice(self.alphabet) for _ in range(LEN_TOKEN)]

        return ''.join(list_password)
