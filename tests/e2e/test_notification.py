import pytest
from e2e.helpers.api_request import create_new_bank_account, login
from e2e.pages.home_page import home_page
from e2e.pages.signin_page import SignInPage
from factory.bank_account_factory import BankAccountFactory


@pytest.fixture
def bank_account_fixture():
    bank_account = BankAccountFactory()
    account = bank_account.create_account()
    return account


@pytest.fixture
def bank_account():
    session = login("Katharina_Bernier", "s3cret")
    created_bank_account = create_new_bank_account(session, "24VniajY1y")
    return created_bank_account


def test_dismiss_single_last_notification(driver, request_payment, user, home_page):
    sign_in_page = SignInPage(driver)
    sign_in_page.login(user["username"], user["password"])

    old_notification_counter = home_page.get_number_of_notifications()
    notification_page = home_page.go_to_notifications()
    notification_page.dismiss_last_notification()
    new_notification_counter = home_page.get_number_of_notifications()

    assert new_notification_counter == old_notification_counter - 1
    assert notification_page.is_notification_list_empty()
