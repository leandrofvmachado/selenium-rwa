from decimal import Decimal

import pytest

from conftest import is_balance_adjusted
from factory.transaction_factory import TransactionFactory
from factory.user_factory import UserFactory
from helpers.api_request import *
from pages.home_page import home_page
from pages.signin_page import SignInPage
from pages.transaction_page import TransactionPage


@pytest.fixture
def new_transaction_page(driver):
    new_transaction_page = TransactionPage(driver)
    return new_transaction_page


@pytest.fixture
def charged_transaction(new_user):
    transaction_factory = TransactionFactory()
    sender_user = UserFactory.users["Katharina_Bernier"].to_dict()
    receiver_id = new_user["id"]
    type = "request"

    transaction = transaction_factory.create_transaction(
        type, sender_user["id"], receiver_id
    ).to_dict()

    session = login(sender_user["username"], sender_user["password"])
    transaction_response = make_new_transaction(session, transaction)
    session = login(new_user["username"], new_user["password"])
    execute_transaction(session, "accepted", transaction_response["transaction"]["id"])
    return transaction, sender_user


@pytest.fixture
def transaction_page(driver):
    return TransactionPage(driver)


@pytest.fixture(autouse=True, scope="function")
def logged_in_user(driver, new_user):
    sign_in_page = SignInPage(driver)
    sign_in_page.login(new_user["username"], new_user["password"])


def test_create_new_payment_transaction(transaction_page, home_page, new_user):
    old_balance = home_page.get_balance()
    transaction_factory = TransactionFactory()
    receiver_user = UserFactory.users["Giovanna74"].to_dict()
    receiver_id = receiver_user["id"]
    type = "payment"
    transaction = transaction_factory.create_transaction(
        type, new_user["id"], receiver_id
    ).to_dict()

    home_page.go_to_new_transaction()
    transaction_page.place_a_transaction(transaction, receiver_user)
    new_balance = home_page.get_balance()

    home_page.go_to_personal_transactions()
    transaction_page.access_last_personal_transaction()
    (
        sender_on_screen,
        receiver_on_screen,
        action_on_screen,
        amount_on_screen,
        description_on_screen,
    ) = transaction_page.get_transaction_info()

    assert home_page.is_in_home_page()
    assert is_balance_adjusted(
        old_balance, new_balance, Decimal(transaction["amount"]), home_page
    )
    assert home_page.is_in_home_page()
    assert sender_on_screen == f"{new_user['first_name']} {new_user['last_name']}"
    assert (
        receiver_on_screen
        == f"{receiver_user['first_name']} {receiver_user['last_name']}"
    )
    assert action_on_screen == "paid"
    assert amount_on_screen == f"-${transaction['amount']}.00"
    assert description_on_screen == transaction["description"]


def test_create_new_request_transaction(transaction_page, home_page, new_user):
    old_balance = home_page.get_balance()
    transaction_factory = TransactionFactory() #TODO: put this into a fixture
    receiver_user = UserFactory.users["Giovanna74"].to_dict()
    receiver_id = receiver_user["id"]
    type = "request"
    transaction = transaction_factory.create_transaction(
        type, new_user["id"], receiver_id
    ).to_dict()

    home_page.go_to_new_transaction()
    transaction_page.place_a_transaction(transaction, receiver_user)
    new_balance = home_page.get_balance()
    home_page.go_to_personal_transactions()
    transaction_page.access_last_personal_transaction()
    (
        sender_on_screen,
        receiver_on_screen,
        action_on_screen,
        amount_on_screen,
        description_on_screen,
    ) = transaction_page.get_transaction_info()

    assert is_balance_adjusted(
        old_balance, new_balance, Decimal(0.0), home_page
    )
    assert sender_on_screen == f"{new_user['first_name']} {new_user['last_name']}"
    assert (
        receiver_on_screen
        == f"{receiver_user['first_name']} {receiver_user['last_name']}"
    )
    assert action_on_screen == "requested"
    assert amount_on_screen == f"+${transaction['amount']}.00"
    assert description_on_screen == transaction["description"]


def test_check_request_paid(charged_transaction, new_user, home_page, transaction_page):
    """
    Test that check the feature of receiving money after making a request.
    The transaction is placed using the API. Both the request and the payment.
    """
    transaction, sender = charged_transaction
    home_page.go_to_personal_transactions()
    (
        sender_on_screen,
        receiver_on_screen,
        action_on_screen,
        amount_on_screen,
    ) = transaction_page.get_transaction_info_on_personal_list()

    assert sender_on_screen == f'{sender["first_name"]} {sender["last_name"]}'
    assert receiver_on_screen == f'{new_user["first_name"]} {new_user["last_name"]}'
    assert action_on_screen == "charged"
    assert amount_on_screen == f"+${transaction['amount']}.00"


def test_accept_request(home_page, transaction_page, request_transaction, new_user):
    """
    Test the acceptance of a request on the transaction page.
    The transaction is placed using the API.
    """
    transaction, sender = request_transaction
    home_page.go_to_personal_transactions()
    transaction_page.access_last_personal_transaction()
    transaction_page.accept_a_request()
    (
        sender_on_screen,
        receiver_on_screen,
        action_on_screen,
        amount_on_screen,
        description_on_screen,
    ) = transaction_page.get_transaction_info()

    assert sender_on_screen == f'{sender["first_name"]} {sender["last_name"]}'
    assert receiver_on_screen == f'{new_user["first_name"]} {new_user["last_name"]}'
    assert action_on_screen == "charged"
    assert amount_on_screen == f"+${transaction['amount']}.00"
    assert description_on_screen == transaction["description"]


def test_reject_request(home_page, transaction_page, request_transaction, new_user):
    """
    Test the rejection of a request on the transaction page.
    The transaction is placed using the API.
    """
    transaction, sender = request_transaction
    home_page.go_to_personal_transactions()
    transaction_page.access_last_personal_transaction()
    transaction_page.reject_a_request()

    (
        sender_on_screen,
        receiver_on_screen,
        action_on_screen,
        amount_on_screen,
        description_on_screen,
    ) = transaction_page.get_transaction_info()

    assert sender_on_screen == f'{sender["first_name"]} {sender["last_name"]}'
    assert receiver_on_screen == f'{new_user["first_name"]} {new_user["last_name"]}'
    assert action_on_screen == "requested"
    assert amount_on_screen == f"+${transaction['amount']}.00"
    assert description_on_screen == transaction["description"]


def test_check_like_and_comment_on_transaction_detail(
    home_page, transaction_page
):
    """
    Test the like and comment on a transaction.
    The transaction is placed using the API.
    """
    transaction_page.access_last_personal_transaction()
    old_number_of_likes = transaction_page.get_number_of_likes()
    old_number_of_comments = 0
    comment = transaction_page.like_and_comment_transaction()
    new_number_of_likes = transaction_page.get_number_of_likes()
    new_number_of_comments = transaction_page.get_number_of_comments()

    assert new_number_of_likes == old_number_of_likes + 1
    assert new_number_of_comments == old_number_of_comments + 1
    assert transaction_page.check_comment_visibility(comment)


def test_date_filter(home_page, transaction_page, new_user, request_transaction):
    home_page.set_today_date()
    transaction, sender = request_transaction
    (
        sender_on_screen,
        receiver_on_screen,
        action_on_screen,
        amount_on_screen,
    ) = transaction_page.get_transaction_info_on_personal_list()

    assert sender_on_screen == f'{sender["first_name"]} {sender["last_name"]}'
    assert receiver_on_screen == f'{new_user["first_name"]} {new_user["last_name"]}'
    assert action_on_screen == "requested"
    assert amount_on_screen == f"+${transaction['amount']}.00"
