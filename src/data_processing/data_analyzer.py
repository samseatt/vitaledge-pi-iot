"""
data_analyzer.py
Processes data in a sliding window to detect thresholds, triggering alerts if necessary.
Explanation of analyze_recent_trends

Database Query:
Fetches recent records (within time_window_minutes) from the SQLite database.
Only includes records with heart rate and temperature values, ordered by timestamp.

Trend Analysis:
Rising Trend Check: Calls is_increasing_trend() to check if heart rate or temperature is consistently increasing.
Average Threshold Check: Examines the average heart rate in the recent records, and flags if it is consistently above a safe threshold.

Helper Function - is_increasing_trend():
Determines whether a list of values shows a strictly increasing trend, meaning each value is greater than the previous.
"""
import sqlite3
from datetime import datetime, timedelta
from statistics import mean

# Alert conditions function from previous code
def check_alert_conditions(sensor_data):
    """Check if any individual sensor reading crosses alert thresholds."""
    if sensor_data.get("heart_rate") and sensor_data["heart_rate"] > 120:
        return "High heart rate alert"
    if sensor_data.get("temperature") and sensor_data["temperature"] > 38.5:
        return "High temperature alert"
    if sensor_data.get("oxygen_level") and sensor_data["oxygen_level"] < 90:
        return "Low oxygen level alert"
    return None  # No alert

# New function for time series analysis
def analyze_recent_trends(db_path, time_window_minutes=5):
    """
    Analyze recent trends in sensor data for potential alerts.

    Args:
        db_path (str): Path to the SQLite database file.
        time_window_minutes (int): The time window (in minutes) to look back for trend analysis.

    Returns:
        str: An alert message if a concerning trend is detected, else None.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Calculate the time threshold for recent records
    threshold_time = datetime.utcnow() - timedelta(minutes=time_window_minutes)

    # Query recent data within the specified time window
    cursor.execute("""
        SELECT timestamp, heart_rate, temperature
        FROM sensor_data
        WHERE timestamp >= ?
        ORDER BY timestamp DESC
    """, (threshold_time.isoformat(),))
    
    rows = cursor.fetchall()
    conn.close()

    # Check if we have enough data to analyze
    if len(rows) < 3:  # Require at least 3 records for meaningful trend analysis
        return None

    # Extract and reverse timestamps for analysis from oldest to newest
    heart_rates = [row[1] for row in rows if row[1] is not None]
    temperatures = [row[2] for row in rows if row[2] is not None]

    # Example trend check: Rising trend detection in heart rate and temperature
    if is_increasing_trend(heart_rates):
        return "Rising trend in heart rate detected - potential concern."
    if is_increasing_trend(temperatures):
        return "Rising trend in temperature detected - potential concern."

    # Example threshold check: Spike in recent average heart rate
    if heart_rates and mean(heart_rates) > 100:
        return "Elevated average heart rate detected in the last 5 minutes."

    return None  # No concerning trend detected

def is_increasing_trend(values):
    """
    Check if there is a consistent upward trend in the list of values.

    Args:
        values (list): List of numeric values to analyze.

    Returns:
        bool: True if there is a consistent increase in values, else False.
    """
    if len(values) < 3:
        return False  # Not enough data to establish a trend

    # Check if each successive value is greater than the previous
    return all(x < y for x, y in zip(values, values[1:]))
