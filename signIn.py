from dbConnect import Database


class UserLogin:
    def __init__(self):
        self.db = Database()

    def sign_in(self):
        email = input("Enter email: ")
        password = input("Enter password: ")

