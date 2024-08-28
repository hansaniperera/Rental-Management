ADD_USER = ("INSERT INTO users(first_name, last_name, email, password, mobile_number, is_admin)"
            " VALUES (?,?,?,?,?,?)")

ADD_CUSTOMER = ("INSERT INTO customers(email, address, license_number, rental_count)"
                " VALUES (?,?,?,0)")

ADD_ADMIN = ("INSERT INTO admins(email, designation, branch)"
             " VALUES (?,?,?)")

STORE_USER_PREFERENCES = ("INSERT OR REPLACE INTO user_preferences(user_mobile, preferred_make, "
                          "preferred_model) VALUES (?, ?, ?)")

GET_USER = ("SELECT u.* FROM users AS u WHERE u.email=? and u.password=?")

CHECK_EMAIL_EXIST =  ("SELECT COUNT(*) FROM users WHERE email = ?")

CHECK_MOBILE_NO_EXIST = ("SELECT COUNT(*) FROM users WHERE mobile_number = ?")

CHECK_CODES = ("SELECT * FROM company_codes")

# Cars
# SQL query to add a new car
ADD_CAR_QUERY = ("\n"
                 "INSERT INTO cars (car_id, make, mileage, model, year, available_now, min_rent_period, "
                 "max_rent_period, daily_rate)\n"
                 "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)\n")


# SQL query to delete a car by its car_id
DELETE_CAR_QUERY = ("\n"
                    "DELETE FROM cars WHERE car_id = ?\n")

FETCH_ALL_CARS = (
    "SELECT car_id, make, mileage, model, year, available_now, min_rent_period, max_rent_period, daily_rate "
    " FROM cars")

CHECK_CAR_EXIST = ("SELECT COUNT(1) FROM cars WHERE car_id = ?")

FETCH_AVAILABLE_CARS_FOR_DATES = (
    "SELECT car_id, make, mileage, model, year, available_now, min_rent_period, max_rent_period, daily_rate "
    "FROM cars "
    "WHERE car_id NOT IN ("
    "   SELECT car_id FROM bookings "
    "   WHERE ( status != 'Rejected' and (  "
          "(from_date <= ? AND to_date >= ?) OR "
          "(from_date <= ? AND to_date >= ?) OR "
          "(from_date >= ? AND to_date <= ?) OR "
          "(from_date <= ? AND to_date >= ?)) "
      ")) and available_now = 'Y' and max_rent_period >= ? and "
                               "min_rent_period <= ? "
)

FETCH_CAR_DETAILS_BY_CAR_ID = ("SELECT car_id, make, mileage, model, year, available_now, min_rent_period, "
                               "max_rent_period, daily_rate FROM cars WHERE car_id = ?")

GET_USER_PREFERENCES = ("SELECT preferred_make, preferred_model, preferred_year, preferred_mileage"
    " FROM user_preferences WHERE user_mobile = ?")

RECOMMENDED_CARS = ("SELECT car_id, make, mileage, model, year, available_now, min_rent_period, max_rent_period, "
                    "daily_rate")

FETCH_MAKES_OF_CARS = ("SELECT DISTINCT make FROM cars")

FETCH_MODELS_OF_MAKE = ("SELECT DISTINCT model FROM cars WHERE make = ?")
#
# Booking

# SQL queries related to bookings
ADD_BOOKING = ("\n"
               "INSERT INTO bookings (user_mobile, car_id, from_date, to_date, status, fee)\n"
               "VALUES (?, ?, ?, ?, ?, ?)\n")

ACCEPT_REJECT_BOOKING = ("\n"
                  "UPDATE bookings\n"
                  "SET status = ?\n"
                  "WHERE booking_id = ?\n")

DELETE_BOOKING = ("\n"
                  "DELETE FROM bookings\n"
                  "WHERE booking_id = ? AND status = 'Pending'\n")

GET_ALL_BOOKINGS = ("\n"
                "SELECT booking_id, user_mobile, car_id, from_date, to_date, status, fee\n"
                "FROM bookings\n")

GET_FUTURE_BOOKINGS = ("\n"
                       "SELECT booking_id, user_mobile, car_id, from_date, to_date, status, fee\n"
                       "FROM bookings\n"
                       "WHERE user_mobile = ?\n"
                       "AND from_date > DATE('now')\n"
                       "ORDER BY from_date ASC;\n")

GET_BOOKINGS_BY_STATUS = ("\n"
                "SELECT booking_id, user_mobile, car_id, from_date, to_date, status, fee\n"
                "FROM bookings WHERE status = ?\n")

CHECK_BOOKING_ID_EXIST = ("\n"
                          "SELECT booking_id FROM bookings WHERE booking_id = ? AND status = 'Pending'\n")

FETCH_RENTAL_COUNTS = ("SELECT rentals_count, last_rental_date FROM customers WHERE email = ?")

FETCH_USER_PREFERENCE = ("SELECT preferred_make, preferred_model FROM user_preferences WHERE user_mobile = ?")

UPDATE_CUSTOMER_RENTAL_COUNT = ("UPDATE customers SET rentals_count = rentals_count + 1, last_rental_date = ?"
                                " WHERE email = ?")