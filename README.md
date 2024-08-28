# HSP-Rental-Management
## Overview
The Car Rental System is a Python-based CLI(Command-Line-Interface) application designed to manage a car rental service. 
This system allows adding, updating, and deleting cars, managing customer bookings, and where maintaining user roles
of Admins and Customers. The application is built with SQLite as the database, since it is lightweight and easy to 
set up as this is a simple application.

## Table of Contents
1. Installation
2. Configuration
3. Usage
4. File Structure
5. Licensing
6. Known Issues
7. Credits

## Installation

## Prerequisites
- Python 3.8 or later\ 
- SQLite (comes pre-installed with Python)\
- pip package manager\

Step 1: Clone the Repository
Clone the repository:

```
> git clone https://github.com/hansaniperera/Rental-Management.git
> cd car-rental-system
```
Step 2: Install Dependencies.

> pip install -r requirements.txt

Step 3: Set up the Database

> python setup_db.py

## Usage
Run the Application:
Execute the main script:

> python rentalApp.py
> 

## File Structure
__rentalApp.py__: The entry point of the application \
__config.py__: Contains configuration settings\
__setup_db.py__: Script to setup the database and create tables\
__dbConnect.py__: Create singleton database instance\
__script.py__: Contains SQL queries used throughout the system\
__mainMenu.py__: Contains menu page\
__userType.py__: Contains Abstract UserType class and concrete Admin and Customer classes which represent different 
user roles in the system\
__userSession.py__: Store current logged user details\
__signIn.py__: handle the sign-in operations\
__signUp.py__: handle the sign-up operations\
__rentalManagement.py__: service to manage rental related operations\
__bookingManagement.py__: service to manage booking related operations\
__carManagement.py__: service to manage car related operations\
__userManagement.py__: service to manage user related operations\
__dateValidator.py__: helper to validate dates\
__vehicleFactory.py__: Factory class to create specific vehicle\
__booking.py__: Contains the Booking details attributes\
__car.py__: Contains the car detail attributes\
__requirements.txt__: Contains Python packages required to run the system\

## Licensing
The Car Rental System is released under the MIT License. You are free to use, modify, and distribute this software 
under the terms of this license. Please verify that you retain the original license notice in any copies of the software.
See LICENSE.txt for more information.

## Known Issues
__User Authentication__: The system does not support any advanced authentication mechanisms.
user passwords stored as plain text in here. Therefore, they need to hashed \
__Error Handling__: Most user inputs are validated, but error handling could be improved \
__Payment Gateway__: Currently this system do not include an online payment gateway for payments
__User Input Limitations__: MAX_ATTEMPT global is set to limit invalid user inputs and some inputs are
 verified with case sensitivity to reduce the complexity of validations(Ex: user preference)


## Credits
This Car Rental System was developed by Hansani Perera. 
I am a passionate software engineer currently pursuing my master's degree.
If you have any queries or feedback, feel free to contact me via below email.
[Hansani Perera](mailto:270484431@yoobeestudent.ac.nz?subject=[RentalManagementSystem])
