import sqlite3
import script
from user import User
from dbConnect import Database


class UserRegister:
    def __init__(self):
        self.db = Database()

    def signup(self):
        first_name = input("Enter first name: ")
        last_name = input("Enter last name: ")
        email = input("Enter email: ")
        mobile_number = input("Enter mobile number: ")
        password = input("Enter password: ")
        confirm_password = input("Confirm password: ")
        is_true = self._check_password(password, confirm_password)

        if is_true:
            company_code = input("If you need admin access, enter company code provided to you or "
                                 "\033[1mPress 1 to continue as a customer.\033[0m\nEnter company code: ")

            if company_code == "1":
                print('save user')
                user = User(first_name, last_name, email, password, mobile_number, False)
                self.save_user(user)
            else:
                self.check_company_code(company_code)
                print('save user')
                user = User(first_name, last_name, email, password, mobile_number, True)
                self.save_user(user)
        else:
            print("Re-enter passwords")

    def check_company_code(self, company_code):
        codes = open("companyCode.txt", "r")
        data = codes.read()
        code_list = data.replace('\n', '').split(",")

        is_admin = company_code in code_list
        if is_admin:
            return True
        else:
            self.__try_screen()

        codes.close()

    def __try_screen(self):
        print("Invalid Company Code. Select an options to continue...\n")
        print(""
              "1. Try again\n"
              "2. Sign in as a customer\n"
              "3. Exit\n"
              "")

    def _check_password(self, password, confirm_password):
        if confirm_password == password:
            return True
        else:
            print("Passwords do not match\n")
            return False

    def save_user(self, user):
        try:
            self.db.execute(script.ADD_USER, (user.first_name, user.last_name, user.email,
                                              user.password, user.mobile_number, user.is_admin))
            print("Saved successfully")
        except sqlite3.Error as e:
            print(f"user save error: {e}")
