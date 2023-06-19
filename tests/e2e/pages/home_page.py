from decimal import Decimal

import pytest
from e2e.pages.base_page import BasePage
from selenium.webdriver.common.by import By


@pytest.fixture
def home_page(driver):
    home_page = HomePage(driver)
    return home_page


class HomePage(BasePage):
    """A class to represent the Home Page"""

    def __init__(self, driver):
        super().__init__(driver)

    # Locators for page elements
    title_locator = (By.CSS_SELECTOR, '[data-test="app-name-logo"]')
    balance_locator = (By.CSS_SELECTOR, '[data-test="sidenav-user-balance"]')
    new_transaction_locator = (By.CSS_SELECTOR, '[data-test="nav-top-new-transaction"]')

    # User journey methods
    def is_in_home_page(self):
        if self.check_url(pytest.url):
            return True
        else:
            return False

    def get_balance(self):
        return Decimal(
            self.find_element(self.balance_locator).text[1:].replace(",", "")
        )

    def go_to_new_transaction(self):
        self.find_element(self.new_transaction_locator).click()
