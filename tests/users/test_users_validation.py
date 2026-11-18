from clients.users.users_schema import CreateUserRequestSchema, CreateUserResponseSchema, UpdateUserResponseSchema, \
    UpdateUserRequestSchema
from fixtures.users import private_users_client

from http import HTTPStatus

import allure
import pytest
from allure_commons.types import Severity

from clients.errors_schema import ValidationErrorResponseSchema
from clients.users.private_users_client import PrivateUsersClient
from clients.users.public_users_client import PublicUsersClient

from fixtures.users import UserFixture
from testdata.users.factory import build_update_user, build_create_user
from tools.allure.features import AllureFeature
from tools.allure.stories import AllureStory
from tools.allure.tags import AllureTag
from tools.assertions.base import assert_status_code
from tools.assertions.schema import validate_json_schema
from tools.assertions.users import assert_create_user_response, assert_update_user_response


@pytest.mark.users
@pytest.mark.regression
@allure.tag(AllureTag.USERS, AllureTag.REGRESSION)
@allure.feature(AllureFeature.USERS)
class TestUsersValidation:

    @staticmethod
    def build_value_with_length(field: str, max_length: int) -> str:
        if field == "email":
            domain = "@example.com"
            return f"{'a' * (max_length - len(domain))}{domain}"

        return "a" * max_length

    # Create user
    CREATE_FIELDS = [
        "email",
        "password",
        "lastName",
        "firstName",
        "middleName",
    ]

    CREATE_EMPTY_FIELDS = CREATE_FIELDS

    CREATE_BOUNDARY_LENGTH_FIELDS = [
        ("password", 250),
        ("lastName", 50),
        ("firstName", 50),
        ("middleName", 50),
    ]

    CREATE_MAX_LENGTH_FIELDS = [
        ("password", 251),
        ("lastName", 51),
        ("firstName", 51),
        ("middleName", 51),
    ]

    # Update user
    UPDATE_FIELDS = [
        "email",
        "firstName",
        "lastName",
        "middleName",
    ]

    UPDATE_EMPTY_FIELDS = UPDATE_FIELDS

    UPDATE_BOUNDARY_LENGTH_FIELDS = [
        ("lastName", 50),
        ("firstName", 50),
        ("middleName", 50),
    ]

    UPDATE_MAX_LENGTH_FIELDS = [
        ("lastName", 51),
        ("firstName", 51),
        ("middleName", 51),
    ]

    #Get user
    INVALID_USER_IDS = [
        "invalid_uuid",
        "123",
        "8e80933a-dce8-42de-ad0e",
    ]

    # Common validation data
    INVALID_EMAILS = [
        "invalid_email",
        "user@",
        "@example.com",
        "user example.com",
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
        request = build_create_user(email=email)

        response = public_users_client.create_user_api(request)
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)

        validate_json_schema(response.json(), response_data.model_json_schema())

    @pytest.mark.parametrize("email", INVALID_EMAILS)
    @allure.tag(AllureTag.UPDATE_ENTITY)
    @allure.story(AllureStory.UPDATE_ENTITY)
    @allure.title("Update user with invalid email")
    @allure.severity(Severity.NORMAL)
    def test_update_user_with_invalid_email(
        self,
        private_users_client: PrivateUsersClient,
        function_user: UserFixture,
        email: str
    ):
        user_id = function_user.response.user.id

        request = build_update_user(email=email)

        response = private_users_client.update_user_api(user_id, request)
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)

        validate_json_schema(response.json(), response_data.model_json_schema())

    @pytest.mark.parametrize("field", CREATE_EMPTY_FIELDS)
    @allure.tag(AllureTag.CREATE_ENTITY)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.title("Create user with empty {field}")
    @allure.severity(Severity.NORMAL)
    def test_create_user_with_empty_field(
            self,
            public_users_client: PublicUsersClient,
            field: str):
        request = build_create_user(**{field: ""})

        response = public_users_client.create_user_api(request)
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)

        validate_json_schema(response.json(), response_data.model_json_schema())

    @pytest.mark.parametrize("field", CREATE_FIELDS)
    @allure.tag(AllureTag.CREATE_ENTITY)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.title("Create user with null {field}")
    @allure.severity(Severity.NORMAL)
    def test_create_user_with_empty_field(
            self,
            public_users_client: PublicUsersClient,
            field: str):
        request = build_create_user(**{field: None})

        response = public_users_client.create_user_api(request)
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)

        validate_json_schema(response.json(), response_data.model_json_schema())

    @pytest.mark.parametrize(("field", "max_length"), CREATE_BOUNDARY_LENGTH_FIELDS)
    @allure.tag(AllureTag.CREATE_ENTITY)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.title("Create user with boundary {field} length")
    @allure.severity(Severity.NORMAL)
    @allure.sub_suite(AllureStory.CREATE_ENTITY)
    def test_create_user_with_boundary_length(
            self,
            field: str,
            max_length: int,
            public_users_client: PublicUsersClient,
    ):
        if field == "email":
            domain = "@example.com"
            value = f"{'a' * (max_length - len(domain))}{domain}"
        else:
            value = "a" * max_length

        request = CreateUserRequestSchema(**{field: value})

        response = public_users_client.create_user_api(request)
        response_data = CreateUserResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_create_user_response(request, response_data)

        validate_json_schema(response.json(), response_data.model_json_schema())


    @allure.tag(AllureTag.CREATE_ENTITY)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.title("Create user with email exceeding max length")
    @allure.severity(Severity.NORMAL)
    def test_create_user_with_email_exceeding_max_length(
            self,
            public_users_client: PublicUsersClient
    ):
        request = build_create_user(email=f"{'a' * 240}@example.com")

        response = public_users_client.create_user_api(request)
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)

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
        request = build_create_user(**{field: "a" * max_length})

        response = public_users_client.create_user_api(request)
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)

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
        request = build_create_user()
        request.pop(field)

        response = public_users_client.create_user_api(request)
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)

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
        request = build_update_user(**{field: ""})

        response = private_users_client.update_user_api(user_id, request)
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)

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
        request = UpdateUserRequestSchema(**build_update_user(**{field: None}))

        response = private_users_client.update_user_api(user_id, request)
        response_data = UpdateUserResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_update_user_response(response_data, request)
        validate_json_schema(response.json(), response_data.model_json_schema())

    @pytest.mark.parametrize(("field", "max_length"), UPDATE_BOUNDARY_LENGTH_FIELDS)
    @allure.tag(AllureTag.UPDATE_ENTITY)
    @allure.story(AllureStory.UPDATE_ENTITY)
    @allure.title("Update user with boundary {field} length")
    @allure.severity(Severity.NORMAL)
    @allure.sub_suite(AllureStory.UPDATE_ENTITY)
    def test_update_user_with_boundary_length(
            self,
            private_users_client: PrivateUsersClient,
            function_user: UserFixture,
            field: str,
            max_length: int
    ):
        if field == "email":
            pytest.skip("EmailStr does not allow a local part longer than 64 characters")

        user_id = function_user.response.user.id
        value = self.build_value_with_length(field, max_length)
        request = UpdateUserRequestSchema(**build_update_user(**{field: value}))

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
        if field == "email":
            pytest.skip("EmailStr does not allow a local part longer than 64 characters")

        user_id = function_user.response.user.id
        value = self.build_value_with_length(field, max_length)
        request = build_update_user(**{field: value})

        response = private_users_client.update_user_api(user_id, request)
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)

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
    def test_get_user_with_invalid_id(
            self,
            private_users_client: PrivateUsersClient,
            user_id: str
    ):
        response = private_users_client.delete_user_api(user_id)
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        validate_json_schema(response.json(), response_data.model_json_schema())