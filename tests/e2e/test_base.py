import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from tests.e2e.pages.base_page import BasePage


@pytest.fixture
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()), options=chrome_options
    )
    yield driver
    driver.quit()


def test_google(driver):
    base_page = BasePage(driver)
    base_page.get_url("https://www.google.com/")
    assert driver.title == "Google"
