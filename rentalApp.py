from dbConnect import Database
from mainMenu import MainMenuDisplay


class RentalApp:

    def __init__(self):
        pass

    def start_rental(self):
        cursor = Database()
        cursor1 = Database()
        print(cursor, cursor1)

        main_menu = MainMenuDisplay()
        main_menu.display_menu()


rentalApp = RentalApp()
rentalApp.start_rental()
