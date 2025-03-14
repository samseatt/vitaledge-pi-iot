## Design Document: VitalEdge Raspberry Pi IoT Edge System


#### **1. Introduction**

**Purpose**  
This design document outlines the architecture, system components, data flow, and interaction model for the **VitalEdge Raspberry Pi IoT Edge System**. It describes the final design that will run on the Raspberry Pi hardware, supporting real-time data capture, processing, local storage, secure transmission, and alert mechanisms.

**Scope**  
This document specifies the complete system architecture, defining module interactions, hardware requirements, and software components for a scalable, modular, and secure edge computing solution within the VitalEdge healthcare ecosystem.

---

#### **2. System Architecture Overview**

The VitalEdge Raspberry Pi IoT Edge System is structured in three main layers:

1. **Sensor Layer**: Interface with health sensors (e.g., heart rate, temperature, and oxygen level) to collect patient data in real time.
2. **Edge Computing Layer**: Includes preprocessing, storage, and alert generation using local analytics on the Raspberry Pi.
3. **Transmission Layer**: Manages secure data transfer to the VitalEdge backend via REST API, with mechanisms for authentication, error handling, and data retransmission on failure.

---

#### **3. Module Design**

Each layer has several modules to handle specific functionalities, as shown below.

---

##### **3.1 Sensor Interface Module**

**Purpose**  
To interface with various Bluetooth and Wi-Fi sensors, collect data, and forward it to the data processing module.

**Components**  
1. **Bluetooth Interface**: Uses the `bluepy` library for communication with Bluetooth-enabled sensors. Supports:
   - **Heart Rate Monitor**
   - **Oxygen Level Sensor**
   - **Temperature Sensor**
   
2. **Wi-Fi Interface**: Manages sensors connected over Wi-Fi for data retrieval (future expansion).

**Design Considerations**  
- **Polling and Event-Driven Data Capture**: Polling frequency can be set based on sensor requirements (e.g., frequent for heart rate, infrequent for daily weight).
- **Mock Sensor Interface**: For testing purposes, a mock sensor class generates synthetic data to simulate real sensor feeds.

---

##### **3.2 Data Processing Module**

**Purpose**  
Processes, standardizes, and formats raw sensor data for storage and transmission.

**Components**  
1. **Data Converter**: Converts raw sensor data into the `IoTDeviceData` format required by the backend.
2. **Alert Generation**: Monitors thresholds (e.g., oxygen below 88%) and triggers alerts if data exceeds critical limits.
3. **Local Analytics**: Performs lightweight calculations, such as averaging or trend detection, for near real-time insights.

**Design Considerations**  
- **Schema Flexibility**: Data conversion logic to support adding new sensor types without extensive code modifications.
- **Configurable Alert Rules**: Thresholds for each sensor type can be configured or updated for future requirements.

---

##### **3.3 Data Storage Module**

**Purpose**  
Stores data locally on the Raspberry Pi using SQLite, ensuring data is buffered and retried upon transmission failures.

**Components**  
1. **SQLite Database**: Stores sensor data, transmission status, and alert history.
   - **Table Structure**:
     - `sensor_data`: Stores raw data from sensors with fields like `deviceId`, `patientId`, `timestamp`, `heartRate`, `temperature`, `oxygenLevel`, and more.
     - `transmission_status`: Tracks the status of each record (`sent`, `unsent`) for efficient retry logic.
   - **Indexes**: Index on `timestamp` and `status` for fast retrieval and retries.
   
2. **Retry Logic**: Periodically scans for unsent data and retransmits records to the backend when connectivity is restored.

**Design Considerations**  
- **Local Data Retention Policy**: Configurable setting for how long data is retained locally (e.g., 24 hours) before deletion.
- **Error Handling**: Robust exception handling for database write failures and recovery mechanisms on reboot.

---

##### **3.4 Data Transmission Module**

**Purpose**  
Handles secure data transmission to the VitalEdge backend via REST APIs and ensures continuous connectivity through retry mechanisms.

**Components**  
1. **JWT Authentication**: Authenticates with the backend and retrieves a token, which is refreshed on expiration.
2. **HTTP Transmission**: Sends processed data to the backend’s REST API. HTTP headers include:
   - Content-Type: application/json
   - Authorization: Bearer <JWT Token>
3. **Retry on Failure**: If transmission fails, the status is marked as "unsent" in SQLite, and a retry is triggered in the next cycle.

**Design Considerations**  
- **Token Expiration Handling**: Automatically refreshes tokens upon expiry and reauthenticates as needed.
- **HTTPS for Secure Transmission**: Ensures all data transmissions are encrypted.
- **Compression (Future Extension)**: Implements data compression to reduce bandwidth usage for higher volume sensor feeds.

---

#### **4. Data Flow**

1. **Sensor Data Collection**: The system polls or receives sensor data at regular intervals.
2. **Preprocessing and Local Storage**: Data is processed, formatted, and saved to SQLite, with initial status as "unsent."
3. **Threshold-Based Alert Generation**: If critical values are detected, an alert is logged and/or sent via notifications.
4. **Transmission to Backend**: Every few seconds, unsent data is retrieved, converted to backend-compatible JSON, and transmitted.
5. **Retry and Acknowledgement**: If the transmission succeeds, the status is updated to "sent" in SQLite. Failed transmissions are retried.

---

#### **5. Hardware Requirements**

**Primary Hardware**  
- **Raspberry Pi 4 Model B**: Quad-core CPU, 4GB RAM for sufficient processing power and storage.
- **Bluetooth Sensors**:
   - Govee Bluetooth Hygrometer Thermometer (for temperature and humidity)
   - Compatible heart rate monitor (e.g., Polar H10)

**Accessories**  
- Power adapter
- MicroSD card (minimum 32GB)
- USB dongle for Wi-Fi (if not embedded)

---

#### **6. Deployment and Configuration**

**Initial Setup**  
- **Environment Configuration**: Install necessary Python libraries (`requests`, `bluepy`, `sqlite3`), set up virtual environment.
- **Database Initialization**: Create SQLite tables for `sensor_data` and `transmission_status`.
- **Configure Authentication**: Set initial username, password, and backend URL for authentication and data endpoints.

**Runtime Configuration**  
- **Polling Interval**: Configure polling rates per sensor in a configuration file.
- **Alert Thresholds**: Editable file or database table for each sensor type’s threshold values.
- **Token Refresh Frequency**: Auto-adjusts based on token expiration duration.

---

#### **7. Error Handling and Logging**

**Error Handling Strategy**  
- **Database Errors**: Catch and log all database errors, retry on the next cycle.
- **Transmission Failures**: If HTTP transmission fails, the record is marked as "unsent," with a retry in the next interval.
- **Sensor Disconnection**: If a sensor disconnects, an alert is triggered, and the system attempts reconnection.

**Logging**  
- **Log Levels**: Info for successful operations, Warning for retried events, Error for critical failures.
- **Log Files**: Store logs locally in `/var/log/vitaledge_iot.log` on the Pi for remote debugging and audits.

---

#### **8. Security Considerations**

1. **Authentication**: Each Pi device will authenticate via JWT to prevent unauthorized data submission.
2. **Data Encryption**: All data transmissions use HTTPS to prevent data interception during transport.
3. **Access Control**: Ensure secure local access to logs and SQLite database, with permissions set to prevent unauthorized tampering.
4. **Data Retention**: Local data deletion mechanism to minimize retention of sensitive information on the edge device.

---

#### **9. Future Expansion**

1. **Additional Sensors**: Easily add support for new sensors through modular sensor interface classes.
2. **Cloud Edge Computing**: Integration with AWS Greengrass or similar platforms to enhance real-time analytics.
3. **ML Model Integration**: Deploy lightweight machine learning models on Pi for predictive health analytics.
4. **Alert Integrations**: Expand alerts to include triggers for external devices or notifications to user devices.

---

#### **10. Glossary**

- **Edge Computing**: Processing of data close to the source rather than on centralized servers.
- **IoT**: Internet of Things; interconnected devices that communicate data over a network.
- **SQLite**: Lightweight, serverless database engine used for local data storage.
- **JWT**: JSON Web Token; a method for representing claims securely between two parties.

---

This design document outlines the final architecture and setup for the VitalEdge Raspberry Pi IoT Edge System, providing a robust, secure, and scalable solution within the VitalEdge healthcare ecosystem. Let me know if any further details are needed on specific sections!