from faker import Faker


class BankAccount:
    def __init__(self, bank_name, routing_number, account_number):
        self.bank_name = bank_name
        self.routing_number = routing_number
        self.account_number = account_number

    def __str__(self):
        return f"{self.bank_name} account ({self.routing_number}-{self.account_number})"


class BankAccountFactory:
    def __init__(self):
        self.faker = Faker()

    def create_bank_account(self):
        bank_name = self.faker.company()
        routing_number = self.faker.random_number(digits=9)
        account_number = self.faker.random_number(digits=10)
        return BankAccount(bank_name, routing_number, account_number)

    # Mutation for creating the bank account
    create_mutation = {
        "operationName": "CreateBankAccount",
        "query": """
        mutation CreateBankAccount($bankName: String!, $accountNumber: String!, $routingNumber: String!) {
            createBankAccount(
            bankName: $bankName
            accountNumber: $accountNumber
            routingNumber: $routingNumber
            ) {
            id
            uuid
            userId
            bankName
            accountNumber
            routingNumber
            isDeleted
            createdAt
            }
        }
        """,
        "variables": {
            "userId": "test",
            "bankName": "test",
            "accountNumber": "test",
            "routingNumber": "test",
        },
    }
