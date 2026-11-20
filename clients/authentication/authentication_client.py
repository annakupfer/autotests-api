import allure
from httpx import Response
from pydantic import BaseModel

from clients.api_client import APIClient
from clients.public_http_builder import get_public_http_client  # Импортируем builder
from clients.authentication.authentication_schema import LoginRequestSchema, RefreshRequestSchema, LoginResponseSchema
from tools.routes import APIRoutes
from clients.api_coverage import tracker


class AuthenticationClient(APIClient):
    """
    Клиент для работы с /api/v1/authentication
    """
    @allure.step("Authenticate user")
    @tracker.track_coverage_httpx(f"{APIRoutes.AUTHENTICATION}/login")
    def login_api(self, request: LoginRequestSchema | dict) -> Response:
        """
        Метод выполняет аутентификацию пользователя.

        :param request: Словарь с email и password.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        if isinstance(request, BaseModel):
            request_data = request.model_dump(by_alias=True)
        else:
            request_data = request

        return self.post(f"{APIRoutes.AUTHENTICATION}/login", json=request_data)

    @allure.step("Refresh authentication token")
    @tracker.track_coverage_httpx(f"{APIRoutes.AUTHENTICATION}/refresh")
    def refresh_api(self, request: RefreshRequestSchema | dict) -> Response:
        """
        Метод выполняет обновление токена

        :param request: Словарь с refresh токеном
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        if isinstance(request, BaseModel):
            request_data = request.model_dump(by_alias=True)
        else:
            request_data = request

        return self.post(f"{APIRoutes.AUTHENTICATION}/refresh", json=request_data)

        # Добавили метод login
    def login(self, request: LoginRequestSchema) -> LoginResponseSchema:

        response = self.login_api(request)  # Отправляем запрос на аутентификацию
        return LoginResponseSchema.model_validate_json(response.text)


# Добавляем builder для AuthenticationClient
def get_authentication_client() -> AuthenticationClient:
    """
    Функция создаёт экземпляр AuthenticationClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию AuthenticationClient.
    """
    return AuthenticationClient(client=get_public_http_client())
