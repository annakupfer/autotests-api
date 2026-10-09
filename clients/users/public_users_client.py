from httpx import Response

from clients.api_client import APIClient
from typing import TypedDict

class CreateUserRequest(TypedDict):
    """
    Описание структуры запроса на создание пользователя
    """
    email: str
    password: str
    first_name: str
    last_name: str
    middle_name: str

class PublicUsersClient(APIClient):
    """
    Клиент для работы с публичными эндпоинтами пользователей
    /api/v1/users
    """
    def create_user_api(self, request: CreateUserRequest) -> Response:
        """
        Метод создает нового пользователя
        :param request: Словарь с email, password, first_name, last_name, middle_name
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.post("/api/v1/users", json=request)
