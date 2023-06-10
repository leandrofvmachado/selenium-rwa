from selenium.webdriver.common.by import By

from e2e.pages.base_page import BasePage

class HomePage(BasePage):
    """A class to represent the Home Page"""

    def __init__(self, driver):
        super().__init__(driver)

    # Locators for page elements
    title_locator = (By.CSS_SELECTOR, '[data-test="app-name-logo"]')

    #User journey methods
    def is_in_home_page(self):
        if self.find_element(self.title_locator):
            return True
        else:
            return False
        

