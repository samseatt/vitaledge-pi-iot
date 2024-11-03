"""
main.py - Main execution script
This script will manage the flow, including sensor data collection, processing,
alerting, and transmission.
"""
# main.py
from src.data_collection.sensor_manager import SensorManager
from src.data_processing.data_converter import convert_to_backend_format
from src.data_processing.data_analyzer import check_alert_conditions, analyze_recent_trends
from src.data_processing.database_manager import DatabaseManager
from src.data_transmission.transmitter import Transmitter
from src.utils.config import DEVICE_ID, PATIENT_ID, DB_PATH
from src.utils.logger import log_info, log_error
import time

def main():
    sensor_manager = SensorManager(use_synthetic=False)
    transmitter = Transmitter()
    db_manager = DatabaseManager()

    while True:
        # Step 1: Collect data from sensors
        sensor_data = sensor_manager.collect_data()

        # Step 2: Save raw sensor data to SQLite
        record_id = db_manager.save_data(DEVICE_ID, PATIENT_ID, sensor_data)
        if record_id is None:
            log_error(f"!!ASSERT!! Unexpectedly null returned for record_id")

        # Step 3: Check for alerts based on the collected sensor data
        alert_message = check_alert_conditions(sensor_data)
        if alert_message:
            log_info(f"Alert: {alert_message}")

        # Assume db_path is already defined as the path to your SQLite database
        trend_alert = analyze_recent_trends(db_path=DB_PATH, time_window_minutes=5)
        if trend_alert:
            print(f"Alert: {trend_alert}")

        # Step 4: Convert sensor data to backend format
        backend_data = convert_to_backend_format(sensor_data)

        # Step 5: Attempt to send backend-formatted data to backend
        # if transmitter.send_data_http(backend_data):
        if transmitter.send_data_http(backend_data, PATIENT_ID, record_id):
            log_info("Data sent successfully to the backend.")
        else:
            log_error("Data transmission failed. Retrying will occur in the next cycle.")

        # Step 6: Retry sending any unsent data
        transmitter.retry_unsent_data()

        # Step 7: Wait before the next reading
        time.sleep(5)  # Adjustable delay between readings

if __name__ == "__main__":
    main()
