
## Requirements Document: VitalEdge Raspberry Pi IoT Edge System

#### **1. Introduction**

**Project Overview**:  
The **VitalEdge Raspberry Pi IoT Edge System** is a versatile edge computing solution designed to capture, preprocess, analyze, and securely transmit health metrics from connected sensors. It acts as a bridge between local IoT data collection and the larger VitalEdge backend, enabling real-time monitoring, event-driven alerts, and remote data storage in a centralized backend.  

**Purpose of the Requirements Document**:  
To define functional and non-functional requirements for the VitalEdge Raspberry Pi IoT Edge System, detailing specific system capabilities and performance criteria to ensure modularity, security, and adaptability within the VitalEdge ecosystem.

---

#### **2. Functional Requirements**

##### **2.1 Data Collection and Connectivity**

**FR1**: The system must support multiple sensor types, initially including:
   - Heart rate sensors
   - Temperature sensors
   - Oxygen level sensors

**FR2**: Data must be collected via both Bluetooth and Wi-Fi protocols, as applicable:
   - **FR2.1**: Bluetooth data collection via bluepy or similar libraries.
   - **FR2.2**: Wi-Fi-based data for future sensors if applicable.

**FR3**: The system must allow sensor data simulation to facilitate testing.

##### **2.2 Local Data Processing**

**FR4**: Data from sensors must be preprocessed locally on the Raspberry Pi device to:
   - Filter noise or anomalies.
   - Standardize data formats for uniform backend compatibility.

**FR5**: Implement local analytics for threshold-based alerts (e.g., critical low oxygen levels), allowing immediate notifications without backend dependency.

##### **2.3 Data Storage and Retry Mechanism**

**FR6**: The system must temporarily store data locally using SQLite for resilience.
   - **FR6.1**: Store raw sensor data, with a timestamp, sensor type, and patient ID.

**FR7**: Implement a retry mechanism to send any unsent data when connectivity is restored.

**FR8**: Store data transmission status (e.g., "sent," "unsent") for each record to prevent duplicate transmissions.

##### **2.4 Secure Data Transmission**

**FR9**: Data must be transmitted to the VitalEdge backend over HTTPS to ensure secure communication.

**FR10**: The system must authenticate each session with the backend using a JSON Web Token (JWT), refreshing tokens as needed when expired.

##### **2.5 Alerts and Notifications**

**FR11**: Implement event-driven alerts for predefined conditions (e.g., oxygen below a threshold) using local analytics.

**FR12**: Support future external alert integrations (e.g., connected alarms) to respond to data events.

##### **2.6 System Configuration and Extensibility**

**FR13**: The system configuration must support easy addition, removal, or modification of connected sensors, enabling extensibility for new sensor types.

**FR14**: Develop sensor abstraction layers to integrate new devices with minimal changes to core code.

---

#### **3. Non-Functional Requirements**

##### **3.1 Security**

**NFR1**: All data must be encrypted during transmission, and sensitive information must be handled in compliance with HIPAA or other applicable data privacy standards.

**NFR2**: Authentication tokens must be securely managed, ensuring unauthorized parties cannot access sensitive data.

##### **3.2 Performance**

**NFR3**: The system must process sensor data with minimal latency (<100ms for local processing tasks) to ensure timely responses for critical health metrics.

**NFR4**: Retry mechanisms should handle intermittent connectivity efficiently, without causing data loss or duplicate transmissions.

**NFR5**: Local alerts must be generated within 50ms of threshold breaches to ensure immediate action can be taken.

##### **3.3 Reliability**

**NFR6**: The system should log all operations, including data processing, transmissions, and error handling, for audit and troubleshooting purposes.

**NFR7**: Data collection should operate with 99% uptime, with resilience to network disruptions.

##### **3.4 Usability**

**NFR8**: Configuration files must be easily editable, with clear documentation, allowing setup adjustments by non-expert users.

**NFR9**: System logs should be accessible for diagnostics and troubleshooting.

---

#### **4. Data Requirements**

**DR1**: Data captured from each sensor must include:
   - Patient ID
   - Device ID
   - Timestamp
   - Sensor type and value
   - Measurement units (e.g., bpm for heart rate)

**DR2**: Data must be formatted in JSON when transmitted to the backend.

**DR3**: Sensor data should follow schema constraints compatible with the VitalEdge backend (e.g., double values for measurements, date formats as ISO 8601).

---

#### **5. Interface Requirements**

##### **5.1 Backend API Integration**

**IR1**: The system must interact with the VitalEdge backend via REST API endpoints, supporting endpoints for:
   - Authentication and JWT retrieval.
   - Data submission to patient records.

**IR2**: The system must support JSON-formatted HTTP POST requests to the backend for data transmission.

**IR3**: Retry mechanisms must ensure that unsent data is resent to the correct backend endpoint.

##### **5.2 Local API or CLI for Configuration**

**IR4**: Provide a configuration interface or CLI commands to allow authorized users to:
   - Configure new sensor connections.
   - Set data transmission intervals and alert thresholds.
   - Review system logs and error reports.

---

#### **6. Compliance Requirements**

**CR1**: The system must ensure data privacy and security compliance, aligning with healthcare industry standards (e.g., HIPAA).

**CR2**: Local storage (SQLite) must not retain data longer than a pre-configured time (e.g., 24 hours), with automatic deletion mechanisms.

**CR3**: The system should provide an audit trail for all data processing and transmission operations, stored in the backend.

---

#### **7. Future Scope and Extensions**

**FS1**: **Predictive Analytics and Machine Learning**: Support integration with predictive models for early detection of potential health issues.

**FS2**: **Integration with Cloud Platforms**: Explore integration with platforms like AWS Greengrass or Azure IoT Edge for enhanced analytics.

**FS3**: **Blockchain for Data Integrity**: Consider a blockchain-based audit trail for tracking data flow and modifications, enhancing data integrity and transparency.

**FS4**: **Expansion of Sensors and Alerts**: Expand the sensor ecosystem and alert types to accommodate a wider range of healthcare monitoring needs.

---

#### **8. Glossary**

- **Edge Computing**: Processing data locally on IoT devices rather than sending it immediately to a centralized backend.
- **IoT**: Internet of Things; interconnected devices that collect and exchange data.
- **SQLite**: Lightweight database system used for local data storage on the Raspberry Pi.
- **JWT**: JSON Web Token; a method for securely transmitting information between parties for authentication.
- **HIPAA**: Health Insurance Portability and Accountability Act; U.S. regulation for protecting patient health information.
