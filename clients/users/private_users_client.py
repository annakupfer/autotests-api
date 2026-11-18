from typing import Any

import allure
from httpx import Response
from pydantic import BaseModel

from clients.api_client import APIClient
from clients.private_http_builder import get_private_http_client, AuthenticationUserSchema
from clients.users.users_schema import GetUserResponseSchema, UpdateUserRequestSchema
from tools.routes import APIRoutes
from clients.api_coverage import tracker


class PrivateUsersClient(APIClient):
    """
    Клиент для работы с /api/v1/users
    """
    @allure.step("Get user me")
    @tracker.track_coverage_httpx(f"{APIRoutes.USERS}/me")
    def get_user_me_api(self) -> Response:
        """
        Метод получения текущего пользователя.

        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.get(f"{APIRoutes.USERS}/me")

    @allure.step("Get user by id {user_id}")
    @tracker.track_coverage_httpx(f'{APIRoutes.USERS}/{{user_id}}')
    def get_user_api(self, user_id: str) -> Response:
        """
        Метод получения пользователя по идентификатору.

        :param user_id: Идентификатор пользователя.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.get(f"{APIRoutes.USERS}/{user_id}")

    @allure.step("Get user by id {user_id}")
    def get_user(self, user_id: str) -> GetUserResponseSchema:
        response = self.get_user_api(user_id)
        return GetUserResponseSchema.model_validate_json(response.text)

    @allure.step("Update user by {user_id}")
    @tracker.track_coverage_httpx(f'{APIRoutes.USERS}/{{user_id}}')
    def update_user_api(
            self,
            user_id: str,
            request: UpdateUserRequestSchema | dict[str, Any]
    ) -> Response:
        """
        Метод обновления пользователя по идентификатору.

        :param user_id: Идентификатор пользователя.
        :param request: Pydantic-модель или словарь с данными пользователя.
        :return: Ответ от сервера в виде объекта httpx.Response.
        """
        if isinstance(request, BaseModel):
            request_data = request.model_dump(by_alias=True)
        else:
            request_data = request

        return self.patch(
            f"{APIRoutes.USERS}/{user_id}",
            json=request_data
        )
    @allure.step("Delete user by id {user_id}")
    @tracker.track_coverage_httpx(f'{APIRoutes.USERS}/{{user_id}}')
    def delete_user_api(self, user_id: str) -> Response:
        """
        Метод удаления пользователя по идентификатору.

        :param user_id: Идентификатор пользователя.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.delete(f"{APIRoutes.USERS}/{user_id}")

# Добавляем builder для PrivateUsersClient
def get_private_users_client(user: AuthenticationUserSchema) -> PrivateUsersClient:
    """
    Функция создаёт экземпляр PublicUsersClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию PrivateUsersClient.
    """
    return PrivateUsersClient(client=get_private_http_client(user))
