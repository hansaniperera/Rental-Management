import sqlite3


# Create Singleton Database connection
class Database:

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance') or not cls.instance:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self):
        if not hasattr(self, 'connection') or not self.connection:
            self.connection = sqlite3.connect('rentalDb_new1.db')
            self.connection.row_factory = sqlite3.Row  # Enable Row factory for column name access
            self.cursor = self.connection.cursor()

    def execute_and_commit(self, query, params=None):
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        self.connection.commit()

    def fetch_one(self, query, params=None):
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        return self.cursor.fetchone()

    def fetch_all(self, query, params=None):
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        return self.cursor.fetchall()

    def execute(self, query, params=None):
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)

    def execute_many(self, query, params_list):
        if params_list:
            self.cursor.executemany(query, params_list)
        else:
            raise ValueError("params_list cannot be empty")

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()

    def close(self):
        self.cursor.close()
        self.connection.close()
