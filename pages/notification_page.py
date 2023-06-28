import pytest
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


@pytest.fixture
def notification_page(driver):
    notification_page = NotificationPage(driver)
    return notification_page


class NotificationPage(BasePage):
    """A class to represent the Notification Page"""

    def __init__(self, driver):
        super().__init__(driver)

    # Locators for page elements
    notifications_list_locator = (By.CSS_SELECTOR, '[data-test="notifications-list"]')
    notifications_list_empty_locator = (
        By.CSS_SELECTOR,
        '[data-test="empty-list-header"]',
    )
    notifications_list_item_locator = (
        By.XPATH,
        '//*[starts-with(@data-test, "notification-list-item")]',
    )
    notifications_list_item_button_locator = (
        By.XPATH,
        '//*[starts-with(@data-test, "notification-mark-read-")]',
    )

    # User journey methods
    def is_in_notifications_page(self):
        if self.check_url(pytest.url + "notifications"):
            return True
        else:
            return False

    def dismiss_last_notification(self):
        self.find_element(self.notifications_list_item_button_locator).click()

    def is_notification_list_empty(self):
        return self.find_element(self.notifications_list_empty_locator)
