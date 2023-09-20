import re


def validate_password(password):
    if len(password) < 8:
        return 'Пароль должен быть больше восьми символов'

    if not re.search(r'[A-Z]', password) or not re.search(r'[a-z]', password):
        return 'Пароль должен содеражть как строчные так и прописные символы'

    if not re.search(r'\d', password):
        return 'Пароль должен содеражть цифры'

    # if not re.search(r'[!@#$%^&*()_+]', password):
    #     return False

    return True
