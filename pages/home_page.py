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
    transaction_list_locator = (By.CSS_SELECTOR, '[data-test="transaction-list"]')
    transaction_list_elements_xpath = (
        '//li[starts-with(@data-test, "transaction-item")]'
    )
    transaction_list_element_sender_xpath = (
        '//*[starts-with(@data-test, "transaction-sender")]'
    )
    transaction_list_element_action_xpath = (
        '//*[starts-with(@data-test, "transaction-action")]'
    )
    transaction_list_element_receiver_xpath = (
        '//*[starts-with(@data-test, "transaction-receiver")]'
    )
    transaction_list_element_amount_xpath = (
        '//*[starts-with(@data-test, "transaction-amount")]'
    )
    top_notifications_link_locator = (
        By.CSS_SELECTOR,
        '[data-test="nav-top-notifications-link"]',
    )
    amount_filter_slider_locator = (
        By.CSS_SELECTOR,
        '[data-test="transaction-list-filter-amount-range-slider"]',
    )
    amount_filter_button_locator = (
        By.CSS_SELECTOR,
        '[data-test="transaction-list-filter-amount-range-button"]',
    )
    date_picker_button_locator = (
        By.CSS_SELECTOR,
        '[data-test="transaction-list-filter-date-range-button"]',
    )

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

    def go_to_home_page(self):
        self.find_element(self.title_locator).click()

    def go_to_personal_transactions(self):
        self.find_element(self.personal_transactions_locator).click()

    def access_last_personal_transaction(self):
        self.go_to_personal_transactions()
        personal_transactions_list = self.get_child_elements(
            self.transaction_list_locator, self.transaction_list_elements_xpath
        )
        personal_transactions_list[0].click()

    def get_transaction_info_on_personal_list(self):
        self.go_to_personal_transactions()
        personal_transactions_list = self.get_child_elements(
            self.transaction_list_locator, self.transaction_list_elements_xpath
        )

        sender_on_screen = self.find_element_in_element(
            personal_transactions_list[0], self.transaction_list_element_sender_xpath
        ).text
        receiver_on_screen = self.find_element_in_element(
            personal_transactions_list[0], self.transaction_list_element_receiver_xpath
        ).text
        action_on_screen = self.find_element_in_element(
            personal_transactions_list[0], self.transaction_list_element_action_xpath
        ).text
        amount_on_screen = self.find_element_in_element(
            personal_transactions_list[0], self.transaction_list_element_amount_xpath
        ).text
        return sender_on_screen, receiver_on_screen, action_on_screen, amount_on_screen

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
