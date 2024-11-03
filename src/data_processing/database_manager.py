"""
database_manager.py
Handles SQLite storage for data that needs to be stored locally for analysis or backup.
"""
import sqlite3
import json
from datetime import datetime
from src.utils.logger import log_info, log_error
from src.utils.config import DB_PATH

# class DatabaseManager:
#     def __init__(self, db_path="/home/pi/vitaledge-pi-monitoring/sensor_data.db"):
#         try:
#             self.conn = sqlite3.connect(db_path)
#             self.create_tables()
#             log_info("Connected to SQLite database.")
#         except sqlite3.Error as e:
#             log_error(f"Failed to connect to SQLite database: {e}")

class DatabaseManager:
    def __init__(self, db_path=DB_PATH):
        log_info(f"Local database path: {db_path}")
        self.conn = sqlite3.connect(db_path)
        self.db_path = db_path
        self._create_table_if_not_exists()

    def create_tables(self):
        with self.conn:
            try:
                self.conn.execute("""
                    CREATE TABLE IF NOT EXISTS sensor_data (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Unique identifier for each record
                        device_id TEXT NOT NULL,               -- Unique identifier for the IoT device
                        patient_id TEXT NOT NULL,              -- Unique identifier for the patient
                        timestamp TEXT NOT NULL,               -- ISO 8601 formatted timestamp of the reading
                        heart_rate REAL,                       -- Heart rate in BPM
                        temperature REAL,                      -- Body temperature in Celsius
                        oxygen_level REAL,                     -- Blood oxygen level in percentage
                        steps_count REAL,                      -- Number of steps taken (if applicable)
                        calories_burned REAL,                  -- Calories burned (if applicable)
                        battery_level REAL,                    -- Battery level percentage of the device
                        signal_strength INTEGER,               -- Signal strength (RSSI) of the device connection
                        status TEXT,                           -- Status of the device or reading (e.g., "active", "error")
                        transmit_status TEXT DEFAULT 'unsent'  -- Status of data transmission to backend ('sent' or 'unsent')
                    )
                """)
                log_info("SQLite table 'sensor_data' created or verified.")
            except sqlite3.Error as e:
                log_error(f"Failed to create table: {e}")

    def _create_table_if_not_exists(self):
        """Ensure that the sensor_data table exists in the database with the updated schema."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sensor_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id TEXT NOT NULL,
                patient_id TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                heart_rate REAL,
                temperature REAL,
                oxygen_level REAL,
                steps_count REAL,
                calories_burned REAL,
                battery_level REAL,
                signal_strength INTEGER,
                status TEXT,
                transmit_status TEXT DEFAULT 'unsent'
            );
        """)
        conn.commit()
        conn.close()

    def save_data(self, device_id, patient_id, sensor_data):
        """
        Save sensor data to the SQLite database.

        Args:
            device_id (str): Unique identifier for the device.
            patient_id (str): Unique identifier for the patient.
            sensor_data (dict): Dictionary of sensor data to store.

        Returns:
            int: The ID of the inserted record.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO sensor_data (
                device_id, patient_id, timestamp, heart_rate, temperature, oxygen_level,
                steps_count, calories_burned, battery_level, signal_strength, status, transmit_status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            device_id,
            patient_id,
            sensor_data.get("timestamp", datetime.utcnow().isoformat()),
            sensor_data.get("heart_rate"),
            sensor_data.get("temperature"),
            sensor_data.get("oxygen_level"),
            sensor_data.get("steps_count"),
            sensor_data.get("calories_burned"),
            sensor_data.get("battery_level"),
            sensor_data.get("signal_strength"),
            sensor_data.get("status", "active"),
            "unsent"
        ))

        record_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return record_id
    
    # def save_data(self, device_id, patient_id, sensor_data, status='unsent'):
    #     """
    #     Save sensor data to the SQLite database.

    #     Args:
    #         device_id (str): Unique identifier for the device.
    #         patient_id (str): Unique identifier for the patient.
    #         sensor_data (dict): Dictionary of sensor data to store.

    #     Returns:
    #         int: The ID of the inserted record.
    #     """
    #     try:
    #         with self.conn:
    #             cursor = self.conn.cursor()
    #             cursor.execute("""
    #                 INSERT INTO sensor_data (
    #                     device_id, patient_id, timestamp, heart_rate, temperature, oxygen_level,
    #                     steps_count, calories_burned, battery_level, signal_strength, status, transmit_status
    #                 ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    #             """, (
    #                 device_id,
    #                 patient_id,
    #                 sensor_data.get("timestamp", datetime.utcnow().isoformat()),
    #                 sensor_data.get("heart_rate"),
    #                 sensor_data.get("temperature"),
    #                 sensor_data.get("oxygen_level"),
    #                 sensor_data.get("steps_count"),
    #                 sensor_data.get("calories_burned"),
    #                 sensor_data.get("battery_level"),
    #                 sensor_data.get("signal_strength"),
    #                 sensor_data.get("status", "active"),
    #                 "unsent"  # Default transmit status
    #             ))
    #             conn.commit()                
    #             record_id = cursor.lastrowid  # Get the ID of the inserted record
    #             conn.close()
    #             log_info(f"Data saved to SQLite for device {device_id}, patient {patient_id} with status '{status}'")
    #             return record_id  # Return the new record ID
    #     except sqlite3.Error as e:
    #         log_error(f"Failed to save data: {e}")
    #         return None  # Return None if insertion failed

    # def save_data(self, device_id, patient_id, sensor_data, status='unsent'):
    #     """Save raw sensor data to SQLite with a specified status."""
    #     try:
    #         with self.conn:
    #             self.conn.execute(
    #                 "INSERT INTO sensor_data (device_id, patient_id, data, status) VALUES (?, ?, ?, ?)",
    #                 (device_id, patient_id, json.dumps(sensor_data), status)
    #             )
    #         log_info(f"Data saved to SQLite for device {device_id}, patient {patient_id} with status '{status}'")
    #     except sqlite3.Error as e:
    #         log_error(f"Failed to save data: {e}")

    def fetch_unsent_data(self):
        """Fetch all unsent data from the database."""
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM sensor_data WHERE transmit_status = 'unsent'")
            unsent_data = cursor.fetchall()
            return unsent_data
        except sqlite3.Error as e:
            log_error(f"Failed to fetch unsent data: {e}")
            return []

    def update_tx_status(self, record_id, new_tx_status):
        """Update the status of a record by its ID."""
        try:
            with self.conn:
                self.conn.execute(
                    "UPDATE sensor_data SET transmit_status = ? WHERE id = ?",
                    (new_tx_status, record_id)
                )
            log_info(f"Record ID {record_id} updated to transmit_status '{new_tx_status}'")
        except sqlite3.Error as e:
            log_error(f"Failed to update transmit_status for record ID {record_id}: {e}")

    # def update_status(self, record_id, status='sent'):
    #     """Update the status of a specific record by ID."""
    #     try:
    #         with self.conn:
    #             self.conn.execute("UPDATE sensor_data SET status = ? WHERE id = ?", (status, record_id))
    #         log_info(f"Updated record ID {record_id} to status '{status}'")
    #     except sqlite3.Error as e:
    #         log_error(f"Failed to update status for record ID {record_id}: {e}")
