
class Car:
    def __init__(self, car_id, make, mileage, model, year, available_now, min_rent_period, max_rent_period,
                 daily_rate):
        self.__car_id = car_id
        self.__make = make
        self.__mileage = mileage
        self.__model = model
        self.__year = year
        self.__available_now = available_now
        self.__min_rent_period = min_rent_period
        self.__max_rent_period = max_rent_period
        self.__daily_rate = daily_rate

    @property
    def car_id(self):
        return self.__car_id

    @car_id.setter
    def car_id(self, car_id):
        self.__car_id = car_id

    @property
    def make(self):
        return self.__make

    @make.setter
    def make(self, make):
        self.__make = make

    @property
    def mileage(self):
        return self.__mileage

    @mileage.setter
    def mileage(self, mileage):
        self.__mileage = mileage

    @property
    def model(self):
        return self.__model

    @model.setter
    def model(self, model):
        self.__model = model

    @property
    def year(self):
        return self.__year

    @year.setter
    def year(self, year):
        self.__year = year


    @property
    def available_now(self):
        return self.__available_now

    @available_now.setter
    def available_now(self, available_now):
        self.__available_now = available_now

    @property
    def min_rent_period(self):
        return self.__min_rent_period

    @min_rent_period.setter
    def min_rent_period(self, min_rent_period):
        self.__min_rent_period = min_rent_period

    @property
    def max_rent_period(self):
        return self.__max_rent_period

    @max_rent_period.setter
    def max_rent_period(self, max_rent_period):
        self.__max_rent_period = max_rent_period

    @property
    def daily_rate(self):
        return self.__daily_rate

    @daily_rate.setter
    def daily_rate(self, daily_rate):
        self.__daily_rate = daily_rate
