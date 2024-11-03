"""
sensor_interface.py
Defines abstract interfaces for sensors, which can be implemented as real or mocked sensors.
For now, implement mock classes that simulate the data generation pattern of actual sensors.
"""
from abc import ABC, abstractmethod
import random, datetime

class SensorInterface(ABC):
    @abstractmethod
    def read_data(self):
        pass

class MockHeartRateSensor(SensorInterface):
    def read_data(self):
        return {"heart_rate": random.uniform(60, 100), "timestamp": datetime.datetime.utcnow().isoformat() + "Z"}

class MockTemperatureSensor(SensorInterface):
    def read_data(self):
        return {"temperature": random.uniform(36.5, 37.5), "timestamp": datetime.datetime.utcnow().isoformat() + "Z"}
