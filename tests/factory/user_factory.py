from faker import Faker


class User:
    def __init__(self, first_name, last_name, username, password):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = password


class UserFactory:
    def __init__(self):
        self.faker = Faker()

    def get_user_data(self):
        first_name = self.faker.first_name()
        last_name = self.faker.last_name()
        username = self.faker.user_name()
        password = self.faker.password()
        confirm_password = password

        return {
            "firstName": first_name,
            "lastName": last_name,
            "username": username,
            "password": password,
            "confirmPassword": confirm_password,
        }
