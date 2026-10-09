from httpx import Response

from clients.api_client import APIClient
from typing import TypedDict

class CreateUserRequest(TypedDict):
    """
    Описание структуры запроса на создание пользователя
    """
    email: str
    password: str
    firstName: str
    lastName: str
    middleName: str

class PublicUsersClient(APIClient):
    """
    Клиент для работы с /api/v1/users
    """
    def create_user_api(self, request: CreateUserRequest) -> Response:
        """
        Метод создает нового пользователя
        :param request: Словарь с email, password, firstName, lastName, middleName
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.post("/api/v1/users", json=request)
