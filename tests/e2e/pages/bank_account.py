import pytest
from e2e.pages.base_page import BasePage
from faker import Faker
from selenium.webdriver.common.by import By

faker = Faker()


@pytest.fixture
def bank_account_page(driver):
    bank_account = BankAccountPage(driver)
    return bank_account


class BankAccountPage(BasePage):
    """A class to represent the Bank Account Page"""

    def __init__(self, driver):
        super().__init__(driver)

    # Locators for page elements
    create_bank_account_locator = (By.CSS_SELECTOR, '[data-test="bankaccount-new"]')
    delete_bank_account_locator = (By.CSS_SELECTOR, '[data-test="bankaccount-delete"]')
    bank_name_input_locator = (By.ID, "bankaccount-bankName-input")
    routing_number_input_locator = (By.ID, "bankaccount-routingNumber-input")
    account_number_input_locator = (By.ID, "bankaccount-accountNumber-input")
    save_bank_account_locator = (By.CSS_SELECTOR, '[data-test="bankaccount-submit"]')
    bank_account_list_locator = (By.CSS_SELECTOR, '[data-test="bankaccount-list"]')
    bank_account_list_item_xpath = (
        '//li[starts-with(@data-test, "bankaccount-list-item")]'
    )

    # User journey methods
    def is_in_bank_account(self):
        return self.check_url(pytest.url + "/bankaccounts")

    def create_bank_account(self, account):
        self.find_element(self.bank_name_input_locator).send_keys(account.bank_name)
        self.find_element(self.routing_number_input_locator).send_keys(
            account.routing_number
        )
        self.find_element(self.account_number_input_locator).send_keys(
            account.account_number
        )
        self.find_element(self.save_bank_account_locator).click()

    def create_new_bank_account(self, account):
        if account is not None:
            self.find_element(self.create_bank_account_locator).click()
            self.create_bank_account(account)

    def get_number_of_bank_accounts(self):
        bank_account_list = self.get_child_elements(
            self.bank_account_list_locator, self.bank_account_list_item_xpath
        )
        return len(bank_account_list)

    def get_recently_created_bank_account(self):
        bank_account_list = self.get_child_elements(
            self.bank_account_list_locator, self.bank_account_list_item_xpath
        )
        return bank_account_list[-1].find_element(By.TAG_NAME, "p")
