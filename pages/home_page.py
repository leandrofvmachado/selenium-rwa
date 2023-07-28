from datetime import date
from decimal import Decimal

import pytest
from selenium.webdriver.common.by import By

from pages.bank_account import BankAccountPage
from pages.base_page import BasePage
from pages.notification_page import NotificationPage


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
    bank_account_locator = (By.CSS_SELECTOR, '[data-test="sidenav-bankaccounts"]')
    notifications_locator = (By.CSS_SELECTOR, '[data-test="sidenav-notifications"]')
    new_transaction_locator = (By.CSS_SELECTOR, '[data-test="nav-top-new-transaction"]')
    personal_transactions_locator = (By.CSS_SELECTOR, '[data-test="nav-personal-tab"]')
    date_picker_button_locator = (
        By.CSS_SELECTOR,
        '[data-test="transaction-list-filter-date-range-button"]',
    )
    top_notifications_link_locator = (
        By.CSS_SELECTOR,
        '[data-test="nav-top-notifications-link"]',
    )
    
    # User journey methods,
    def is_in_home_page(self):
        if self.check_url(pytest.url):
            return True
        else:
            return False

    def get_balance(self):
        return Decimal(
            self.find_element(self.balance_locator).text[1:].replace(",", "")
        )
    
    def go_to_personal_transactions(self):
        self.find_element(self.personal_transactions_locator).click()

    def go_to_new_transaction(self):
        self.find_element(self.new_transaction_locator).click()

    def go_to_home_page(self):
        self.find_element(self.title_locator).click()

    def go_to_bank_accounts(self):
        self.find_element(self.bank_account_locator).click()
        return BankAccountPage(self.driver)

    def go_to_notifications(self):
        self.find_element(self.notifications_locator).click()
        return NotificationPage(self.driver)

    def get_number_of_notifications(self):
        if self.is_in_home_page():
            return int(self.find_element(self.top_notifications_link_locator).text)

    def set_today_date(self):
        self.find_element(self.date_picker_button_locator).click()
        today_date = date.today().strftime("%Y-%m-%d")
        today_date_xpath = (By.XPATH, f'//*[starts-with(@data-date, "{today_date}")]')
        self.find_element(today_date_xpath).click()
        self.find_element(today_date_xpath).click()
