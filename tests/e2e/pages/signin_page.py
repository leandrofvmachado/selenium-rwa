from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from e2e.pages.base_page import BasePage

class SignInPage(BasePage):
    """A class to represent the SignIn Page"""

    def __init__(self, driver):
        super().__init__(driver)

    # Locators for page elements
    username_locator = (By.ID, "username")
    password_locator = (By.ID, "password")
    login_button_locator = (By.CSS_SELECTOR, '[data-tes="signin-submit"]')
    signup_button_locator = (By.CSS_SELECTOR, '[data-test="signup"]')
    

    # Methods to perform actions
    def enter_username(self, username):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.username_locator)
        ).send_keys(username)

    def enter_password(self, password):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.password_locator)
        ).send_keys(password)

    def click_login_button(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.login_button_locator)
        ).click()

    def is_in_signin_page(self):
        self.check_url('http://172.23.80.1:3000/signin')
        
    #User journey methods
    # def go_to_signup_page(self):
    #     WebDriverWait(self.driver, 10).until(
    #         EC.url_changes(driver.current_url)
    #     )

    def login(self, username, password):
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()
        assert 1 == 1