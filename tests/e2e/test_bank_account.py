import pytest
from factory.bank_account import BankAccountFactory


@pytest.fixture
def bank_account():
    bank_account = BankAccountFactory()
    account = bank_account.create_account()
    return account


def test_create_new_bank_account(logged_in_home_page, bank_account):
    bank_account_page = logged_in_home_page.go_to_bank_accounts()
    old_number_of_accounts = bank_account_page.get_number_of_bank_accounts()
    bank_account_page.create_new_bank_account(bank_account)
    new_number_of_accounts = bank_account_page.get_number_of_bank_accounts()
    bank_account_created = bank_account_page.get_recently_created_bank_account()

    assert new_number_of_accounts == old_number_of_accounts + 1
    assert bank_account_created.text == bank_account.bank_name
