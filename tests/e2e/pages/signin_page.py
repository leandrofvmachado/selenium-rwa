import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from e2e.pages.base_page import BasePage
from e2e.pages.home_page import HomePage

class SignInPage(BasePage):
    """A class to represent the SignIn Page"""

    def __init__(self, driver):
        super().__init__(driver)

    # Locators for page elements
    username_locator = (By.ID, "username")
    password_locator = (By.ID, "password")
    login_button_locator = (By.CSS_SELECTOR, '[data-test="signin-submit"]')
    signup_button_locator = (By.CSS_SELECTOR, '[data-test="signup"]')
    signup_link_locator = (By.CSS_SELECTOR, '[data-test="signup"]')
    

    #User journey methods
    def is_in_signin_page(self):
        return self.check_url(f'{pytest.url}/signin')
    
    def go_to_signup_page(self):
        self.click_on(self.signup_link_locator)

    def login(self, username, password):
        self.find_element(self.username_locator).send_keys(username)
        self.find_element(self.password_locator).send_keys(password)
        self.find_element(self.login_button_locator).click()
        home_page = HomePage(self.driver)
        assert home_page.is_in_home_page()
        return home_page