# Singleton instance to store logged user details

# Singleton object to save current logged user details
class UserSession:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.current_user = None  # Initialize the current user
        return cls._instance

    def set_current_user(self, user):
        self.current_user = user  # Set the current user

    def get_current_user(self):
        return self.current_user  # Get the current user
