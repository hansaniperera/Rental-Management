import sys, os
from signUp import UserRegister
from signIn import UserLogin


class MainMenuDisplay:
    def __init__(self):
        pass

    def display_menu(self):
        print("=============== | Welcome to Car Rental Management System | ===============")
        print("")
        print(""
              "Signup/Signin to continue:\n"
              "1. Sign Up\n"
              "2. Sign In\n"
              "3. Exit\n"
              "")

        login_choice = input("Enter your choice:")
        self.login_choice(login_choice)

    def login_choice(self, login_choice):
        if login_choice == "1":
            user_reg = UserRegister()
            user_reg.signup()
        elif login_choice == "2":
            user_log = UserLogin()
            user_log.sign_in()
        elif login_choice == "3":
            print("Thank you for using Car Rental Management System")
            sys.exit(0)
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Invalid choice. Please try again.")
            self.display_menu()
