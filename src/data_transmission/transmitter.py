"""
transmitter.py
Manages HTTP calls to the backend, sending data that’s already in the correct format.
It manages token retrieval and re-authentication efficiently.
This refactored version includes a token management system that retrieves and caches the token
but also re-authenticates if the token has expired or becomes invalid.
"""
import requests
import json
import time
from src.utils.config import DEVICE_ID, PATIENT_ID, BACKEND_URL, AUTH_ENDPOINT, USERNAME, PASSWORD
from src.utils.logger import log_info, log_error
from src.data_processing.database_manager import DatabaseManager
from src.data_processing.data_converter import convert_to_backend_format

class Transmitter:
    def __init__(self):
        self.token = None
        self.db_manager = DatabaseManager()

    def get_jwt_token(self):
        """Authenticate and retrieve JWT token."""
        credentials = {"username": USERNAME, "password": PASSWORD}
        try:
            response = requests.post(AUTH_ENDPOINT, json=credentials)
            response.raise_for_status()
            self.token = response.text.strip()
            log_info("JWT token obtained successfully.")
            return self.token
        except requests.exceptions.RequestException as e:
            log_error(f"Failed to authenticate: {e}")
            self.token = None
            return None

    def send_data_http(self, data, patient_id, record_id=None):
        """Send data via HTTP POST to the backend with JWT authentication."""
        if not self.token:
            self.token = self.get_jwt_token()
            if not self.token:
                log_error("Authentication failed. Cannot send data.")
                return False

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }
        endpoint = f"{BACKEND_URL}/api/patients/{patient_id}/device-data"
        
        try:
            response = requests.post(endpoint, json=data, headers=headers)
            response.raise_for_status()
            
            # Mark as sent if the transmission was successful
            if record_id is not None:
                self.db_manager.update_tx_status(record_id, 'sent')
                log_info(f"Data for record ID {record_id} sent successfully and marked as 'sent'.")
            
            return True
        except requests.exceptions.RequestException as e:
            log_error(f"Failed to send data: {e}")
            return False

    # def send_data_http(self, data, patient_id=PATIENT_ID):
    #     """Send data to backend with JWT authentication."""
    #     if not self.token:
    #         log_info("JWT token missing, attempting to authenticate...")
    #         self.get_jwt_token()

    #     headers = {
    #         'Content-Type': 'application/json',
    #         'Authorization': f'Bearer {self.token}'
    #     }
    #     endpoint = f"{BACKEND_URL}/api/patients/{patient_id}/device-data"

    #     try:
    #         response = requests.post(endpoint, data=json.dumps(data), headers=headers)
    #         response.raise_for_status()
    #         log_info(f"Data sent successfully for patient {patient_id}: {data}")
    #         return True
    #     except requests.exceptions.HTTPError as e:
    #         if response.status_code == 401:
    #             log_error("JWT token expired, re-authenticating...")
    #             self.get_jwt_token()
    #             return self.send_data_http(data, patient_id)  # Retry with new token
    #         else:
    #             log_error(f"Failed to send data: {e}")
    #             return False
    #     except requests.exceptions.RequestException as e:
    #         log_error(f"Transmission error: {e}")
    #         return False

    def retry_unsent_data(self):
        """Attempt to resend all unsent data in the SQLite buffer."""
        unsent_data = self.db_manager.fetch_unsent_data()
        for record in unsent_data:
            log_info(f"record: {record}")
            try:
                # Read the sqlite record - TODO read into individual field
                record_id, device_id, patient_id, timestamp, heart_rate, temperature, oxygen_level, steps_count, calories_burned, battery_level, signal_strength, status, transmit_status = record
 
                 # Recreate raw data as a python dictionary from sqlite data format
                sensor_data = {
                    "heart_rate": heart_rate,
                    "temperature": temperature,
                    "oxygen_level": oxygen_level
                }

                # Decode the raw data and convert to backend format
                # sensor_data = json.loads(data_json)
                backend_data = convert_to_backend_format(sensor_data)

                # Attempt to send to backend
                if self.send_data_http(backend_data, patient_id):
                    self.db_manager.update_tx_status(record_id, 'sent')  # Update status to 'sent' after success
                    log_info(f"Record ID {record_id} sent successfully and marked as 'sent'.")
                else:
                    log_error(f"Retry failed for record ID {record_id}")
            except json.JSONDecodeError as e:
                log_error(f"Failed to parse data for record ID {record_id}: {e}")

    # def retry_unsent_data(self):
    #     """Attempt to resend all unsent data in the SQLite buffer."""
    #     unsent_data = self.db_manager.fetch_unsent_data()
    #     for record in unsent_data:
    #         log_info(f"$$$$$$$ Unsent data found: {unsent_data}")
    #         record_id, device_id, patient_id, data_json, timestamp, status = record
    #         try:
    #             data = json.loads(data_json)  # Decode the JSON string back to a dictionary
    #             log_info(f"$$$$ Sending retry data: {data}")
    #             if self.send_data_http(data, patient_id):
    #                 self.db_manager.update_status(record_id, 'sent')
    #             else:
    #                 log_error(f"Retry failed for record ID {record_id}")
    #         except json.JSONDecodeError as e:
    #             log_error(f"Failed to decode JSON data for record ID {record_id}: {e}")
    
    # def retry_unsent_data(self):
    #     """Attempt to resend all unsent data in the SQLite buffer."""
    #     unsent_data = self.db_manager.fetch_unsent_data()
    #     for record in unsent_data:
    #         record_id, device_id, patient_id, data_json, timestamp, status = record
    #         log_info(f"data_json: {data_json}")
    #         data = json.loads(data_json)
    #         if self.send_data_http(data, patient_id):
    #             self.db_manager.update_status(record_id, 'sent')
    #         else:
    #             log_error(f"Retry failed for record ID {record_id}")
