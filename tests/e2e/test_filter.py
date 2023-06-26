from pages.home_page import home_page


def test_date_filter(home_page, logged_in_user, user, request_payment):
    home_page.set_today_date()
    (
        amount_requested,
        description_requested,
        receiver_id_requested,
        sender_id_requested,
    ) = request_payment
    (
        sender_on_screen,
        receiver_on_screen,
        action_on_screen,
        amount_on_screen,
    ) = home_page.get_transaction_info_on_personal_list()

    assert action_on_screen == "requested"
    assert amount_on_screen == f"+${amount_requested}.00"
