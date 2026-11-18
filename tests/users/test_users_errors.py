from http import HTTPStatus

import pytest
from allure_commons.types import Severity

from clients.errors_schema import InternalErrorResponseSchema, ValidationErrorResponseSchema
from clients.users.private_users_client import PrivateUsersClient, get_private_users_client
from fixtures.users import UserFixture, private_users_client
from tools.allure.epics import AllureEpic
from tools.allure.features import AllureFeature
from tools.allure.stories import AllureStory
from tools.allure.tags import AllureTag
from tools.assertions.base import assert_status_code
from tools.assertions.errors import assert_validation_error_response
from tools.assertions.schema import validate_json_schema

import allure


@pytest.mark.users
@pytest.mark.regression
@allure.tag(AllureTag.USERS, AllureTag.REGRESSION)
@allure.feature(AllureFeature.USERS)
class TestUsersErrors:
    ...
