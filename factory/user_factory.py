from faker import Faker


class User:
    def __init__(self, first_name, last_name, username, password, id=None, balance=0.0):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = password
        self.id = id
        self.balance = balance

    def to_dict(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "username": self.username,
            "password": self.password,
            "id": self.id,
            "balance": self.balance,
        }

    def to_signup_dict(user):
        dict_user = user.to_dict()
        return {
            "firstName": dict_user["first_name"],
            "lastName": dict_user["last_name"],
            "username": dict_user["username"],
            "password": dict_user["password"],
            "confirmPassword": dict_user["password"],
        }

    def set_id(self, id):
        self.id = id

    def set_balance(self, balance):
        self.balance = balance


class UserFactory:
    users = {
        "Katharina_Bernier": User(
            "Edgar", "Johns", "Katharina_Bernier", "s3cret", "t45AiwidW", 1650.00
        ),
        "Tavares_Barrows": User(
            "Arely", "Kertzmann", "Tavares_Barrows", "s3cret", "qywYp6hS0U", 1650.00
        ),
        "Giovanna74": User(
            "Ibrahim", "Dickens", "Giovanna74", "s3cret", "24VniajY1y", 1650.00
        ),
    }

    def __init__(self):
        self.faker = Faker()

    def create_user(self):
        first_name = self.faker.first_name()
        last_name = self.faker.last_name()
        username = self.faker.user_name()
        password = self.faker.password()

        return User(first_name, last_name, username, password)
