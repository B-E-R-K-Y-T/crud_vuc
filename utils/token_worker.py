"""Модуль `token_worker.py` содержит класс `TokenWorker`, который предоставляет функциональность для генерации новых токенов.

Класс `TokenWorker` имеет следующие методы:

- `__init__()`: Конструктор класса, инициализирует атрибут `alphabet` с набором символов, используемых для генерации токенов. Набор символов включает буквы верхнего и нижнего регистра, а также цифры.

- `generate_new_token()`: Метод, который генерирует новый токен. Он создает случайную последовательность символов из алфавита, указанного в атрибуте `alphabet`, длиной `LEN_TOKEN` (которая импортируется из модуля `config`). Возвращает сгенерированный токен в виде строки.

Пример использования модуля:

```python
from token_worker import TokenWorker

# Создание экземпляра класса TokenWorker
tokens = TokenWorker()

# Генерация нового токена
new_token = tokens.generate_new_token()

# Вывод нового токена
print(new_token)
```

При запуске модуль `token_worker.py` в качестве самостоятельного скрипта (если `__name__` равно `'__main__'`), будет сгенерирован и выведен новый токен.

Обратите внимание, что генерируемые токены могут использоваться для различных целей, таких как аутентификация пользователей, создание временных ключей доступа и т. д. Токены представляют собой случайные и уникальные последовательности символов, которые сложно угадать, обеспечивая безопасность и уникальность идентификаторов.
"""

import random
import string

from config import LEN_TOKEN


class TokenWorker:
    def __init__(self):
        self.alphabet = string.ascii_letters + string.digits

    def generate_new_token(self):
        token = [random.choice(self.alphabet) for _ in range(LEN_TOKEN)]

        return ''.join(token)


if __name__ == '__main__':
    print(TokenWorker().generate_new_token())
