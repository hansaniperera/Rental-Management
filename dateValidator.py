from datetime import datetime
from globals import MAX_ATTEMPTS


class DateValidator:
    def __init__(self):
        pass

    def get_booking_dates(self):
        attempts = 0

        while attempts < MAX_ATTEMPTS:
            from_date = self.get_valid_date("Enter the start date (YYYY-MM-DD): ")
            if from_date is None:
                return None, None

            to_date = self.get_valid_date("Enter the end date (YYYY-MM-DD): ")
            if to_date is None:
                return None, None

            if datetime.strptime(from_date, "%Y-%m-%d") > datetime.strptime(to_date, "%Y-%m-%d"):
                print("End date must be after the start date. Please try again.")
                attempts += 1
            else:
                return from_date, to_date

        print("Too many invalid attempts. Returning to the main menu.")
        return None, None

    def get_valid_date(self, prompt):
        attempts = 0
        while attempts < MAX_ATTEMPTS:
            date_str = input(prompt)
            try:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                if date_obj >= datetime.today():
                    return date_str
                else:
                    print("Please enter a future date.")
            except ValueError:
                print("Invalid date format. Please enter in YYYY-MM-DD format.")
            attempts += 1

        print("Too many invalid attempts. Returning to the main menu.")
        return None
