import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import (
    element_to_be_clickable,
    invisibility_of_element_located,
    presence_of_element_located,
    url_changes,
    visibility_of_element_located,
)
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def find_element(self, locator):
        try:
            return self.wait.until(visibility_of_element_located(locator))
        except TimeoutException:
            print(
                f"Element with locator {locator} was not found within timeout period of 10 seconds"
            )
            raise

    def find_element_by_id(self, id):
        return self.find_element((By.ID, id))

    def find_element_by_xpath(self, xpath):
        return self.find_element((By.XPATH, xpath))

    def find_elements(self, locator):
        try:
            return self.wait.until(presence_of_element_located(locator))
        except TimeoutException:
            print(
                f"Elements with locator {locator} were not found within timeout period of 10 seconds"
            )

    def find_elements_by_id(self, id):
        return self.find_elements((By.ID, id))

    def find_elements_by_xpath(self, xpath):
        return self.find_elements((By.XPATH, xpath))

    def click_on(self, element):
        try:
            self.wait.until(element_to_be_clickable(element)).click()
        except TimeoutException:
            print(
                f"Element {element} was not found within timeout period of 10 seconds and couldnt be clicked"
            )
            raise

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

    def check_url(self, url):
        try:
            self.wait.until(url_changes(url))
            return True
        except:
            return False

    def get_child_elements(self, parent_locator, child_locator):
        try:
            parent_element = self.find_element(parent_locator)
            return parent_element.find_elements(By.XPATH, child_locator)
        except TimeoutException:
            print(
                f"Element with locator {parent_locator} was not found within timeout period of 10 seconds"
            )

    def check_if_text_exists_in_list(self, parent_locator, text_to_be_present):
        try:
            parent_element = self.find_element(parent_locator)
            elements = parent_element.find_elements(
                By.XPATH, "//*[contains(text(), '{}')]".format(text_to_be_present)
            )
            if len(elements) > 0:
                return True
            else:
                return False
        except TimeoutException:
            print(
                f"Element with locator {parent_locator} was not found within timeout period of 10 seconds"
            )

    def wait_until_list_is_loaded_correctly(
        self, user_list_locator, child_user_list_locator, receiver_email
    ):
        """
        This code snippet defines a method that waits for a list to be loaded correctly. It expects length to be one and
        the email(or any text) appears in the list element.
        It takes in a user list locator, a child user list locator, and a receiver email as arguments. 
        It sets a maximum time of 10 seconds and iterates through the list of child elements until it finds the receiver email(it can be any text), 
        or until the iterator reaches the maximum time. If the receiver email is not found within the 
        allotted time, a TimeoutError is raised.
        """
        max_time = 10
        iterator = 0
        child_elements = self.get_child_elements(
            user_list_locator, child_user_list_locator
        )
        while not (
            len(child_elements) == 1
            and self.check_if_text_exists_in_list(user_list_locator, receiver_email)
        ):
            if iterator >= max_time:
                raise TimeoutError(f"{receiver_email} was not found in the user list")
            time.sleep(1)
            child_elements = self.get_child_elements(
                user_list_locator, child_user_list_locator
            )
            iterator += 1
