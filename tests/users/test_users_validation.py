from clients.users.users_schema import CreateUserRequestSchema, CreateUserResponseSchema, UpdateUserResponseSchema, \
    UpdateUserRequestSchema

from http import HTTPStatus

import allure
import pytest
from allure_commons.types import Severity

from clients.errors_schema import ValidationErrorResponseSchema
from clients.users.private_users_client import PrivateUsersClient
from clients.users.public_users_client import PublicUsersClient

from fixtures.users import UserFixture
from testdata.invalid_data import INVALID_EMAILS
from testdata.users.factory import build_update_user, build_create_user, build_value_with_length
from tools.allure.features import AllureFeature
from tools.allure.stories import AllureStory
from tools.allure.tags import AllureTag
from tools.assertions.base import assert_status_code
from tools.assertions.errors import assert_validation_error_for_field
from tools.assertions.schema import validate_json_schema
from tools.assertions.users import assert_create_user_response, assert_update_user_response


@pytest.mark.users
@pytest.mark.regression
@allure.tag(AllureTag.USERS, AllureTag.REGRESSION)
@allure.feature(AllureFeature.USERS)
class TestUsersValidation:

    # Create user
    CREATE_FIELDS = [
        "email",
        "password",
        "lastName",
        "firstName",
        "middleName",
    ]

    CREATE_MAX_LENGTH_FIELDS = [
        ("email", 250),
        ("password", 250),
        ("lastName", 50),
        ("firstName", 50),
        ("middleName", 50),
    ]

    CREATE_MIN_LENGTH_FIELDS = [
        ("password", 1),
        ("lastName", 1),
        ("firstName", 1),
        ("middleName", 1),
    ]

    # Update user
    UPDATE_FIELDS = [
        "email",
        "firstName",
        "lastName",
        "middleName",
    ]

    UPDATE_MAX_LENGTH_FIELDS = [
        ("email", 250),
        ("lastName", 50),
        ("firstName", 50),
        ("middleName", 50),
    ]

    UPDATE_MIN_LENGTH_FIELDS = [
        ("lastName", 1),
        ("firstName", 1),
        ("middleName", 1),
    ]
    # Get user
    INVALID_USER_IDS = [
        "invalid_uuid",
        "123",
        "8e80933a-dce8-42de-ad0e",
    ]

    @pytest.mark.parametrize("email", INVALID_EMAILS)
    @allure.tag(AllureTag.CREATE_ENTITY)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.title("Create user with invalid email: {email}")
    @allure.severity(Severity.NORMAL)
    def test_create_user_with_invalid_email(
            self,
            public_users_client: PublicUsersClient,
            email: str
    ):
        request_data = build_create_user(email=email)
        request = CreateUserRequestSchema.model_construct(**request_data)

        response = public_users_client.create_user_api(request)
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        assert_validation_error_for_field(response_data, "email")

        validate_json_schema(response.json(), response_data.model_json_schema())


    @pytest.mark.parametrize("email", INVALID_EMAILS)
    @allure.tag(AllureTag.UPDATE_ENTITY)
    @allure.story(AllureStory.UPDATE_ENTITY)
    @allure.title("Update user with invalid email: {email}")
    @allure.severity(Severity.NORMAL)
    def test_update_user_with_invalid_email(
        self,
        private_users_client: PrivateUsersClient,
        function_user: UserFixture,
        email: str
    ):
        user_id = function_user.response.user.id

        request_data = build_update_user(email=email)
        request = UpdateUserRequestSchema.model_construct(**request_data)

        response = private_users_client.update_user_api(user_id, request)
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        assert_validation_error_for_field(response_data, "email")

        validate_json_schema(response.json(), response_data.model_json_schema())


    @pytest.mark.parametrize("field", CREATE_FIELDS)
    @allure.tag(AllureTag.CREATE_ENTITY)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.title("Create user with empty {field}")
    @allure.severity(Severity.NORMAL)
    def test_create_user_with_empty_field(
            self,
            public_users_client: PublicUsersClient,
            field: str):

        request_data = build_create_user(**{field: ""})

        response = public_users_client.create_user_api(request_data)
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        assert_validation_error_for_field(response_data, field)

        validate_json_schema(response.json(), response_data.model_json_schema())


    @pytest.mark.parametrize("field", CREATE_FIELDS)
    @allure.tag(AllureTag.CREATE_ENTITY)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.title("Create user with null {field}")
    @allure.severity(Severity.NORMAL)
    def test_create_user_with_null_field(
            self,
            public_users_client: PublicUsersClient,
            field: str):

        request_data = build_create_user(**{field: None})

        response = public_users_client.create_user_api(request_data)
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        assert_validation_error_for_field(response_data, field)

        validate_json_schema(response.json(), response_data.model_json_schema())


    @pytest.mark.parametrize(("field", "min_length"), CREATE_MIN_LENGTH_FIELDS)
    @allure.tag(AllureTag.CREATE_ENTITY)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.title("Create user with minimum {field} length")
    @allure.severity(Severity.NORMAL)
    def test_create_user_with_min_length(
            self,
            public_users_client: PublicUsersClient,
            field: str,
            min_length: int
    ):
        value = "a" * min_length

        request_data = build_create_user(**{field: value})
        request = CreateUserRequestSchema(**request_data)

        response = public_users_client.create_user_api(request)
        response_data = CreateUserResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_create_user_response(request, response_data)

        validate_json_schema(response.json(), response_data.model_json_schema())


    @pytest.mark.parametrize(("field", "max_length"), CREATE_MAX_LENGTH_FIELDS)
    @allure.tag(AllureTag.CREATE_ENTITY)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.title("Create user with max {field} length")
    @allure.severity(Severity.NORMAL)
    @allure.sub_suite(AllureStory.CREATE_ENTITY)
    def test_create_user_with_max_length(
            self,
            field: str,
            max_length: int,
            public_users_client: PublicUsersClient,
    ):
        value = build_value_with_length(field, max_length)

        request_data = build_create_user(**{field: value})
        request = CreateUserRequestSchema(**request_data)

        response = public_users_client.create_user_api(request)
        response_data = CreateUserResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_create_user_response(request, response_data)

        validate_json_schema(response.json(), response_data.model_json_schema())


    @pytest.mark.parametrize("field, max_length", CREATE_MAX_LENGTH_FIELDS)
    @allure.tag(AllureTag.CREATE_ENTITY)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.title("Create user with {field} exceeding max length")
    @allure.severity(Severity.NORMAL)
    def test_create_user_with_field_exceeding_max_length(
            self,
            public_users_client: PublicUsersClient,
            field: str,
            max_length: int
    ):
        value = build_value_with_length(field, max_length + 1)

        request_data = build_create_user(**{field: value})
        request = CreateUserRequestSchema(**request_data)

        response = public_users_client.create_user_api(request)
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        assert_validation_error_for_field(response_data, field)

        validate_json_schema(response.json(), response_data.model_json_schema())

    @pytest.mark.parametrize("field", CREATE_FIELDS)
    @allure.tag(AllureTag.CREATE_ENTITY)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.title("Create user without required {field}")
    @allure.severity(Severity.NORMAL)
    def test_create_user_without_required_field(
            self,
            public_users_client: PublicUsersClient,
            field: str
    ):
        request_data = build_create_user()
        request_data.pop(field)

        response = public_users_client.create_user_api(request_data)
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        assert_validation_error_for_field(response_data, field)

        validate_json_schema(response.json(), response_data.model_json_schema())

    @pytest.mark.parametrize("field", UPDATE_FIELDS)
    @allure.tag(AllureTag.UPDATE_ENTITY)
    @allure.story(AllureStory.UPDATE_ENTITY)
    @allure.title("Update user with empty {field}")
    @allure.severity(Severity.NORMAL)
    def test_update_user_with_empty_field(
            self,
            private_users_client: PrivateUsersClient,
            function_user: UserFixture,
            field: str,
    ):
        user_id = function_user.response.user.id

        request_data = build_update_user(**{field: ""})
        request = UpdateUserRequestSchema.model_construct(**request_data)

        response = private_users_client.update_user_api(user_id, request)
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        assert_validation_error_for_field(response_data, field)

        validate_json_schema(response.json(), response_data.model_json_schema())

    @pytest.mark.skip(reason="API returns 500 when updating user fields with null")
    @pytest.mark.parametrize("field", UPDATE_FIELDS)
    @allure.tag(AllureTag.UPDATE_ENTITY)
    @allure.story(AllureStory.UPDATE_ENTITY)
    @allure.title("Update user with null {field}")
    @allure.severity(Severity.NORMAL)
    def test_update_user_with_null_field(
            self,
            private_users_client: PrivateUsersClient,
            function_user: UserFixture,
            field: str,
    ):
        user_id = function_user.response.user.id

        request_data = build_update_user(**{field: None})
        request = UpdateUserRequestSchema.model_construct(**request_data)

        response = private_users_client.update_user_api(user_id, request)
        response_data = UpdateUserResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_update_user_response(response_data, request)

        validate_json_schema(response.json(), response_data.model_json_schema())


    @pytest.mark.parametrize(("field", "min_length"), UPDATE_MIN_LENGTH_FIELDS)
    @allure.tag(AllureTag.UPDATE_ENTITY)
    @allure.story(AllureStory.UPDATE_ENTITY)
    @allure.title("Update user with minimum {field} length")
    @allure.severity(Severity.NORMAL)
    def test_update_user_with_min_length(
            self,
            private_users_client: PrivateUsersClient,
            function_user: UserFixture,
            field: str,
            min_length: int
    ):
        user_id = function_user.response.user.id
        value = "a" * min_length

        request_data = build_update_user(**{field: value})
        request = UpdateUserRequestSchema(**request_data)

        response = private_users_client.update_user_api(user_id, request)
        response_data = UpdateUserResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_update_user_response(response_data, request)

        validate_json_schema(response.json(), response_data.model_json_schema())


    @pytest.mark.parametrize(("field", "max_length"), UPDATE_MAX_LENGTH_FIELDS)
    @allure.tag(AllureTag.UPDATE_ENTITY)
    @allure.story(AllureStory.UPDATE_ENTITY)
    @allure.title("Update user with boundary {field} length")
    @allure.severity(Severity.NORMAL)
    @allure.sub_suite(AllureStory.UPDATE_ENTITY)
    def test_update_user_with_max_length(
            self,
            private_users_client: PrivateUsersClient,
            function_user: UserFixture,
            field: str,
            max_length: int
    ):

        user_id = function_user.response.user.id
        value = build_value_with_length(field, max_length)

        request_data = build_update_user(**{field: value})
        request = UpdateUserRequestSchema(**request_data)

        response = private_users_client.update_user_api(user_id, request)
        response_data = UpdateUserResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_update_user_response(response_data, request)

        validate_json_schema(response.json(), response_data.model_json_schema())

    @pytest.mark.parametrize(("field", "max_length"), UPDATE_MAX_LENGTH_FIELDS)
    @allure.tag(AllureTag.UPDATE_ENTITY)
    @allure.story(AllureStory.UPDATE_ENTITY)
    @allure.title("Update user with {field} exceeding max length")
    @allure.severity(Severity.NORMAL)
    @allure.sub_suite(AllureStory.UPDATE_ENTITY)
    def test_update_user_with_field_exceeding_max_length(
            self,
            private_users_client: PrivateUsersClient,
            function_user: UserFixture,
            field: str,
            max_length: int
    ):

        user_id = function_user.response.user.id
        value = build_value_with_length(field, max_length + 1)

        request_data = build_update_user(**{field: value})
        request = UpdateUserRequestSchema(**request_data)

        response = private_users_client.update_user_api(user_id, request)
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        assert_validation_error_for_field(response_data, field)

        validate_json_schema(response.json(), response_data.model_json_schema())

    @pytest.mark.parametrize("user_id", INVALID_USER_IDS)
    @allure.tag(AllureTag.GET_ENTITY)
    @allure.story(AllureStory.GET_ENTITY)
    @allure.tag(AllureTag.USERS, AllureTag.REGRESSION)
    @allure.title("Get user with invalid ID")
    @allure.severity(Severity.NORMAL)
    def test_get_user_with_invalid_id(
            self,
            private_users_client: PrivateUsersClient,
            user_id: str
    ):
        response = private_users_client.get_user_api(user_id)
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        validate_json_schema(response.json(), response_data.model_json_schema())

    @pytest.mark.parametrize("user_id", INVALID_USER_IDS)
    @allure.tag(AllureTag.DELETE_ENTITY)
    @allure.story(AllureStory.DELETE_ENTITY)
    @allure.tag(AllureTag.USERS, AllureTag.REGRESSION)
    @allure.title("Delete user with invalid ID")
    @allure.severity(Severity.NORMAL)
    def test_delete_user_with_invalid_id(
            self,
            private_users_client: PrivateUsersClient,
            user_id: str
    ):
        response = private_users_client.delete_user_api(user_id)
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        validate_json_schema(response.json(), response_data.model_json_schema())