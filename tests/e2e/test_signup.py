import pytest

from pages.signup_page import SignUpPage 

@pytest.fixture
def signup_page(driver):
    signup_page = SignUpPage(driver)
    signup_page.get_url(f"{pytest.url}/signup")
    return signup_page

def test_open_signup_window(signup_page):
    signup_data, signin_page = signup_page.signup()
    assert signin_page.is_in_signin_page()
    assert signin_page.login(signup_data['username'], signup_data['password'])