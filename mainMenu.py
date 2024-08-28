import sys

from bookingManagement import BookingManagementService
from rentalManagement import RentalManagementService
from signUp import UserRegister
from signIn import UserLogin
from carManagement import CarManagementService
from userManagement import UserManagementService
from userSession import UserSession


class MainMenuDisplay:
    def __init__(self):
        self.car_management_service = CarManagementService()
        self.booking_management_service = BookingManagementService()
        self.user_session = UserSession()
        self.rental_management_service = RentalManagementService()
        self.user_management_service = UserManagementService()

    def display_menu(self):
        print("===============================================================================")
        print("")
        print("=============== | Welcome to HSP Car Rental Management System | ===============")
        print("")
        print("===============================================================================")
        print(""
              "Signup/Signin to continue:\n"
              "1. Sign Up\n"
              "2. Sign In\n"
              "3. Exit\n"
              "")

        login_choice = input("Enter your choice:")
        is_admin_navigate = self.login_choice(login_choice)
        if is_admin_navigate:
            self.admin_screen()
        else:
            self.customer_screen()

    def login_choice(self, login_choice):
        user_log = UserLogin()
        if login_choice == "1":
            user_reg = UserRegister()
            is_registered = user_reg.signup()
            if is_registered is True:
                print("***** Login to continue... *****")
                is_admin_navigate = user_log.sign_in()
                if is_admin_navigate is not None:
                    return is_admin_navigate
                else:
                    self.display_menu()
            else:
                self.display_menu()
        elif login_choice == "2":
            is_admin_navigate = user_log.sign_in()
            if is_admin_navigate is not None:
                return is_admin_navigate
            else:
                self.display_menu()
        elif login_choice == "3":
            print("Thank you for visiting our Car Rental Service. Goodbye!")
            self.user_session.set_current_user(None)
            sys.exit(0)
        else:
            print("Invalid choice. Please try again.")
            self.display_menu()

    def admin_screen(self):
        while True:
            print("\n***** Admin Screen - Vehicle Management *****")
            print("1. Add a vehicle")
            print("2. Update a vehicle")
            print("3. Delete a vehicle")
            print("4. Accept/Reject pending Bookings")
            print("5. View all Bookings")
            print("6. Logout")

            choice = input("Enter your choice (1-5): ")

            if choice == "1":
                self.car_management_service.add_vehicle()
            elif choice == "2":
                self.car_management_service.update_vehicle()
            elif choice == "3":
                self.car_management_service.delete_vehicle()
            elif choice == "4":
                self.rental_management_service.view_accept_reject_rental_screen()
            elif choice == "5":
                self.booking_management_service.view_bookings()
            elif choice == "6":
                print("Thank you for visiting our Car Rental Service. Goodbye!")
                self.user_session.set_current_user(None)
                self.display_menu()
            else:
                print("Invalid choice, please try again.")

    def customer_screen(self):
        current_user = self.user_session.get_current_user()
        while True:
            print("==================================================")
            print(f"\n\t Hi {current_user["first_name"]}  {current_user["last_name"]}!\n")
            print("==================================================")
            print("1. Check available cars for your desired dates")
            print("2. Book a car")
            print("3. View My Future Bookings")
            print("4. Save user preferences")
            print("5. Logout")

            choice = input("Please select an option (1-5): ")

            if choice == "1":
                self.car_management_service.show_available_cars_screen()
            elif choice == "2":
                self.booking_management_service.add_booking_details()
            elif choice == "3":
                self.booking_management_service.view_future_bookings()
            elif choice == "4":
                print("User Preference")
                self.user_management_service.save_user_preferences(current_user["mobile_number"])
            elif choice == "5":
                print("Thank you for visiting our Car Rental Service. Goodbye!")
                self.user_session.set_current_user(None)
                self.display_menu()
            else:
                print("Invalid choice. Please select an option between 1 and 5.")
