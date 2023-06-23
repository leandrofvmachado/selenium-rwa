import json

import requests
from factory.bank_account import BankAccountFactory

base_url = "http://localhost:3001"


def make_request(session, url, payload, request_type):
    if request_type == "GET":
        response = session.get(url, params=payload)
    elif request_type == "POST":
        if url.endswith("/graphql"):
            response = session.post(
                url, headers={"Content-Type": "application/json"}, data=payload
            )
        else:
            response = session.post(url, data=payload)
    elif request_type == "PUT":
        response = session.put(url, data=payload)
    elif request_type == "DELETE":
        response = session.delete(url)
    elif request_type == "PATCH":
        response = session.patch(url, data=payload)
    else:
        raise ValueError(f"Unsupported request type: {request_type}")

    if not response.ok:
        raise ValueError(
            f"Request failed with status code {response.status_code}: {response.text}"
        )

    return response


def login(username, password):
    session = requests.Session()
    login_payload = {
        "type": "LOGIN",
        "username": username,
        "password": password,
    }

    response = make_request(session, f"{base_url}/login", login_payload, "POST")
    return session


def logout(session):
    logout_payload = {
        "type": "LOGOUT",
    }

    response = make_request(session, f"{base_url}/logout", logout_payload, "POST")
    return response.json()


def make_new_transaction(
    session, amount, transaction_type, note, receiver_id, sender_id
):
    new_transaction_payload = {
        "amount": amount,
        "transactionType": transaction_type,
        "description": note,
        "receiverId": receiver_id,
        "senderId": sender_id,
    }

    response = make_request(
        session, f"{base_url}/transactions", new_transaction_payload, "POST"
    )
    return response.json()


def execute_transaction(session, request_status, transaction_id):
    execute_transaction_payload = {
        "requestStatus": request_status,
        "id": transaction_id,
    }
    make_request(
        session,
        f"{base_url}/transactions/{transaction_id}",
        execute_transaction_payload,
        "PATCH",
    )


def create_new_bank_account(session, user_id):
    factory = BankAccountFactory()
    bank_account = factory.create_bank_account()
    mutation = factory.create_mutation.copy()
    mutation["variables"]["bankName"] = bank_account.bank_name
    mutation["variables"]["userId"] = user_id
    mutation["variables"]["routingNumber"] = str(bank_account.routing_number)
    mutation["variables"]["accountNumber"] = str(bank_account.account_number)
    make_request(session, f"{base_url}/graphql", json.dumps(mutation), "POST")

    return bank_account
