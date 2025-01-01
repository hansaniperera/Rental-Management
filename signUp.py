import script
from dbConnect import Database
from globals import MAX_ATTEMPTS
from userManagement import UserManagementService

# Manage sign up operation
class UserRegister:
    def __init__(self):
        self.db = Database()
        self.user_management_service = UserManagementService()

    def signup(self):
        user = self.user_management_service.get_user_details()
        if user is None:
            return False
        first_name, last_name, email, password, mobile_number = user

        company_code = self.__get_company_code()

        if company_code is None:
            return False

        return self.user_management_service.save_admin_customer(first_name, last_name, email, password,
                                                         mobile_number, company_code)

    # Validate company code
    def __check_company_code(self, company_code):

        code_list = self.db.fetch_all(script.CHECK_CODES, params=None)
        codes = [(row['code'], row['description']) for row in code_list]
        code_exists = any(code[0] == company_code for code in codes)

        if code_exists:
            return True
        else:
            return False

    # Screen to get company code
    def __company_code_screen(self):
        return input("If you need admin access, enter company code provided to you or select one of choice\n"
                     "\033[1m 1. Continue as a customer\n 3. Logout.\033[0m\nEnter company code: ")

    # Retry screen to get company code
    def __get_company_code(self):
        attempts = 0
        while attempts < MAX_ATTEMPTS:
            company_code = self.__company_code_screen()

            if company_code == "1" or company_code == "3":
                return company_code
            elif self.__check_company_code(company_code):
                return company_code
            else:
                print("Invalid company code. Please try again.")
                attempts += 1

        print("Too many invalid attempts. Returning to the main menu.")
        return None
