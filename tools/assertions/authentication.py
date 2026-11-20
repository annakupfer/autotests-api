import allure

from clients.authentication.authentication_schema import LoginResponseSchema, RefreshResponseSchema
from clients.errors_schema import InternalErrorResponseSchema, ValidationErrorResponseSchema
from tools.assertions.base import assert_equal, assert_is_true, assert_length
from tools.assertions.errors import assert_internal_error_response
from tools.logger import get_logger

logger = get_logger("AUTHENTICATION_ASSERTIONS")

@allure.step("Check login response")
def assert_login_response(response: LoginResponseSchema):
    """
    Проверяет корректность ответа при успешной авторизации.

    :param response: Объект ответа с токенами авторизации.
    :raises AssertionError: Если какое-либо из условий не выполняется.
    """
    logger.info("Check login response")
    assert_equal(response.token.token_type, "bearer", "token_type")
    assert_is_true(response.token.access_token, "access_token")
    assert_is_true(response.token.refresh_token, "refresh_token")

@allure.step("Check login with invalid credentials error response")
def assert_login_with_invalid_credentials_response(actual: InternalErrorResponseSchema):
    """
    Проверяет корректность ответа при попытке авторизации с некорретными данными пользователя

    :param actual: Фактический ответ
    :raises AssertionError: Если фактический ответ не соответствует ожидаемому тексту ошибки
    """
    logger.info("Check login with invalid credentials error response")

    expected = InternalErrorResponseSchema(details="Invalid credentials")
    assert_internal_error_response(actual, expected)

@allure.step("Check login without required fields response")
def assert_login_without_required_fields_response(
        actual: ValidationErrorResponseSchema
):
    """
    Проверяет корректность ответа при попытке авторизации при отсутствии обязательных полей

    :param actual: Фактический ответ
    :raises AssertionError: Если фактический ответ не соответствует ожидаемому тексту ошибки
    """
    logger.info("Check login without required fields response")

    assert_length(actual.details, [None, None], "details")
    error_fields = [detail.location[-1] for detail in actual.details]

    assert "email" in error_fields
    assert "password" in error_fields


@allure.step("Check refresh token response")
def assert_refresh_token_response(response: RefreshResponseSchema):
    """
    Проверяет корректность ответа при успешном обновлении токенов

    :param response: Объект ответа с токенами авторизации.
    :raises AssertionError: Если какое-либо из условий не выполняется.
    """
    logger.info("Check refresh token response")
    assert_equal(response.token.token_type, "bearer", "token_type")
    assert_is_true(response.token.access_token, "access_token")
    assert_is_true(response.token.refresh_token, "refresh_token")
    
    
@allure.step("Check refresh token with invalid value response")
def assert_refresh_token_with_invalid_value_response(actual: InternalErrorResponseSchema):
    """
    Проверяет корректность ответа при обновлении токена с невалидным значением

    :param actual: Фактический ответ API с ошибкой
    :raises AssertionError: Если какое-либо из условий не выполняется.
    """
    logger.info("Check refresh token with invalid value response")

    expected = InternalErrorResponseSchema(details="Invalid or expired refresh token")
    assert_internal_error_response(actual, expected)