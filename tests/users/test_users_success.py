from http import HTTPStatus

import pytest
from allure_commons.types import Severity

from clients.errors_schema import InternalErrorResponseSchema
from clients.private_http_builder import AuthenticationUserSchema
from clients.users.private_users_client import PrivateUsersClient, get_private_users_client
from clients.users.public_users_client import PublicUsersClient
from clients.users.users_schema import CreateUserRequestSchema, CreateUserResponseSchema, GetUserResponseSchema, \
    UpdateUserRequestSchema, UpdateUserResponseSchema
from fixtures.users import UserFixture, private_users_client
from tools.allure.epics import AllureEpic
from tools.allure.features import AllureFeature
from tools.allure.stories import AllureStory
from tools.allure.tags import AllureTag
from tools.assertions.base import assert_status_code
from tools.assertions.schema import validate_json_schema
from tools.assertions.users import assert_create_user_response, assert_get_user_response, assert_update_user_response, \
    assert_user_not_found_response
from tools.fakers import fake

import allure


@pytest.mark.users
@pytest.mark.regression
@allure.tag(AllureTag.USERS, AllureTag.REGRESSION)
@allure.epic(AllureEpic.LMS)  # Добавили epic
@allure.feature(AllureFeature.USERS)
@allure.parent_suite(AllureEpic.LMS)  # allure.parent_suite == allure.epic
@allure.suite(AllureFeature.USERS)  # allure.suite == allure.feature
class TestUsersSuccess:
    @pytest.mark.parametrize("domain", ["mail.ru", "gmail.com", "example.com"])
    @allure.tag(AllureTag.CREATE_ENTITY)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.title("Create user")
    @allure.severity(Severity.BLOCKER)  # Добавили severity
    @allure.sub_suite(AllureStory.CREATE_ENTITY)  # allure.sub_suite == allure.story
    def test_create_user(self, domain: str, public_users_client: PublicUsersClient):  # Используем фикстуру API клиента
        # Удалили инициализацию API клиента из теста
        email = fake.email(domain=domain)
        request = CreateUserRequestSchema(email=email)

        response = public_users_client.create_user_api(request)
        response_data = CreateUserResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_create_user_response(request, response_data)

        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.tag(AllureTag.GET_ENTITY)
    @allure.story(AllureStory.GET_ENTITY)
    @allure.title("Get user me")
    @allure.severity(Severity.CRITICAL)
    @allure.sub_suite(AllureStory.GET_ENTITY)  # allure.sub_suite == allure.story
    def test_get_user_me(
            self,
            function_user: UserFixture,
            private_users_client: PrivateUsersClient
    ):
        response = private_users_client.get_user_me_api()
        response_data = GetUserResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_get_user_response(response_data, function_user.response)

        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.tag(AllureTag.GET_ENTITY)
    @allure.story(AllureStory.GET_ENTITY)
    @allure.title("Get user")
    @allure.severity(Severity.BLOCKER)
    @allure.sub_suite(AllureStory.GET_ENTITY)
    def test_get_user(self, private_users_client: PrivateUsersClient, function_user: UserFixture):
        user_id = function_user.response.user.id
        response = private_users_client.get_user_api(user_id)
        response_data = GetUserResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_get_user_response(response_data, function_user.response)

        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.tag(AllureTag.UPDATE_ENTITY)
    @allure.story(AllureStory.UPDATE_ENTITY)
    @allure.title("Update user")
    @allure.severity(Severity.CRITICAL)
    @allure.sub_suite(AllureStory.UPDATE_ENTITY)
    def test_update_user(
            self,
            private_users_client: PrivateUsersClient,
            function_user: UserFixture
    ):
        user_id = function_user.response.user.id
        request = UpdateUserRequestSchema()
        response = private_users_client.update_user_api(user_id, request)
        response_data = UpdateUserResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_update_user_response(response_data, request)

        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.tag(AllureTag.DELETE_ENTITY)
    @allure.story(AllureStory.DELETE_ENTITY)
    @allure.title("Delete user")
    @allure.severity(Severity.CRITICAL)
    @allure.sub_suite(AllureStory.DELETE_ENTITY)
    def test_delete_user(
            self,
            private_users_client: PrivateUsersClient,
            public_users_client: PublicUsersClient,
            function_user: UserFixture
    ):
        user_id = function_user.response.user.id

        # Create another user for verification
        another_user_request = CreateUserRequestSchema()
        public_users_client.create_user_api(another_user_request)

        another_user_auth = AuthenticationUserSchema(
            email=another_user_request.email,
            password=another_user_request.password
        )
        another_user_client = get_private_users_client(another_user_auth)

        # Delete the first user
        delete_response = private_users_client.delete_user_api(user_id)
        assert_status_code(delete_response.status_code, HTTPStatus.OK)

        # Check that user is deleted
        get_response = another_user_client.get_user_api(user_id)

        get_response_data = InternalErrorResponseSchema.model_validate_json(
            get_response.text
        )

        assert_status_code(get_response.status_code, HTTPStatus.NOT_FOUND)
        assert_user_not_found_response(get_response_data)

        validate_json_schema(get_response.json(), get_response_data.model_json_schema())


