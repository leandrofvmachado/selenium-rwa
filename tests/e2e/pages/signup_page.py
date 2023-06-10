import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage
from conftest import create_signup_data
from e2e.pages.signin_page import SignInPage

class SignUpPage(BasePage):
    """A class to represent the SignUp Page"""

    def __init__(self, driver):
        super().__init__(driver)

    # Locators for page elements
    first_name_locator = (By.ID, "firstName")
    last_name_locator = (By.ID, "lastName")
    username_locator = (By.ID, "username")
    password_locator = (By.ID, "password")
    confirm_password_locator = (By.ID, "confirmPassword")
    signup_button_locator = (By.CSS_SELECTOR, '[data-test="signup-submit"]')

    # Methods to perform actions
    def enter_first_name(self, first_name):
        pytest.set_trace()
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.first_name_locator)
        ).send_keys(first_name)

    def enter_last_name(self, last_name):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.last_name_locator)
        ).send_keys(last_name)

    def enter_username(self, username):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.username_locator)
        ).send_keys(username)

    def enter_password(self, password):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.password_locator)
        ).send_keys(password)

    def enter_confirm_password(self, password):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.confirm_password_locator)
        ).send_keys(password)

    def click_signup_button(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.signup_button_locator)
        ).click()

    #User journey methods
    def signup(self):
        try:
            signup_data = create_signup_data()
            self.enter_first_name(signup_data['first_name'])
            self.enter_last_name(signup_data['last_name'])
            self.enter_username(signup_data['username'])
            self.enter_password(signup_data['password'])
            self.enter_confirm_password(signup_data['password'])
            self.click_signup_button()
            sign_in_page = SignInPage(self.driver)
            assert sign_in_page.is_in_signin_page()
        except:
            self.driver.save_screenshot('ss.png')
            raise

        return signup_data, sign_in_page