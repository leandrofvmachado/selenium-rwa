from faker import Faker


class Transaction:
    def __init__(self, sender_id, receiver_id, amount, description, type):
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.amount = amount
        self.description = description
        self.type = type

    def to_dict(self):
        return {
            "sender_id": self.sender_id,
            "receiver_id": self.receiver_id,
            "amount": self.amount,
            "description": self.description,
            "type": self.type,
        }

    def set_type(self, type):
        self.type = type

    def set_amount(self, amount):
        self.amount = amount


class TransactionFactory:
    def __init__(self):
        self.faker = Faker()

    def create_transaction(self, type, sender_id, receiver_id):
        amount = str(self.faker.pyint(min_value=10, max_value=50))
        description = self.faker.sentence(nb_words=10)

        return Transaction(sender_id, receiver_id, amount, description, type)
