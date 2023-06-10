import pytest

from pages.signup_page import SignUpPage 

@pytest.fixture
def signup_page(driver, url):
    signup_page = SignUpPage(driver)
    signup_page.get_url(f"{url}/signup")
    return signup_page

def test_open_signup_window(signup_page):
    # pytest.set_trace()
    signup_data, signin_page = signup_page.signup()
    print(signup_data)