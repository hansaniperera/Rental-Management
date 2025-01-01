from dbConnect import Database
import sqlite3
import script
from globals import MAX_ATTEMPTS
from userSession import UserSession

# Manage sign in operations
class UserLogin:
    def __init__(self):
        self.db = Database()

    def sign_in(self):
        attempts = 0
        while attempts < MAX_ATTEMPTS:
            email = input("Enter email: ")
            password = input("Enter password: ")

            admin = self.verify_user_details(email, password)
            if admin == 1:
                return True
            elif admin == 0:
                return False
            else:
                attempts += 1

        print("Too many failed login attempts. Returning to the main menu.")
        return None

    # Validate user details
    def verify_user_details(self, email, password):
        try:
            user = self.db.fetch_one(script.GET_USER, (email, password))

            if user:
                session = UserSession()
                session.set_current_user(user)
                return int(user['is_admin'])
            else:
                print("Incorrect email/password. Please sign in again.")
                return None

        except sqlite3.Error as error:
            print(f"Error while executing get user : {error}")
            raise