"""
data_converter.py
Converts data to a JSON-compatible format for the backend, adding metadata like device ID, etc.
"""
# src/data_processing/data_converter.py
from datetime import datetime
from src.utils.config import DEVICE_ID, PATIENT_ID

def convert_to_backend_format(data, device_id=DEVICE_ID, patient_id=PATIENT_ID):
    """Convert sensor data to match backend IoTDeviceData schema."""
    # Extract individual data fields or use None if a field isn't available in the mock data
    return {
        "deviceId": device_id,
        "patientId": patient_id,
        "timestamp": datetime.utcnow().isoformat() + "Z",  # UTC timestamp in ISO 8601 format
        "heartRate": data.get("heart_rate"),
        "stepsCount": data.get("steps_count"),
        "caloriesBurned": data.get("calories_burned"),
        "oxygenLevel": data.get("oxygen_level"),
        "temperature": data.get("temperature")
    }
