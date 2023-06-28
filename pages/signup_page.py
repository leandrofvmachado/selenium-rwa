from selenium.webdriver.common.by import By

from conftest import create_signup_data
from pages.base_page import BasePage
from pages.signin_page import SignInPage


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

    # User journey methods
    def signup(self):
        signup_data = create_signup_data()
        self.find_element(self.first_name_locator).send_keys(signup_data["first_name"])
        self.find_element(self.last_name_locator).send_keys(signup_data["last_name"])
        self.find_element(self.username_locator).send_keys(signup_data["username"])
        self.find_element(self.password_locator).send_keys(signup_data["password"])
        self.find_element(self.confirm_password_locator).send_keys(
            signup_data["password"]
        )
        self.click_on(self.signup_button_locator)
        sign_in_page = SignInPage(self.driver)
        assert sign_in_page.is_in_signin_page()

        return signup_data, sign_in_page
