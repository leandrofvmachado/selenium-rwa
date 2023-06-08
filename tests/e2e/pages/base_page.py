from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import (
    element_to_be_clickable,
    invisibility_of_element_located,
    presence_of_element_located,
    visibility_of_element_located,
)
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def find_element(self, locator):
        return self.wait.until(visibility_of_element_located(locator))

    def find_element_by_id(self, id):
        return self.find_element((By.ID, id))

    def find_element_by_xpath(self, xpath):
        return self.find_element((By.XPATH, xpath))

    def find_elements(self, locator):
        return self.wait.until(presence_of_element_located(locator))

    def find_elements_by_id(self, id):
        return self.find_elements((By.ID, id))

    def find_elements_by_xpath(self, xpath):
        return self.find_elements((By.XPATH, xpath))

    def click_on(self, element):
        return self.wait.until(element_to_be_clickable(element)).click()

    def is_visible(self, locator):
        try:
            self.wait.until(visibility_of_element_located(locator))
            return True
        except:
            return False

    def is_not_visible(self, locator):
        try:
            self.wait.until(invisibility_of_element_located(locator))
            return True
        except:
            return False

    def get_url(self, url):
        self.driver.get(url)
