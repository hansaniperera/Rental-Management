class Booking:
    def __init__(self, user_mobile, car_id, from_date, to_date, status, fees, booking_id=None):
        self.__user_mobile = user_mobile
        self.__car_id = car_id
        self.__from_date = from_date
        self.__to_date = to_date
        self.__status = status
        self.__booking_id = booking_id
        self.__fees = fees

    @property
    def user_mobile(self):
        return self.__user_mobile

    @user_mobile.setter
    def user_mobile(self, user_mobile):
        self.__user_mobile = user_mobile


    @property
    def car_id(self):
        return self.__car_id

    @car_id.setter
    def car_id(self, car_id):
        self.__car_id = car_id

    @property
    def from_date(self):
        return self.__from_date

    @from_date.setter
    def from_date(self, from_date):
        self.__from_date = from_date

    @property
    def to_date(self):
        return self.__to_date

    @to_date.setter
    def to_date(self, to_date):
        self.__to_date = to_date

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, status):
        self.__status = status

    @property
    def booking_id(self):
        return self.__booking_id

    @booking_id.setter
    def booking_id(self, booking_id):
        self.__booking_id = booking_id

    @property
    def fees(self):
        return self.__fees

    @fees.setter
    def fees(self, fees):
        self.__fees = fees


