"""
src/data_collection/mock_sensors.py
"""
import random
import time

class MockTemperatureSensor:
    """Simulate a temperature sensor."""
    def __init__(self, min_temp=36.0, max_temp=37.5):
        self.min_temp = min_temp
        self.max_temp = max_temp

    def read_temperature(self):
        """Simulate reading temperature."""
        temp = round(random.uniform(self.min_temp, self.max_temp), 1)
        print(f"Mock Temperature Reading: {temp}°C")  # For debugging
        return temp

class MockHeartRateSensor:
    """Simulate a heart rate sensor."""
    def __init__(self, min_heart_rate=60, max_heart_rate=100):
        self.min_heart_rate = min_heart_rate
        self.max_heart_rate = max_heart_rate

    def read_heart_rate(self):
        """Simulate reading heart rate."""
        heart_rate = random.randint(self.min_heart_rate, self.max_heart_rate)
        print(f"Mock Heart Rate Reading: {heart_rate} bpm")  # For debugging
        return heart_rate
