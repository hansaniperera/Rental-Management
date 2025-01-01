# HSP-Rental-Management
## Overview
The Car Rental System is a Python-based CLI(Command-Line-Interface) application designed to manage a car rental service. 
This system allows adding, updating, and deleting cars, managing customer bookings, and where maintaining user roles
of Admins and Customers. This also includes an innovative feature to calculate rental fee discount based on rental 
counts and user preference.The application is built with SQLite as the database, since it is lightweight and easy to 
set up as this is a simple application.

### Note: Initial Cars and Company_Codes added to database when initializing
(Company code : XYZ, BCD, ABC) - No functionality to add this from app to keep the security.

## Table of Contents
1. Installation
2. Configuration
3. Usage
4. File Structure
5. Project Structure
6. Licensing
7. Known Issues
8.Credits

## Installation

## Prerequisites
- Python 3.8 or later\ 
- SQLite (comes pre-installed with Python)\
- pip package manager\

Step 1: Clone the Repository
Clone the repository:

```
> https://github.com/hansaniperera/Rental-Management.git
> cd Rental-Management
```
Step 2: Install Dependencies.

> pip install -r requirements.txt

## Usage
Run the Application:
Execute the main script:

> python main.py
> 

## File Structure
__rentalApp.py__: The entry point of the application \
__setupDb.py__: Script to setup the database and create tables and initial insert scripts if needed\
__dbConnect.py__: Create singleton database instance\
__script.py__: Contains SQL queries used in the the system\
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

## Project Structure

__User Sign-up__: Users can sign up for the rental application here as a Customer or Admin\
__User Sign-In__: All the registered users can sign in to the application and with specific role they will be 
directed to Admin Screen or Customer Screen\
__Admin Screen__: Admins have the following operations
- Add a vehicle
- Update a vehicle
- Delete a vehicle
- Accept/Reject pending Bookings
- View all Bookings
- Logout

__Customer Screen__: Customers have the following operations
- Check available cars for desired dates
- Book a car
- View Future Bookings
- Save user preferences
- Logout

## Licensing
The Car Rental System is released under the MIT License. You are free to use, modify, and distribute this software 
under the terms of this license. Please verify that you retain the original license notice in any copies of the software.
See LICENSE.txt for more information.

## Known Issues
__User Authentication__: The system does not support any advanced authentication mechanisms.
user passwords stored as plain text in here. Therefore, they need to hashed \
__Error Handling__: Most user inputs are validated, but error handling could be improved \
__Payment Gateway__: Currently this system do not include an online payment gateway for payments\
__User Input Limitations__: MAX_ATTEMPT global is set to limit invalid user inputs and some inputs are
 verified with case sensitivity to reduce the complexity of validations(Ex: user preference)\
__IDE Compatibility__: It seems PyCharm IDE sometimes doesn't support some time. Better to use Terminal or 
Command Prompt


## Credits
This Car Rental System was developed by Hansani Perera. 
I am a passionate software engineer currently pursuing my master's degree.
If you have any queries or feedback, feel free to contact me via below email.
[Hansani Perera](mailto:270484431@yoobeestudent.ac.nz?subject=[RentalManagementSystem])
