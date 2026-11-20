from http import HTTPStatus
from typing import Any

import allure
import pytest
from allure_commons.types import Severity

from clients.authentication.authentication_client import AuthenticationClient
from clients.authentication.authentication_schema import LoginRequestSchema
from clients.errors_schema import ValidationErrorResponseSchema
from fixtures.users import UserFixture
from testdata.invalid_data import INVALID_EMAILS
from tools.allure.epics import AllureEpic
from tools.allure.features import AllureFeature
from tools.allure.stories import AllureStory
from tools.allure.tags import AllureTag
from tools.assertions.authentication import assert_login_without_required_fields_response
from tools.assertions.base import assert_status_code
from tools.assertions.errors import assert_validation_error_for_field
from tools.assertions.schema import validate_json_schema

@pytest.mark.regression
@pytest.mark.authentication
@allure.tag(AllureTag.AUTHENTICATION, AllureTag.REGRESSION)
@allure.epic(AllureEpic.LMS)
@allure.feature(AllureFeature.AUTHENTICATION)
@allure.parent_suite(AllureEpic.LMS)
@allure.suite(AllureFeature.AUTHENTICATION)


class TestAuthenticationValidation:

    @pytest.mark.parametrize("email", INVALID_EMAILS)
    @allure.title("Login with invalid email")
    @allure.story(AllureStory.LOGIN)
    @allure.severity(Severity.CRITICAL)
    @allure.sub_suite(AllureStory.LOGIN)
    def test_login_with_invalid_email(
            self,
            function_user: UserFixture,
            authentication_client: AuthenticationClient,
            email: str
    ):
        request_data = {"email": email, "password": function_user.password}
        request = LoginRequestSchema(**request_data)

        response = authentication_client.login_api(request)
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        assert_validation_error_for_field(response_data, field="email")

        validate_json_schema(response.json(), response_data.model_json_schema())


    @pytest.mark.parametrize("field", ["email", "password"])
    @allure.title("Login without required field: {field}")
    @allure.story(AllureStory.LOGIN)
    @allure.severity(Severity.CRITICAL)
    @allure.sub_suite(AllureStory.LOGIN)
    def test_login_without_required_field(
            self,
            function_user: UserFixture,
            authentication_client: AuthenticationClient,
            field: str,
    ):
        request_data = {"email": function_user.email, "password": function_user.password}
        request_data.pop(field)

        response = authentication_client.login_api(request_data)
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        assert_validation_error_for_field(response_data, field=field)

        validate_json_schema(response.json(), response_data.model_json_schema())


    @allure.title("Login without required fields")
    @allure.story(AllureStory.LOGIN)
    @allure.severity(Severity.CRITICAL)
    @allure.sub_suite(AllureStory.LOGIN)
    def test_login_without_required_fields(
            self,
            authentication_client: AuthenticationClient,
    ):
        response = authentication_client.login_api({})
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        assert_login_without_required_fields_response(response_data)

        validate_json_schema(response.json(), response_data.model_json_schema())


    @pytest.mark.parametrize(
        "field, invalid_value",
        [
            ("email", None),
            ("email", 123),
            ("email", 12.5),
            ("email", True),
            ("email", []),
            ("email", {}),
            ("password", None),
            ("password", 123),
            ("password", 12.5),
            ("password", True),
            ("password", []),
            ("password", {}),
        ]
    )

    @allure.title("Login with invalid value type for {field}")
    @allure.story(AllureStory.LOGIN)
    @allure.severity(Severity.CRITICAL)
    @allure.sub_suite(AllureStory.LOGIN)
    def test_login_with_invalid_data_type(
            self,
            function_user: UserFixture,
            authentication_client: AuthenticationClient,
            field: str,
            invalid_value: Any
    ):
        request_data = {"email": function_user.email, "password": function_user.password}
        request_data[field] = invalid_value

        response = authentication_client.login_api(request_data)
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        assert_validation_error_for_field(response_data, field=field)

        validate_json_schema(response.json(), response_data.model_json_schema())