import os

from globals import DATABASE_NAME
from mainMenu import MainMenuDisplay
from setupDb import SetupDatabase

# Entry point of the system
class RentalApp:

    def __init__(self):
        self.main_menu = MainMenuDisplay()
        self.setup_db = SetupDatabase()

    # Start rental app
    def start_rental(self):
        database_created = not os.path.isfile(DATABASE_NAME)
        tables_initialized = self.setup_db.table_exists("users")

        if database_created:
            self.setup_db.initialize_db()
            self.setup_db.run_insert_scripts()
        elif not tables_initialized:
            self.setup_db.initialize_db()
            self.setup_db.run_insert_scripts()

        self.main_menu.display_menu()

if __name__ == "__main__":
    rentalApp = RentalApp()
    rentalApp.start_rental()
