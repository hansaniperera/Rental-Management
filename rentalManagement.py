import sqlite3
from datetime import datetime
from tabulate import tabulate
import script
from dbConnect import Database
from globals import MAX_ATTEMPTS

# Service to manage rental operations
class RentalManagementService:
    def __init__(self):
        self.db = Database()

    # Calculate rental fee
    def calculate_rental_fees(self, days, daily_rate):
        return float(daily_rate * int(days) + float(self.__calculate_additional_charges(days)))

    # Get the number of days
    def calculate_days(self, from_date, to_date):
        date_format = "%Y-%m-%d"

        try:
            from_date_obj = datetime.strptime(from_date, date_format)
            to_date_obj = datetime.strptime(to_date, date_format)

            diff = to_date_obj - from_date_obj
            return diff.days

        except ValueError as e:
            print(f"Error in date format: {e}")
            return None

    # Calculate additional charges for rental fee
    def __calculate_additional_charges(self, days):

        if days < 5:
            return 0
        elif 5 <= days < 10:
            return 5
        elif 10 <= days < 15:
            return 15
        elif 15 <= days < 20:
            return 25
        else:
            return 35

    # Screen to accept/reject screen -Admins
    def view_accept_reject_rental_screen(self):
        bookings = self.view_pending_bookings()
        if bookings is None:
            return

        booking_id = self.__get_valid_booking_id()
        if booking_id is None:
            return

        action = self.__get_accept_or_reject_choice()
        if action is None:
            return

        self.accept_reject_booking(booking_id, action)

    # Get the choice for accept/reject
    def __get_accept_or_reject_choice(self):
        attempts = 0
        while attempts < MAX_ATTEMPTS:
            choice = (input(
                "Do you want to 'Accept' or 'Reject' this booking? (Enter A for Accept, R for Reject): ").
                      strip().upper())

            if choice == "A":
                return "Accepted"
            elif choice == "R":
                return "Rejected"
            else:
                print("Invalid input. Please enter 'A' to Accept or 'R' to Reject.")
                attempts += 1

        print("Too many invalid attempts. Returning to the main menu.")
        return None

    #  Validate booking id
    def __get_valid_booking_id(self):
        attempts = 0
        while attempts < MAX_ATTEMPTS:
            booking_id = input("\nEnter the Booking ID to process: ")

            if self.__is_valid_booking_id(booking_id):
                return booking_id
            else:
                print("Invalid Booking ID. Please try again.")
                attempts += 1

        print("Too many invalid attempts. Returning to the main menu.")
        return None

    # Check for booking id in database
    def __is_valid_booking_id(self, booking_id):
        try:
            result = self.db.fetch_one(
                script.CHECK_BOOKING_ID_EXIST, (booking_id,)
            )
            return result is not None
        except sqlite3.Error as error:
            print(f"Error while validating booking ID: {error}")
            return False

    #  Save booking status to database
    def accept_reject_booking(self, booking_id, status):
        try:
            self.db.execute_and_commit(
                script.ACCEPT_REJECT_BOOKING, (status, booking_id)
            )
            print(f"Booking {booking_id} has been {status} successfully.")
        except sqlite3.Error as error:
            print(f"Failed to accept booking: {error}")
            raise

    #  Get the pending bookings to display
    def view_pending_bookings(self):
        try:
            bookings = self.db.fetch_all(script.GET_BOOKINGS_BY_STATUS, ('Pending',))
            if bookings:
                print("Here are pending bookings:")
                self.display_bookings(bookings)
                return bookings
            else:
                print("No pending bookings found.")
                return None
        except sqlite3.Error as error:
            print(f"Failed to retrieve pending bookings: {error}")
            return None

    # Display booking details
    def display_bookings(self, booking_data):
        headers = ["Booking ID", "User Mobile", "Car ID", "From Date", "To Date", "Status", "Fees($)"]
        print(tabulate(booking_data, headers=headers, tablefmt="fancy_grid"))

    # Calculate the discount
    def calculate_discount(self, email, user_mobile, car_make, car_model):
        user = self.db.fetch_one(script.FETCH_RENTAL_COUNTS,
                                 (email,))
        discount = 0
        if int(user['rentals_count']) > 4:
            discount += 10

        preferences = self.db.fetch_one(
            script.FETCH_USER_PREFERENCE, (user_mobile,))
        if preferences and preferences['preferred_make'] == car_make and preferences['preferred_model'] == car_model:
            discount += 5

        return discount

