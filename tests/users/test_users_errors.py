from http import HTTPStatus
from uuid import uuid4

import pytest
from allure_commons.types import Severity

from clients.errors_schema import InternalErrorResponseSchema
from clients.users.private_users_client import PrivateUsersClient
from clients.users.public_users_client import PublicUsersClient
from clients.users.users_schema import GetUserResponseSchema, UpdateUserRequestSchema, CreateUserRequestSchema
from fixtures.users import private_users_client
from testdata.users.factory import build_update_user
from tools.allure.epics import AllureEpic
from tools.allure.features import AllureFeature
from tools.allure.stories import AllureStory
from tools.allure.tags import AllureTag
from tools.assertions.base import assert_status_code
from tools.assertions.schema import validate_json_schema

import allure

from tools.assertions.users import assert_user_not_found_response, assert_create_user_with_existing_email_response


@pytest.mark.users
@pytest.mark.regression
@allure.tag(AllureTag.USERS, AllureTag.REGRESSION)
@allure.epic(AllureEpic.LMS)
@allure.feature(AllureFeature.USERS)
@allure.parent_suite(AllureEpic.LMS)
@allure.suite(AllureFeature.USERS)
class TestUsersErrors:

    @allure.tag(AllureTag.GET_ENTITY)
    @allure.story(AllureStory.GET_ENTITY)
    @allure.title("Get nonexistent user")
    @allure.severity(Severity.NORMAL)
    @allure.sub_suite(AllureStory.GET_ENTITY)
    def test_get_nonexistent_user(self, private_users_client: PrivateUsersClient):
        user_id = str(uuid4())

        response = private_users_client.get_user_api(user_id)
        response_data = InternalErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.NOT_FOUND)
        assert_user_not_found_response(response_data)

        validate_json_schema(response.json(), response_data.model_json_schema())

    @pytest.mark.skip(reason="API return 500 when updating a non-existent user")
    @allure.tag(AllureTag.UPDATE_ENTITY)
    @allure.story(AllureStory.UPDATE_ENTITY)
    @allure.title("Update nonexistent user")
    @allure.severity(Severity.NORMAL)
    @allure.sub_suite(AllureStory.UPDATE_ENTITY)
    def test_update_nonexistent_user(self, private_users_client: PrivateUsersClient):

        user_id = str(uuid4())

        request = UpdateUserRequestSchema(**build_update_user())

        response = private_users_client.update_user_api(user_id, request)
        response_data = InternalErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.NOT_FOUND)
        assert_user_not_found_response(response_data)

        validate_json_schema(response.json(), response_data.model_json_schema())

    @pytest.mark.skip(reason="API return 200 instead of 404 when deleting a non-existent user")
    @allure.tag(AllureTag.DELETE_ENTITY)
    @allure.story(AllureStory.DELETE_ENTITY)
    @allure.title("Delete nonexistent user")
    @allure.severity(Severity.NORMAL)
    @allure.sub_suite(AllureStory.DELETE_ENTITY)
    def test_delete_nonexistent_user(self, private_users_client: PrivateUsersClient):

        user_id = str(uuid4())

        response = private_users_client.delete_user_api(user_id)
        response_data = InternalErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.NOT_FOUND)
        assert_user_not_found_response(response_data)

        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.tag(AllureTag.CREATE_ENTITY)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.title("Create user with existing email")
    @allure.severity(Severity.NORMAL)
    @allure.sub_suite(AllureStory.CREATE_ENTITY)
    def test_create_user_with_existing_email(
            self,
            public_users_client: PublicUsersClient,
            private_users_client: PrivateUsersClient
    ):

        request = CreateUserRequestSchema()
        existing_user = public_users_client.create_user_api(request)
        existing_user_data = GetUserResponseSchema.model_validate_json(existing_user.text)

        email = existing_user_data.user.email
        request_with_existing_email = CreateUserRequestSchema(email=email)
        response = public_users_client.create_user_api(request_with_existing_email)

        response_data = InternalErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.FORBIDDEN)
        assert_create_user_with_existing_email_response(email, response_data)

        validate_json_schema(response.json(), response_data.model_json_schema())

