import sqlite3
from tabulate import tabulate
import script
from car import Car
from dateValidator import DateValidator
from dbConnect import Database
from datetime import datetime
from globals import MAX_ATTEMPTS
from rentalManagement import RentalManagementService
from vehicleFactory import CarFactory

#  Service to manage operations related to car
class CarManagementService:
    def __init__(self):
        self.db = Database()
        self.date_validator = DateValidator()
        self.rental_management_service = RentalManagementService()

    # Add a car to the database
    def add_car(self, car):

        try:
            self.db.execute_and_commit(script.ADD_CAR_QUERY, (
                car.car_id, car.make, car.mileage, car.model, car.year,
                car.available_now, car.min_rent_period, car.max_rent_period, car.daily_rate
            ))
        except sqlite3.Error as error:
            print(f"Failed to add car: {error}")
            raise

    # Delete a car from the database
    def delete_car(self, car_id):
        try:
            self.db.execute_and_commit(script.DELETE_CAR_QUERY, (car_id,))
        except sqlite3.Error as error:
            print(f"Failed to delete car: {error}")
            raise

    # Screen to add car
    def add_vehicle(self):
        car_id = self.get_valid_car_id()
        if car_id is None:
            return
        make = input("Enter car make: ")
        mileage = self.get_valid_mileage("Enter car mileage: ")
        if mileage is None:
            return
        model = input("Enter car model: ")
        year = self.get_valid_year("Enter car year: ")
        if year is None:
            return
        available_now = self.get_valid_availability("Is the car available now (Y/N)? ")
        if available_now is None:
            return

        result = self.check_rent_range()
        if result is None:
            return
        min_rent_period, max_rent_period = result

        daily_rate = self.get_valid_daily_rate("Enter daily rate($): ")
        if daily_rate is None:
            return
        factory = CarFactory()
        car = factory.create_vehicle(car_id, make, mileage, model, year, available_now, min_rent_period,
                                     max_rent_period, daily_rate)
        self.add_car(car)
        print(f"Car with {car_id} added successfully.")

    # Initiate update car details
    def update_vehicle(self):
        self.view_all_cars()
        car_id = self.get_update_car()
        if not car_id:
            return

        update_data = self.get_update_data(car_id)
        if update_data is not None and update_data["value"] is not None:
            self.save_update(car_id, update_data)
        else:
            return

    # Screen to get car Id to update
    def get_update_car(self):
        attempts = 0
        while attempts < MAX_ATTEMPTS:
            car_id = input("\nEnter the car ID to update: ")
            if self.car_exists(car_id):
                return car_id
            print(f"Car with ID {car_id} does not exist. Please try again.")
            attempts += 1

        print("Too many invalid attempts. Back to main menu.")
        return None

    # Create table to display cars
    def display_cars(self, cars):
        headers = ["ID", "Make", "Model", "Year", "Mileage", "Available Now", "Min Rent Period(days)",
                   "Max Rent Period(days)", "Daily Rate($)"]
        table_data = [
            [car.car_id, car.make, car.model, car.year, car.mileage, car.available_now, car.min_rent_period,
             car.max_rent_period, car.daily_rate] for
            car in cars]
        print(tabulate(table_data, headers=headers, tablefmt="grid"))

    # Screen to get the update choice of a car
    def get_update_choice(self):
        print("\nWhich detail would you like to update?")
        print("1. Make")
        print("2. Mileage")
        print("3. Model")
        print("4. Year")
        print("5. Availability (Y/N)")
        print("6. Minimum Rent Period")
        print("7. Maximum Rent Period")
        print("8. Daily Rate")
        return input("Enter the number of the detail you want to update: ")

    # Save update of car detail to database
    def save_update(self, car_id, update_data):
        try:
            self.update_car_column(car_id, update_data["column"], update_data["value"])
            print(f"Car with {car_id} updated successfully.")
        except Exception as e:
            print(f"Failed to update vehicle: {e}")
            raise

    # Fetch all cars from database
    def get_all_cars(self):
        try:
            rows = self.db.fetch_all(script.FETCH_ALL_CARS, params=None)
            cars = [Car(*row) for row in rows]
            return cars
        except sqlite3.Error as error:
            print(f"Error while fetching cars: {error}")
            return []

    #  Update column n value of the car
    def update_car_column(self, car_id, column, value):
        query = f"UPDATE cars SET {column} = ? WHERE car_id = ?"

        try:
            self.db.execute_and_commit(query, (value, car_id))
        except sqlite3.Error as error:
            print(f"Failed to update {column}: {error}")
            raise

    #  Screen to delete a car
    def delete_vehicle(self):
        attempts = 0
        cars = self.get_all_cars()
        if not cars:
            print("No car found in the database.")
            return

        print("All Cars in the database:")
        self.display_cars(cars)
        while attempts < MAX_ATTEMPTS:
            car_id = input("Enter the car ID to delete: ")

            if self.car_exists(car_id):
                self.delete_car(car_id)
                print(f"Car with {car_id} deleted successfully.")
                return
            else:
                print(f"Car with ID {car_id} does not exist.")
                attempts += 1

        print("Too many invalid attempts. Returning to the main menu.")
        return

    # Check whether car exist by car id
    def car_exists(self, car_id):
        try:
            result = self.db.fetch_one(script.CHECK_CAR_EXIST, (car_id,))
            if result is None:
                return False
            return result[0] > 0
        except sqlite3.Error as error:
            print(f"Error while checking if car exists: {error}")
            return False

    # Screen to get valid availability input
    def get_valid_availability(self, prompt):
        attempts = 0
        while attempts < MAX_ATTEMPTS:
            availability = input(prompt).upper()
            if availability in ['Y', 'N']:
                return availability
            print("Invalid input. Please enter 'Y' or 'N'.")
            attempts += 1

        print("Too many invalid attempts. Returning to the main menu.")
        return None

    # Screen to get valid car id
    def get_valid_car_id(self):
        attempts = 0
        while attempts < MAX_ATTEMPTS:
            car_id = input("Enter car ID: ")
            if not self.car_exists(car_id):
                return car_id
            print(f"Car with ID {car_id} already exists. Please enter a different ID.")
            attempts += 1

        print("Too many invalid attempts. Returning to the main menu.")
        return None

    # Get user choice for update car
    def get_field_and_choice(self):
        update_choice = self.get_update_choice()
        update_fields = {
            "1": ("make", "Enter new make: "),
            "2": ("mileage", "Enter new mileage: "),
            "3": ("model", "Enter new model: "),
            "4": ("year", "Enter new year: "),
            "5": ("available_now", "Is the car available now (Y/N)? "),
            "6": ("min_rent_period", "Enter new minimum rent period (Days): "),
            "7": ("max_rent_period", "Enter new maximum rent period (Days): "),
            "8": ("daily_rate", "Enter new daily rate: ")
        }
        return update_choice, update_fields

    # Get update choice and validations
    def get_update_data(self, car_id):
        attempts = 0
        while attempts < MAX_ATTEMPTS:
            update_choice, update_fields = self.get_field_and_choice()
            if update_choice in update_fields:
                column, prompt = update_fields[update_choice]

                if update_choice == "5":
                    value = self.get_valid_availability(prompt)
                elif update_choice == "2":
                    value = self.get_valid_mileage(prompt)
                elif update_choice == "4":
                    value = self.get_valid_year(prompt)
                elif update_choice == "6" or update_choice == "7":
                    value = self.get_valid_rent(prompt)
                elif update_choice == "8":
                    value = self.get_valid_daily_rate(prompt)
                else:
                    value = input(prompt)

                if value is None:
                    print("Invalid input. Please try again.")
                    attempts += 1
                    continue

                if update_choice == "6":
                    is_validated, min_rent_period = self.validate_min_rent_period(car_id, value)
                    if is_validated is False:
                        return None
                    value = min_rent_period
                elif update_choice == "7":
                    is_validated, max_rent_period = self.validate_max_rent_period(car_id, value)
                    if is_validated is False:
                        return None
                    value = max_rent_period

                return {"column": column, "value": value}
            else:
                print("Invalid choice. Please enter a number between 1 and 8.")
                attempts += 1

        print("Too many invalid attempts. Returning to the main menu.")
        return None

    # Screen to get valid year
    def get_valid_year(self, prompt):
        current_year = datetime.now().year
        attempts = 0
        while attempts < MAX_ATTEMPTS:
            year = input(prompt)
            if year.isdigit() and 1900 <= int(year) <= current_year:
                return year
            print(f"Invalid year. Please enter a year between 1900 and {current_year}.")
            attempts += 1

        print("Too many invalid attempts. Returning to the main menu.")
        return None

    # Screen to get valid rent
    def get_valid_rent(self, prompt):
        attempts = 0
        while attempts < MAX_ATTEMPTS:
            rent = input(prompt)
            if rent.isdigit() and int(rent) > 0:
                return int(rent)

            if rent.replace('.', '', 1).isdigit():
                print("Invalid rent period. Please enter a whole number.")
            else:
                print("Invalid rent period. Please enter a valid period.")
            attempts += 1

        print("Too many invalid attempts. Returning to the main menu.")
        return None

    # Screen to get valid mileage
    def get_valid_mileage(self, prompt):
        attempts = 0
        while attempts < MAX_ATTEMPTS:
            mileage = input(prompt)
            if mileage.replace('.', '', 1).isdigit() and float(mileage) >= 0:
                return mileage
            print("Invalid mileage. Please enter a valid mileage.")
            attempts += 1

        print("Too many invalid attempts. Returning to the main menu.")
        return None

    # Validate rent range
    def check_rent_range(self):
        attempts = 0
        while attempts < MAX_ATTEMPTS:
            min_rent_period = self.get_valid_rent("Enter minimum rent period(Days): ")
            if min_rent_period is None:
                return None

            max_rent_period = self.get_valid_rent("Enter maximum rent period(Days): ")
            if max_rent_period is None:
                return None

            if int(min_rent_period) < int(max_rent_period):
                return min_rent_period, max_rent_period
            print(f"Maximum rent period ({max_rent_period} days) must be greater than minimum rent "
                  f"period ({min_rent_period} days).")
            attempts += 1

        print("Too many invalid attempts. Returning to the main menu.")
        return None

    # Validate maximum rent period
    def validate_max_rent_period(self, car_id, max_rent_period):
        attempts = 0

        while attempts < MAX_ATTEMPTS:
            try:
                current_min_rent_period, current_max_rent_period  = self.get_min_max_rent_period(car_id)
                if current_max_rent_period is None or current_min_rent_period is None:
                    return False, None

                if int(max_rent_period) > int(current_min_rent_period):
                    return True, max_rent_period
                else:
                    print(f"Maximum rent period ({max_rent_period} days) must be greater than minimum rent period "
                          f"({current_min_rent_period} days).")
                    attempts += 1
                    max_rent_period = self.get_valid_rent("Enter new maximum rent period(Days): ")
                    if max_rent_period is None:
                        return False, None

            except sqlite3.Error as error:
                print(f"Error while validating rent range: {error}")
                raise

        print("Too many invalid attempts. Returning to the main menu.")
        return False, None

    # Validate minimum rent period
    def validate_min_rent_period(self, car_id, min_rent_period):
        attempts = 0

        while attempts < MAX_ATTEMPTS:
            try:
                current_min_rent_period, current_max_rent_period = self.get_min_max_rent_period(car_id)
                if current_min_rent_period is None or current_max_rent_period is None:
                    return False, None
                if int(min_rent_period) > int(current_max_rent_period):
                    print(f"Minimum rent period ({min_rent_period} days) must be less than maximum rent period "
                          f"({current_max_rent_period} days).")
                    min_rent_period = self.get_valid_rent("Enter a new minimum rent period(Days): ")
                    if min_rent_period is None:
                        return False, None
                else:
                    return True, min_rent_period
            except sqlite3.Error as error:
                print(f"Error while validating rent range: {error}")
                raise

            attempts += 1

        print("Too many invalid attempts. Returning to the main menu.")
        return False, None

    # Get Min and Max rent period of a car
    def get_min_max_rent_period(self, car_id):
        car_details = self.db.fetch_one(
            script.FETCH_CAR_DETAILS_BY_CAR_ID, (car_id,)
        )
        if car_details["min_rent_period"] is None or car_details["max_rent_period"] is None:
            return None, None
        return (car_details["min_rent_period"],
                car_details["max_rent_period"])

    # Screen to show available cars
    def show_available_cars_screen(self):
        from_date, to_date = self.date_validator.get_booking_dates()
        if from_date is None or to_date is None:
            return None, None
        days = self.rental_management_service.calculate_days(from_date, to_date)
        cars = self.get_available_cars(from_date, to_date, int(days))
        if not cars:
            print("No available cars found in the database.")
            return None, None
        print("Available cars:")
        self.display_cars(cars)
        return from_date, to_date

    # Get available cars
    def get_available_cars(self, new_from_date, new_to_date, days):
        try:
            rows = self.db.fetch_all(script.FETCH_AVAILABLE_CARS_FOR_DATES, (new_to_date, new_from_date,
                                                                             new_from_date, new_to_date, new_from_date,
                                                                             new_to_date, new_from_date, new_to_date,
                                                                             days, days))
            cars = [Car(*row) for row in rows]
            return cars
        except sqlite3.Error as error:
            print(f"Error while fetching cars: {error}")
            return []

    # Validate daily rate
    def get_valid_daily_rate(self, prompt):
        attempts = 0
        while attempts < MAX_ATTEMPTS:
            rate = input(prompt)
            if rate.replace('.', '', 1).isdigit() and float(rate) > 0:
                return rate
            print("Invalid daily rate. Please enter a valid rate.")
            attempts += 1

        print("Too many invalid attempts. Returning to the main menu.")
        return None

    def view_all_cars(self):
        cars = self.get_all_cars()
        if not cars:
            print("No car found in the database.")
            return

        print("All Cars in the database:")
        self.display_cars(cars)

