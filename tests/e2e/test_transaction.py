from decimal import Decimal

import pytest
from conftest import is_balance_adjusted
from e2e.pages.home_page import home_page
from e2e.pages.new_transaction_page import NewTransactionPage
from e2e.pages.signin_page import SignInPage


@pytest.fixture
def new_transaction_page(driver):
    signin_page = SignInPage(driver)
    signin_page.go_to_signin_page()
    home_page = signin_page.login("Katharina_Bernier", "s3cret")
    home_page.go_to_new_transaction()
    new_transaction_page = NewTransactionPage(driver)
    return new_transaction_page


def test_create_new_transaction(new_transaction_page, home_page):
    amount = 50
    old_balance = home_page.get_balance()

    home_page = new_transaction_page.make_a_transaction("Ibrahim Dickens", amount)
    new_balance = home_page.get_balance()
    
    assert home_page.is_in_home_page()
    assert is_balance_adjusted(old_balance, new_balance, Decimal(amount), home_page)
