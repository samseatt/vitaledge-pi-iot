"""
sensor_manager.py
Centralizes sensor handling, providing a unified way to acquire data,
allowing multiple sensors to be registered and managed.

Explanation of Mock Sensors:
MockTemperatureSensor: Generates a random temperature within a specified range to simulate
real-world variations in body temperature.
MockHeartRateSensor: Generates a random heart rate within a realistic range for testing purposes.

The SensorManager includes the collect_from_sensors method, which uses MockTemperatureSensor
and MockHeartRateSensor to produce sensor-like data.
"""
import random
from src.data_collection.mock_sensors import MockTemperatureSensor, MockHeartRateSensor
from src.utils.logger import log_info, log_error

class SensorManager:
    def __init__(self, use_synthetic=False):
        self.use_synthetic = use_synthetic
        self.temp_sensor = MockTemperatureSensor()
        self.heart_rate_sensor = MockHeartRateSensor()

    def collect_data(self):
        """Collect data from sensors or synthetic data."""
        try:
            if self.use_synthetic:
                return self.generate_synthetic_data()
            log_info("Collecting data from actual sensors.")
            return self.collect_from_sensors()
        except Exception as e:
            log_error(f"Error collecting data: {e}")
            return {}

    def collect_from_sensors(self):
        """Collect data from mock sensors for testing."""
        data = {
            "temperature": self.temp_sensor.read_temperature(),
            "heart_rate": self.heart_rate_sensor.read_heart_rate(),
            "oxygen_level": None  # Placeholder; add mock or actual data for oxygen level
        }
        log_info(f"Collected data from sensors: {data}")
        return data

    def generate_synthetic_data(self):
        """Generate synthetic sensor data."""
        data = {
            "heart_rate": random.randint(60, 100),
            "temperature": round(random.uniform(36.5, 37.5), 1),
            "oxygen_level": random.randint(90, 100)
        }
        log_info(f"Synthetic data generated: {data}")
        return data
