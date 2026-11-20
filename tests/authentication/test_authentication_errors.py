from http import HTTPStatus

import allure
import pytest
from allure_commons.types import Severity

from clients.authentication.authentication_client import AuthenticationClient
from clients.authentication.authentication_schema import LoginRequestSchema, RefreshRequestSchema
from clients.errors_schema import InternalErrorResponseSchema, ValidationErrorResponseSchema
from fixtures.users import UserFixture
from tools.allure.epics import AllureEpic
from tools.allure.features import AllureFeature
from tools.allure.stories import AllureStory
from tools.allure.tags import AllureTag
from tools.assertions.authentication import assert_login_with_invalid_credentials_response, \
    assert_refresh_token_with_invalid_value_response
from tools.assertions.base import assert_status_code
from tools.assertions.errors import assert_validation_error_for_field
from tools.assertions.schema import validate_json_schema
from tools.fakers import fake


@pytest.mark.regression
@pytest.mark.authentication
@allure.tag(AllureTag.AUTHENTICATION, AllureTag.REGRESSION)
@allure.epic(AllureEpic.LMS)
@allure.feature(AllureFeature.AUTHENTICATION)
@allure.parent_suite(AllureEpic.LMS)
@allure.suite(AllureFeature.AUTHENTICATION)


class TestAuthenticationErrors:
    @pytest.mark.parametrize("password", ["invalid_password", ""])
    @allure.title("Login with invalid password: {password}")
    @allure.story(AllureStory.LOGIN)
    @allure.severity(Severity.CRITICAL)
    @allure.sub_suite(AllureStory.LOGIN)
    def test_login_with_invalid_password(
            self,
            function_user: UserFixture,
            authentication_client: AuthenticationClient,
            password: str
    ):

        request_data = {"email": function_user.email, "password": password}
        request = LoginRequestSchema(**request_data)

        response = authentication_client.login_api(request)
        response_data = InternalErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.UNAUTHORIZED)
        assert_login_with_invalid_credentials_response(response_data)

        validate_json_schema(response.json(), response_data.model_json_schema())


    @allure.title("Login with nonexistent user credentials")
    @allure.story(AllureStory.LOGIN)
    @allure.severity(Severity.CRITICAL)
    @allure.sub_suite(AllureStory.LOGIN)
    def test_login_with_nonexistent_user_credentials(
            self,
            authentication_client: AuthenticationClient
    ):

        request = LoginRequestSchema(
                    email=f"{fake.uuid4()}@example.com",
                    password="ValidPassword123"
        )

        response = authentication_client.login_api(request)
        response_data = InternalErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.UNAUTHORIZED)
        assert_login_with_invalid_credentials_response(response_data)

        validate_json_schema(response.json(), response_data.model_json_schema())


    @pytest.mark.parametrize("refresh_token", ["Invalid_refresh_token", ""])
    @allure.title("Refresh token with invalid value")
    @allure.story(AllureStory.REFRESH)
    @allure.severity(Severity.CRITICAL)
    @allure.sub_suite(AllureStory.REFRESH)
    def test_refresh_token_with_invalid_value(
            self,
            function_user: UserFixture,
            authentication_client: AuthenticationClient,
            refresh_token: str
    ):

        refresh_request = RefreshRequestSchema(refresh_token=refresh_token)

        response = authentication_client.refresh_api(refresh_request)
        response_data = InternalErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.UNAUTHORIZED)
        assert_refresh_token_with_invalid_value_response(response_data)

        validate_json_schema(response.json(), response_data.model_json_schema())


    @allure.title("Refresh token without token")
    @allure.story(AllureStory.REFRESH)
    @allure.severity(Severity.CRITICAL)
    @allure.sub_suite(AllureStory.REFRESH)
    def test_refresh_token_without_token(
            self,
            function_user: UserFixture,
            authentication_client: AuthenticationClient
    ):

        response = authentication_client.refresh_api({})
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        assert_validation_error_for_field(response_data, field="refreshToken")

        validate_json_schema(response.json(), response_data.model_json_schema())
