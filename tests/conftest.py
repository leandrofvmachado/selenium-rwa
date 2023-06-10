from _pytest.config import hookimpl
from py.xml import html
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from faker import Faker
import logging
from selenium.webdriver.remote.remote_connection import LOGGER

from e2e.pages.base_page import BasePage

LOGGER.setLevel(logging.WARNING)
logging.getLogger('faker.factory').setLevel(logging.ERROR)
fake = Faker()

@pytest.fixture(autouse=True, scope="session")
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()), options=chrome_options
    )
    yield driver
    driver.quit()
    
@pytest.fixture(autouse=True, scope='session')
def url():
    pytest.url = "http://localhost:3000"


def create_signup_data():
    return {
        "first_name": fake.lexify(text='?????'),
        "password": fake.bothify(text='??##??##??##'),
        "last_name": fake.lexify(text='?????'),
        "username": fake.lexify(text='?????'),
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
