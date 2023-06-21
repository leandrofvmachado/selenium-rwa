from decimal import Decimal

import pytest
from conftest import is_balance_adjusted, logged_in_home_page
from e2e.helpers.api_request import *
from e2e.pages.home_page import home_page
from e2e.pages.transaction_page import TransactionPage


@pytest.fixture
def new_transaction_page(driver, logged_in_home_page):
    logged_in_home_page.go_to_new_transaction()
    new_transaction_page = TransactionPage(driver)
    return new_transaction_page


@pytest.fixture
def payment_request_charged():
    amount = 50
    description = "selenium_automation"
    receiver_id = "24VniajY1y"
    sender_id = "t45AiwidW"

    session = login("Katharina_Bernier", "s3cret")
    transaction_response = make_new_transaction(
        session, amount, "request", description, receiver_id, sender_id
    )
    session = login("Giovanna74", "s3cret")
    execute_transaction(session, "accepted", transaction_response["transaction"]["id"])
    return amount, description, receiver_id, sender_id


@pytest.fixture
def payment_request_requested():
    amount = 50
    description = "selenium_automation"
    receiver_id = "t45AiwidW"
    sender_id = "24VniajY1y"

    session = login("Giovanna74", "s3cret")
    make_new_transaction(
        session, amount, "request", description, receiver_id, sender_id
    )
    return amount, description, receiver_id, sender_id


@pytest.fixture
def transaction_page(driver, logged_in_home_page):
    return TransactionPage(driver)


def test_create_new_payment_transaction(new_transaction_page, home_page):
    amount = 50
    old_balance = home_page.get_balance()
    receiver = "Ibrahim Dickens"

    home_page = new_transaction_page.make_a_transaction(receiver, amount)
    new_balance = home_page.get_balance()

    (
        sender_on_screen,
        receiver_on_screen,
        action_on_screen,
        amount_on_screen,
    ) = home_page.get_transaction_info_on_personal_list()
    assert home_page.is_in_home_page()
    assert is_balance_adjusted(old_balance, new_balance, Decimal(amount), home_page)

    assert home_page.is_in_home_page()
    assert sender_on_screen == "Edgar Johns"
    assert receiver_on_screen == receiver
    assert action_on_screen == "paid"
    assert amount_on_screen == f"-${amount}.00"


def test_create_new_request_transaction(new_transaction_page, transaction_page):
    amount = 50
    receiver = "Ibrahim Dickens"
    note = "selenium_automation"

    home_page = new_transaction_page.place_a_request(receiver, note, amount)
    home_page.access_last_personal_transaction()
    (
        sender_on_screen,
        receiver_on_screen,
        action_on_screen,
        amount_on_screen,
        description_on_screen,
    ) = transaction_page.get_transaction_info()

    assert sender_on_screen == "Edgar Johns"
    assert receiver_on_screen == receiver
    assert action_on_screen == "requested"
    assert amount_on_screen == f"+${amount}.00"
    assert description_on_screen == note


def test_check_request_paid(home_page, payment_request_charged):
    home_page.go_to_home_page()
    (
        amount_requested,
        description_requested,
        receiver_id_requested,
        sender_id_requested,
    ) = payment_request_charged
    (
        sender_on_screen,
        receiver_on_screen,
        action_on_screen,
        amount_on_screen,
    ) = home_page.get_transaction_info_on_personal_list()
    assert action_on_screen == "charged"
    assert amount_on_screen == f"+${amount_requested}.00"


def test_accept_a_request(home_page, transaction_page, payment_request_requested):
    home_page.access_last_personal_transaction()
    transaction_page.accept_a_request()

    (
        amount_requested,
        description_requested,
        receiver_id_requested,
        sender_id_requested,
    ) = payment_request_requested
    (
        sender_on_screen,
        receiver_on_screen,
        action_on_screen,
        amount_on_screen,
        description_on_screen,
    ) = transaction_page.get_transaction_info()
    assert action_on_screen == "charged"
    assert amount_on_screen == f"+${amount_requested}.00"
    assert description_on_screen == description_requested
