import sqlite3

from dbConnect import Database

CREATE_ADMINS = ("CREATE TABLE IF NOT EXISTS admins (  "
    "email       TEXT PRIMARY KEY  "
                     "REFERENCES users (email),  "
    "branch      TEXT,  "
   " designation TEXT  "
");")

CREATE_BOOKINGS = ("CREATE TABLE IF NOT EXISTS bookings (  "
    "user_mobile INTEGER REFERENCES users (mobile_number),  "
    "car_id      TEXT    REFERENCES cars (car_id),  "
    "from_date   TEXT,  "
    "to_date     TEXT,  "
    "status      TEXT,  "
    "booking_id  INTEGER PRIMARY KEY  "
                        "UNIQUE  "
                        "NOT NULL,  "
   " fee         NUMERIC  "
");")

CREATE_CARS = ("CREATE TABLE IF NOT EXISTS cars (  "
    "car_id          TEXT        PRIMARY KEY  "
                               " UNIQUE  "
                                "NOT NULL,  "
    "make            TEXT,  "
    "mileage         NUMERIC,  "
    "model           TEXT,  "
    "year            INTEGER,  "
    "available_now   TEXT (1, 1),  "
    "min_rent_period INTEGER,  "
    "max_rent_period INTEGER,  "
   " daily_rate      NUMERIC  "
");")

CREATE_COMPANY_CODES = ("CREATE TABLE IF NOT EXISTS company_codes (  "
    "code        TEXT PRIMARY KEY,  "
   " description TEXT  "
");")

CREATE_CUSTOMERS = ("CREATE TABLE customers (  "
    "email               PRIMARY KEY  "
                        "REFERENCES users (email),  "
    "address        TEXT,  "
    "license_number TEXT, "
    "rentals_count    INTEGER DEFAULT 0, "
    "last_rental_date TEXT  "
");")

CREATE_USERS = ("CREATE TABLE IF NOT EXISTS users (  "
    "mobile_number INTEGER PRIMARY KEY,  "
    "first_name    TEXT,  "
    "last_name     TEXT,  "
    "email         TEXT    UNIQUE,  "
    "password      TEXT,  "
    "is_admin      TEXT  "
");")

CREATE_USER_PREFERENCES = ("CREATE TABLE IF NOT EXISTS user_preferences ( "
    "user_mobile INTEGER REFERENCES users (mobile_number),  "
    "preferred_make TEXT,  "
    "preferred_model TEXT,  "
    "PRIMARY KEY(user_mobile)  "
");")

BATCH_INSERT_CARS = """
INSERT INTO Cars (car_id, make, mileage, model, year, available_now, min_rent_period, max_rent_period, daily_rate)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
"""

INITIAL_CARS = [
    ('C001', 'Toyota', 15000, 'Corolla', 2020, 'Y', 5, 30, 80),
    ('C002', 'Honda', 20000, 'Civic', 2019, 'Y', 3, 14, 85),
    ('C003', 'Ford', 25000, 'Focus', 2021, 'Y', 3, 7, 90),
    ('C004', 'Chevrolet', 18000, 'Malibu', 2018, 'N', 2, 30, 90),
    ('C005', 'Nissan', 30000, 'Altima', 2020, 'Y', 1, 60, 82.5),
    ('C006', 'BMW', 12000, 'X3', 2022, 'Y', 3, 10, 120.25),
    ('C007', 'Mercedes', 10000, 'C-Class', 2021, 'Y', 2, 12, 122.25),
    ('C008', 'Hyundai', 15000, 'Elantra', 2019, 'Y', 3, 18, 85),
    ('C009', 'Kia', 20000, 'Soul', 2018, 'N', 1, 31, 75.24),
    ('C010', 'MMM', 13000, 'A4', 2020, 'Y', 2, 28, 100.25),
    ('C011', 'Nissan', 1000, 'Wagon', 2017, 'Y', 2, 36, 75.65),
    ('C012', 'Toyota', 2000, 'Aqua', 2018, 'Y', 4, 40, 80.55),
    ('C013', 'Nissan', 1150, 'March', 2011, 'Y', 1, 90, 78.9),
    ('C014', 'Audi', 1890, 'E8', 2022, 'Y', 5, 18, 128.45)
]

BATCH_INSERT_ADMINS = """
INSERT INTO admins (email, branch, designation) VALUES (?, ?, ?);
"""

INITIAL_ADMINS = [
    ('admin@hsp.com', 'Head Office', 'Owner')
]

BATCH_INSERT_COMPANY_CODES = """
INSERT INTO company_codes (code, description) VALUES (?, ?);
"""

INITIAL_COMPANY_CODES = [
    ('XYZ', 'Super Admin Code'),
    ('BCD', 'Staff Code'),
    ('ABC', 'Manager Code')
]

BATCH_INSERT_CUSTOMERS = """
INSERT INTO customers (email, address, license_number) VALUES (?, ?, ?);
"""

# Initial customer data
INITIAL_CUSTOMERS = [
    ('hansani@gmail.com', '189, Union Street, Auckland', 'L98765')
]

BATCH_INSERT_USERS = """
INSERT INTO users (mobile_number, first_name, last_name, email, password, is_admin) VALUES (?, ?, ?, ?, ?, ?);
"""

# Initial user data
INITIAL_USERS = [
    (215467845, 'super', 'admin', 'admin@hsp.com', 'test@123', '1'),
    (215678430, 'hansani', 'perera', 'hansani@gmail.com', '123', '0')
]

#  Setup database tables and default data
class SetupDatabase:

    def __init__(self):
        self.db = Database()

    # Create and commit tables
    def initialize_db(self):

        tables = [
            ("CARS", CREATE_CARS),
            ("USERS", CREATE_USERS),
            ("BOOKINGS", CREATE_BOOKINGS),
            ("ADMINS", CREATE_ADMINS),
            ("CUSTOMERS", CREATE_CUSTOMERS),
            ("COMPANY_CODES", CREATE_COMPANY_CODES),
            ("USER_PREFERENCES", CREATE_USER_PREFERENCES),
        ]

        self.db.connection.execute("BEGIN TRANSACTION")

        for table_name, create_query in tables:
            if not self.table_exists(table_name):
                self.db.cursor.execute(create_query)

        self.db.connection.commit()

    # Insert default data
    def run_insert_scripts(self):
        try:
            self.db.execute("BEGIN TRANSACTION")

            # self.db.execute_many(BATCH_INSERT_USERS, INITIAL_USERS)
            # self.db.execute_many(BATCH_INSERT_ADMINS, INITIAL_ADMINS)
            # self.db.execute_many(BATCH_INSERT_CUSTOMERS, INITIAL_CUSTOMERS)
            self.db.execute_many(BATCH_INSERT_CARS, INITIAL_CARS)
            self.db.execute_many(BATCH_INSERT_COMPANY_CODES, INITIAL_COMPANY_CODES)

            self.db.commit()

        except sqlite3.Error as e:
            self.db.rollback()
            print(f"Transaction failed: {e}")
            raise

    #  Check whether a table exist
    def table_exists(self, table_name):
        query = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';"
        result = self.db.fetch_one(query)
        return result is not None


if __name__ == "__main__":
    setup = SetupDatabase()
    setup.initialize_db()
    setup.run_insert_scripts()