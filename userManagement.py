import sqlite3

import script
from carManagement import CarManagementService
from dbConnect import Database
from globals import MAX_ATTEMPTS
from userType import Customer, Admin
from tabulate import tabulate
import re


class UserManagementService:
    def __init__(self):
        self.db = Database()
        self.car_management_service = CarManagementService()

    def save_admin_customer(self, first_name, last_name, email, password, mobile_number, company_code):
        if company_code == "1":
            licence_no = input("Enter License Number: ")
            address = input("Enter Address: ")
            customer = Customer(first_name, last_name, email,
                                password, mobile_number, False, address, licence_no)
            customer.save(self.db)
        elif company_code == "3":
            return False
        else:
            designation = input("Enter Designation: ")
            branch = input("Enter Branch: ")
            admin = Admin(first_name, last_name, email, password, mobile_number,
                          True, designation, branch)
            admin.save(self.db)
        return True

    def get_user_details(self):
        first_name = self.__get_valid_first_name()
        if first_name is None:
            return None
        last_name = self.__get_valid_last_name()
        if last_name is None:
            return None
        email = self.__get_valid_email()
        if email is None:
            return None
        mobile_number = self.__get_valid_mobile_number()
        if mobile_number is None:
            return None
        password = self.__get_password()
        if password is None:
            return None
        user = (first_name, last_name, email, password, mobile_number)
        return user

    def __validate_name(self, name):
        return name.isalpha() and len(name) > 1

    def __validate_email(self, email):
        return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

    def __validate_mobile_number(self, mobile_number):
        return mobile_number.isdigit() and len(mobile_number) == 10 and mobile_number[0] == '0'

    def __get_valid_mobile_number(self):
        attempts = 0
        while attempts < MAX_ATTEMPTS:
            mobile_number = input("Enter mobile number: ")
            if self.__validate_mobile_number(mobile_number):
                if not self.__mobile_exist_exists(mobile_number):
                    return mobile_number
                else:
                    print("Mobile number already exists in the database. Please enter a different mobile number.")
                    attempts += 1
            else:
                print("Invalid mobile number. Please enter a 10-digit number starting with 0.")
                attempts += 1

        print("Too many invalid attempts. Returning to the main menu.")
        return None

    def __get_valid_email(self):
        attempts = 0
        while attempts < MAX_ATTEMPTS:
            email = input("Enter email: ")
            if self.__validate_email(email):
                if not self.__email_exists(email):
                    return email
                else:
                    print("Email already exists in the database. Please enter a different email.")
                    attempts += 1
            else:
                print("Invalid email format. Please try again.")
                attempts += 1

        print("Too many invalid attempts. Returning to the main menu.")
        return None

    def __email_exists(self, email):

        self.db.execute(script.CHECK_EMAIL_EXIST, (email,))
        count = self.db.cursor.fetchone()[0]
        return count > 0

    def __get_valid_first_name(self):
        attempts = 0
        while attempts < MAX_ATTEMPTS:
            first_name = input("Enter first name: ")
            if self.__validate_name(first_name):
                return first_name
            else:
                print("Invalid first name. Please try again.")
                attempts += 1

        print("Too many invalid attempts. Returning to the main menu.")
        return None

    def __get_valid_last_name(self):
        attempts = 0
        while attempts < MAX_ATTEMPTS:
            last_name = input("Enter last name: ")
            if self.__validate_name(last_name):
                return last_name
            else:
                print("Invalid last name. Please try again.")
                attempts += 1

        print("Too many invalid attempts. Returning to the main menu.")
        return None

    def __get_password(self):
        attempts = 0
        while attempts < MAX_ATTEMPTS:
            password = self.__password_screen()
            confirm_password = self.__confirm_password_screen()

            if self.__check_password(password, confirm_password):
                return password
            else:
                print("Passwords do not match. Please try again.")
                attempts += 1

        print("Too many invalid attempts. Returning to the main menu.")
        return None

    def __password_screen(self):
        return input("Enter password: ")

    def __confirm_password_screen(self):
        return input("Confirm password: ")

    def __check_password(self, password, confirm_password):
        return confirm_password == password

    def __mobile_exist_exists(self, mobile_number):

        self.db.execute(script.CHECK_MOBILE_NO_EXIST, (mobile_number,))
        count = self.db.cursor.fetchone()[0]
        return count > 0

    def save_user_preferences(self, user_mobile):
        preferred_make = self.get_valid_make()
        if preferred_make is None:
            return None

        preferred_model = self.get_valid_model(preferred_make)
        if preferred_model is None:
            return None

        try:
            self.db.execute_and_commit(script.STORE_USER_PREFERENCES,
                                       (user_mobile, preferred_make, preferred_model))
            print("User preferences saved successfully.")
        except sqlite3.Error as error:
            print(f"Failed to save user preferences: {error}")

    def get_valid_make(self):
        makes = self.get_all_makes()
        if not makes:
            print("No available makes found.")
            return None
        formatted_makes = [[make] for make in makes]
        print("\nAvailable car makes:")
        print(tabulate(formatted_makes, headers=["Make"], tablefmt="pretty"))

        attempts = 0
        while attempts < MAX_ATTEMPTS:
            preferred_make = input("Enter your preferred car make: ")
            if preferred_make in makes:
                return preferred_make
            print("Invalid make. Please select from the available makes.")
            attempts += 1

        print("Too many invalid attempts. Returning to the main menu.")
        return None

    def get_valid_model(self, make):
        models = self.get_all_models_for_make(make)
        if not models:
            print(f"No available models found for make: {make}.")
            return None
        formatted_models = [[model] for model in models]
        print("\nAvailable car models for", make)
        print(tabulate(formatted_models, headers=["Model"], tablefmt="pretty"))

        attempts = 0
        while attempts < MAX_ATTEMPTS:
            preferred_model = input("Enter your preferred car model: ")
            if preferred_model in models:
                return preferred_model
            print("Invalid model. Please select from the available models.")
            attempts += 1

        print("Too many invalid attempts. Returning to the main menu.")
        return None

    def get_all_makes(self):
        try:
            rows = self.db.fetch_all(script.FETCH_MAKES_OF_CARS, params=None)
            return [row["make"] for row in rows]
        except sqlite3.Error as error:
            print(f"Failed to fetch car makes: {error}")
            return []

    def get_all_models_for_make(self, make):
        try:
            rows = self.db.fetch_all(script.FETCH_MODELS_OF_MAKE, (make,))
            return [row["model"] for row in rows]
        except sqlite3.Error as error:
            print(f"Failed to fetch car models: {error}")
            return []
