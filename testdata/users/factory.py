from tools.fakers import fake

def build_create_user(**overrides) -> dict:
    """
    Создаёт валидные тестовые данные для создания пользователя.
    """
    user = {
        "email": fake.email(),
        "password": fake.password(),
        "lastName": fake.last_name(),
        "firstName": fake.first_name(),
        "middleName": fake.middle_name(),
    }
    user.update(overrides)
    return user


def build_update_user(**overrides) -> dict:
    """
    Создаёт валидные тестовые данные для обновления пользователя.
    """
    user = {
        "email": fake.email(),
        "lastName": fake.last_name(),
        "firstName": fake.first_name(),
        "middleName": fake.middle_name(),
    }
    user.update(overrides)
    return user

def build_value_with_length(field: str, length: int) -> str:
    """
    Создаёт тестовое значение заданной длины.
    """
    if field == "email":
        local_part = fake.random_string(64)
        domain = f"{'b' * 63}.{'c' * 63}.{'d' * (length - 193)}"
        return f"{local_part}@{domain}"

    return "a" * length