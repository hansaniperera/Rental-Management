import sqlite3


# Create Singleton Database connection
class Database:

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance') or not cls.instance:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self):
        if not hasattr(self, 'connection') or not self.connection:
            self.connection = sqlite3.connect('rentalDb.db')
            self.cursor = self.connection.cursor()

    def execute(self, query, params=None):
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        self.connection.commit()
