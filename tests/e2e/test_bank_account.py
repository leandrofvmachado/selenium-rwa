import pytest
from e2e.helpers.api_request import create_new_bank_account, login
from factory.bank_account_factory import BankAccountFactory


@pytest.fixture
def bank_account_fixture():
    bank_account = BankAccountFactory()
    account = bank_account.create_bank_account()
    return account


@pytest.fixture
def bank_account():
    session = login("Katharina_Bernier", "s3cret")
    created_bank_account = create_new_bank_account(session, "24VniajY1y")
    return created_bank_account


def test_create_new_bank_account(logged_in_home_page, bank_account_fixture):
    bank_account_page = logged_in_home_page.go_to_bank_accounts()
    old_number_of_accounts = bank_account_page.get_number_of_bank_accounts()
    bank_account_page.create_new_bank_account(bank_account_fixture)
    new_number_of_accounts = bank_account_page.get_number_of_bank_accounts()
    bank_account_created = bank_account_page.get_recently_created_bank_account_text()

    assert new_number_of_accounts == old_number_of_accounts + 1
    assert bank_account_created == bank_account_fixture.bank_name


def test_delete_bank_account(logged_in_home_page, bank_account):
    bank_account_page = logged_in_home_page.go_to_bank_accounts()
    old_number_of_accounts = bank_account_page.get_number_of_bank_accounts()
    bank_account_page.delete_bank_account(bank_account)
    new_number_of_accounts = bank_account_page.get_number_of_bank_accounts()
    bank_account_created = bank_account_page.get_recently_created_bank_account_text()

    assert "Deleted" in bank_account_created
    assert new_number_of_accounts == old_number_of_accounts
