import logging
import time

import pytest
from _pytest.config import hookimpl
from faker import Faker
from py.xml import html
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.remote.remote_connection import LOGGER
from webdriver_manager.chrome import ChromeDriverManager

from factory.transaction_factory import TransactionFactory
from factory.user_factory import UserFactory
from helpers.api_request import *
from pages.signin_page import SignInPage

LOGGER.setLevel(logging.WARNING)
logging.getLogger("faker.factory").setLevel(logging.ERROR)
fake = Faker()


@pytest.fixture(autouse=True, scope="function")
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()), options=chrome_options
    )
    yield driver
    driver.quit()


@pytest.fixture(autouse=True, scope="session")
def url():
    pytest.url = "http://localhost:3000"


@pytest.fixture()
def logged_in_home_page(driver):
    signin_page = SignInPage(driver)
    signin_page.go_to_signin_page()
    home_page = signin_page.login("Katharina_Bernier", "s3cret")
    return home_page


@pytest.fixture
def request_transaction(new_user):
    transaction_factory = TransactionFactory()
    sender_user = UserFactory.users["Katharina_Bernier"].to_dict()
    receiver_id = new_user["id"]
    type = "request"

    transaction = transaction_factory.create_transaction(
        type, sender_user["id"], receiver_id
    ).to_dict()

    session = login(sender_user["username"], sender_user["password"])
    make_new_transaction(session, transaction)
    return transaction, sender_user


def add_balance(session, user):
    transaction_factory = TransactionFactory()
    sender_user = UserFactory.users["Katharina_Bernier"].to_dict()
    receiver_id = user["id"]
    type = "payment"

    transaction = transaction_factory.create_transaction(
        type, sender_user["id"], receiver_id
    )
    transaction.set_amount(50)
    transaction = transaction.to_dict()

    session = login(sender_user["username"], sender_user["password"])
    make_new_transaction(session, transaction)
    return transaction, sender_user


@pytest.fixture
def new_user():
    user_factory = UserFactory()
    user = user_factory.create_user()

    response = signup(user.to_signup_dict())
    session = login(user.to_dict()["username"], user.to_dict()["password"])
    user.set_id(response["user"]["id"])
    create_new_bank_account(session, response["user"]["id"])
    add_balance(session, user.to_dict())

    return user.to_dict()


def is_balance_adjusted(old_balance, new_balance, amount, home_page):
    max_time = 10
    iterator = 0
    while old_balance != new_balance + amount:
        time.sleep(1)
        iterator += 1
        new_balance = home_page.get_balance()
        if iterator > max_time:
            return False

    return True


def create_signup_data():
    return {
        "first_name": fake.lexify(text="?????"),
        "password": fake.bothify(text="??##??##??##"),
        "last_name": fake.lexify(text="?????"),
        "username": fake.lexify(text="?????"),
    }


def pytest_html_results_table_header(cells):
    del cells[1]
    cells.insert(0, html.th("Testcase"))
    cells.pop()


def pytest_html_results_table_row(report, cells):
    del cells[1]
    cells.insert(0, html.td(report.testcase))
    cells.pop()


@hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    testcase = str(item.function.__doc__)
    c = str(item.function.__name__)[5:]

    report.testcase = f"{c} [{testcase}]"


def pytest_html_report_title(report):
    report.title = "E2E Tio Patinhas"


def pytest_configure(config):
    config._metadata = {}
