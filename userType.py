import sqlite3
from abc import ABC, abstractmethod
import script

# Abstract class to define user
class UserType(ABC):
    def __init__(self, first_name, last_name, email, password, mobile_number, is_admin):
        self.__first_name = first_name
        self.__last_name = last_name
        self.__email = email
        self.__password = password
        self.__mobile_number = mobile_number
        self.__is_admin = is_admin

    @property
    def first_name(self):
        return self.__first_name

    @first_name.setter
    def first_name(self, first_name):
        self.__first_name = first_name

    @property
    def last_name(self):
        return self.__last_name

    @last_name.setter
    def last_name(self, last_name):
        self.__last_name = last_name

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, email):
        self.__email = email

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, password):
        self.__password = password

    @property
    def mobile_number(self):
        return self.__mobile_number

    @mobile_number.setter
    def mobile_number(self, mobile_number):
        self.__mobile_number = mobile_number

    @property
    def is_admin(self):
        return self.__is_admin

    @is_admin.setter
    def is_admin(self, is_admin):
        self.__is_admin = is_admin

    def save_user_details(self, db):
        try:
            db.execute(
                script.ADD_USER,
                (self.first_name, self.last_name, self.email, self.password, self.mobile_number, self.is_admin)
            )
        except sqlite3.Error as e:
            raise Exception(f"Error saving user details: {e}")

    @abstractmethod
    def save(self, db):
        pass

# Concrete class for admin
class Admin(UserType):
    def __init__(self, first_name, last_name, email, password, mobile_number, is_admin, designation, branch):
        super().__init__(first_name, last_name, email, password, mobile_number, is_admin)
        self.__designation = designation
        self.__branch = branch

    def save(self, db):
        try:
            # Start transaction
            db.execute("BEGIN TRANSACTION")
            self.save_user_details(db)
            db.execute(
                script.ADD_ADMIN,
                (self.email, self.__designation, self.__branch)
            )
            db.commit()
            print("Admin details saved")
        except sqlite3.Error as e:
            db.rollback()
            print(f"Transaction failed: {e}")
            raise

    @property
    def designation(self):
        return self.__designation

    @designation.setter
    def designation(self, value):
        self.__designation = value

    @property
    def branch(self):
        return self.__branch

    @branch.setter
    def branch(self, value):
        self.__branch = value

# Concrete class for customer
class Customer(UserType):
    def __init__(self, first_name, last_name, email, password, mobile_number, is_admin, address, license_no):
        super().__init__(first_name, last_name, email, password, mobile_number, is_admin)
        self.__address = address
        self.__license_no = license_no

    def save(self, db):
        try:
            db.execute("BEGIN TRANSACTION")
            self.save_user_details(db)
            db.execute(
                script.ADD_CUSTOMER,
                (self.email, self.__address, self.__license_no)
            )
            db.commit()
            print("Customer details saved")
        except sqlite3.Error as e:
            db.rollback()
            print(f"Transaction failed: {e}")
            raise

    @property
    def address(self):
        return self.__address

    @address.setter
    def address(self, value):
        self.__address = value

    @property
    def license_no(self):
        return self.__license_no

    @license_no.setter
    def license_no(self, value):
        self.__license_no = value
