from mainMenu import MainMenuDisplay
from setupDb import SetupDatabase

class RentalApp:

    def __init__(self):
        self.main_menu = MainMenuDisplay()
        self.setup_db = SetupDatabase()

    def start_rental(self):
        self.setup_db.initialize_db()
        self.setup_db.run_insert_scripts()
        self.main_menu.display_menu()

if __name__ == "__main__":
    rentalApp = RentalApp()
    rentalApp.start_rental()
