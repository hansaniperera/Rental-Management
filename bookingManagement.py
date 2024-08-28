import sqlite3
from datetime import datetime

import script
from booking import Booking
from carManagement import CarManagementService
from dateValidator import DateValidator
from dbConnect import Database
from tabulate import tabulate

from globals import MAX_ATTEMPTS
from rentalManagement import RentalManagementService
from userSession import UserSession


class BookingManagementService:
    def __init__(self):
        self.db = Database()
        self.car_management_service = CarManagementService()
        self.user_session = UserSession()
        self.date_validator = DateValidator()

    def add_booking(self, booking_data):
        try:
            self.db.execute("BEGIN TRANSACTION")
            self.db.execute(script.ADD_BOOKING, (booking_data.user_mobile,
                                                            booking_data.car_id, booking_data.from_date,
                                                            booking_data.to_date, booking_data.status,
                                                            booking_data.fees))
            current_user = self.user_session.get_current_user()
            self.update_user_loyalty(current_user["email"])
            self.db.commit()
            print(f"Booking for {booking_data.car_id} added successfully.")
        except sqlite3.Error as error:
            print(f"Failed to add booking: {error}")

    def view_bookings(self):
        try:
            bookings = self.db.fetch_all(script.GET_ALL_BOOKINGS)
            if not bookings:
                print("No bookings found.")
                return
            self.display_bookings(bookings)
        except sqlite3.Error as e:
            print(f"Failed to retrieve bookings: {e}")

    def add_booking_details(self):
        rental_management_service = RentalManagementService()
        try:
            from_date, to_date = self.car_management_service.show_available_cars_screen()
            if from_date is None or to_date is None:
                return
            car_id = self.get_car_id()
            if car_id is None:
                return
            current_user = self.user_session.get_current_user()
            user_mobile = current_user["mobile_number"]

            car_details = self.db.fetch_one(script.FETCH_CAR_DETAILS_BY_CAR_ID, (car_id,))
            if car_details:
                days = rental_management_service.calculate_days(from_date, to_date)
                fee = rental_management_service.calculate_rental_fees(days, car_details["daily_rate"])
                if fee is None:
                    print("Failed to calculate rent fee.")
                    return None
                discount = rental_management_service.calculate_discount(current_user["email"], user_mobile,
                                                                        car_details['make'], car_details['model'])
                if discount > 0:
                    fee = fee * (1 - discount / 100)
                    print(
                        f"Congratulations! You've received a {discount}% discount on your booking. Final rental fee: "
                        f"${fee:.2f}")
                booking = Booking(user_mobile, car_id, from_date, to_date, "Pending", round(fee, 2))
                self.add_booking(booking)
                return
            else:
                print(f"Failed to retrieve details of car {car_id}.")
                return None

        except sqlite3.Error as error:
            print(f"Failed to retrieve details of car: {error}")
            return None

    def get_car_id(self):
        attempts = 0
        while attempts < MAX_ATTEMPTS:
            car_id = input("Enter the car ID to book: ")
            if self.car_management_service.car_exists(car_id):
                return car_id
            print(f"Car with ID {car_id} does not exist.")
            attempts += 1

        print("Too many invalid attempts. Back to main menu.")
        return None

    def view_future_bookings(self):
        session = UserSession()
        current_user = session.get_current_user()

        if not current_user:
            print("No user is currently logged in.")
            return None

        try:
            bookings = self.db.fetch_all(script.GET_FUTURE_BOOKINGS, (current_user["mobile_number"],))
            if bookings:
                print("Here are your future bookings:")
                self.display_bookings(bookings)
                return bookings
            else:
                print("No future bookings found.")
                return None
        except sqlite3.Error as error:
            print(f"Failed to retrieve future bookings: {error}")
            return None

    def display_bookings(self, booking_data):
        headers = ["Booking ID", "User Mobile", "Car ID", "From Date", "To Date", "Status", "Fees($)"]
        print(tabulate(booking_data, headers=headers, tablefmt="fancy_grid"))

    def update_user_loyalty(self, email):
        current_date = datetime.now().strftime('%Y-%m-%d')
        self.db.execute(
            script.UPDATE_CUSTOMER_RENTAL_COUNT,
            (current_date, email)
        )










