from abc import ABC, abstractmethod

from car import Car


class VehicleFactory(ABC):
    @abstractmethod
    def create_vehicle(self, car_id, make, mileage, model, year, available_now, min_rent_period,
                       max_rent_period, daily_rate):
        pass


class CarFactory(VehicleFactory):
    def create_vehicle(self, car_id, make, mileage, model, year, available_now, min_rent_period,
                       max_rent_period, daily_rate):
        return Car(car_id, make, mileage, model, year, available_now, min_rent_period, max_rent_period,
                   daily_rate)

