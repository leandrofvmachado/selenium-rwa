import logging
import time

import pytest
from _pytest.config import hookimpl
from e2e.helpers.api_request import *
from e2e.pages.signin_page import SignInPage
from factory.user_factory import UserFactory
from faker import Faker
from py.xml import html
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.remote.remote_connection import LOGGER
from webdriver_manager.chrome import ChromeDriverManager

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
def request_payment(user):
    amount = 50
    description = "selenium_automation"
    receiver_id = user["id"]
    sender_id = "24VniajY1y"

    session = login("Giovanna74", "s3cret")
    make_new_transaction(
        session, amount, "request", description, receiver_id, sender_id
    )
    return amount, description, receiver_id, sender_id


@pytest.fixture
def user():
    user_factory = UserFactory()
    user_data = user_factory.get_user_data()

    response = signup(user_data)
    session = login(user_data["username"], user_data["password"])
    create_new_bank_account(session, response["user"]["id"])
    user_data.update({"id": response["user"]["id"]})

    return user_data


@pytest.fixture
def logged_in_user(driver, user):
    sign_in_page = SignInPage(driver)
    sign_in_page.login(user["username"], user["password"])


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
