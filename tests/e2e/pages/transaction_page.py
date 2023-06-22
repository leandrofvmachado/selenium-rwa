import pytest
from pages.base_page import BasePage
from pages.home_page import HomePage
from selenium.webdriver.common.by import By


class TransactionPage(BasePage):
    """A class to represent the New/transaction Page"""

    def __init__(self, driver):
        super().__init__(driver)

    # Locators for page elements
    search_input_locator = (By.ID, "user-list-search-input")
    user_list_locator = (By.CSS_SELECTOR, '[data-test="users-list"]')
    child_user_list_locator = '//li[starts-with(@data-test, "user-list-item")]'
    amount_input_locator = (By.ID, "amount")
    add_a_note_input_locator = (By.ID, "transaction-create-description-input")
    request_button_locator = (
        By.CSS_SELECTOR,
        '[data-test="transaction-create-submit-request"]',
    )
    payment_button_locator = (
        By.CSS_SELECTOR,
        '[data-test="transaction-create-submit-payment"]',
    )
    return_to_transactions_button_locator = (
        By.CSS_SELECTOR,
        '[data-test="new-transaction-return-to-transactions"]',
    )
    create_another_transaction_button_locator = (
        By.CSS_SELECTOR,
        '[data-test="new-transaction-create-another-transaction"]',
    )
    balance_locator = (By.CSS_SELECTOR, '[data-test="sidenav-user-balance"]')
    accept_request_locator = (
        By.XPATH,
        '//button[starts-with(@data-test, "transaction-accept-request")]',
    )
    reject_request_locator = (
        By.XPATH,
        '//button[starts-with(@data-test, "transaction-reject-request")]',
    )
    transaction_sender_locator = (
        By.XPATH,
        '//span[starts-with(@data-test, "transaction-sender")]',
    )
    transaction_action_locator = (
        By.XPATH,
        '//*[starts-with(@data-test, "transaction-action")]',
    )
    transaction_receiver_locator = (
        By.XPATH,
        '//span[starts-with(@data-test, "transaction-receiver")]',
    )
    transaction_amount_locator = (
        By.XPATH,
        '//*[starts-with(@data-test, "transaction-amount")]',
    )
    transaction_description_locator = (
        By.XPATH,
        '//*[starts-with(@data-test, "transaction-description")]',
    )

    # paid 50 for a,
    # User journey methods
    def make_a_transaction(self, receiver_name, amount=50):
        self.find_element(self.search_input_locator).send_keys(receiver_name)
        self.wait_until_list_is_loaded_correctly(
            self.user_list_locator, self.child_user_list_locator, receiver_name
        )
        self.find_element(self.user_list_locator).click()
        self.find_element(self.amount_input_locator).send_keys(amount)
        self.find_element(self.add_a_note_input_locator).send_keys(
            "selenium automation"
        )
        self.find_element(self.payment_button_locator).click()
        self.find_element(self.return_to_transactions_button_locator).click()
        home_page = HomePage(self.driver)
        # TODO check text send 50 for a selenium automation
        # TODO go in mine tab and check the transaction is there
        return home_page

    def place_a_request(self, receiver_name, note, amount=50):
        self.find_element(self.search_input_locator).send_keys(receiver_name)
        self.wait_until_list_is_loaded_correctly(
            self.user_list_locator, self.child_user_list_locator, receiver_name
        )
        self.find_element(self.user_list_locator).click()
        self.find_element(self.amount_input_locator).send_keys(amount)
        self.find_element(self.add_a_note_input_locator).send_keys(note)
        self.find_element(self.request_button_locator).click()
        assert self.find_element(
            (By.XPATH, "//*[contains(text(), '{}')]".format(f"Requested"))
        )
        self.find_element(self.return_to_transactions_button_locator).click()
        home_page = HomePage(self.driver)
        return home_page

    def is_in_new_transaction_page(self):
        self.check_url(pytest.url + "/transaction/new")

    def take_action_on_request(self, action):
        assert (
            self.find_element(self.transaction_action_locator).text == "requested"
        ), "Transaction is not a payment request"
        if action == "accept":
            self.find_element(self.accept_request_locator).click()
        else:
            self.find_element(self.reject_request_locator).click()

    def reject_a_request(self):
        self.take_action_on_request("reject")

    def accept_a_request(self):
        self.take_action_on_request("accept")

    def get_transaction_info(self):
        sender = self.find_element(self.transaction_sender_locator).text
        receiver = self.find_element(self.transaction_receiver_locator).text
        action = self.find_element(self.transaction_action_locator).text
        amount = self.find_element(self.transaction_amount_locator).text
        description = self.find_element(self.transaction_description_locator).text
        return sender, receiver, action, amount, description
