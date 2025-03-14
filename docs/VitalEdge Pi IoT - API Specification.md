## API Specification for VitalEdge Pi IoT (Raspberry Pi IoT Edge System)

This document provides the API specifications for the **VitalEdge Raspberry Pi IoT Edge System**, covering both the **mocked** and **real** implementations. It describes the interfaces for system authentication, data transmission, data retrieval, and health alert notifications.

This API specification provides a complete guide for implementing both the mocked and real data interfaces for the VitalEdge Raspberry Pi IoT Edge System, ensuring flexibility, scalability, and security in data handling.

---

#### **1. Overview**

- **Base URL**: `http://host.docker.internal:8080` (for emulator environment)
- **Base URL (Production)**: `https://<vitaledge-backend-url>` (for live environment)
- **Authorization**: JWT Bearer Token (required for data transmission and retrieval APIs)

---

### **2. API Endpoints**

The endpoints are categorized based on their functionality and are consistent across both the mocked and real implementations, with minor adjustments in data sources and sensor specifications.

---

#### **2.1 Authentication API**

**Purpose**  
Authenticate the Raspberry Pi device and retrieve a JWT token to be used in further requests.

**Endpoint**  
`POST /authenticate`

**Request**

| Field       | Type   | Description                       |
|-------------|--------|-----------------------------------|
| `username`  | string | Username for authentication       |
| `password`  | string | Password for authentication       |

**Example Request (JSON)**

```json
{
  "username": "admin",
  "password": "password"
}
```

**Response**

| Field   | Type   | Description                                  |
|---------|--------|----------------------------------------------|
| `token` | string | JWT token valid for further API requests     |

**Example Response (JSON)**

```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Error Codes**

- **401 Unauthorized**: Incorrect username or password.
- **500 Internal Server Error**: Server failed to generate a token.

---

#### **2.2 Sensor Data Transmission API**

**Purpose**  
Transmit collected sensor data to the VitalEdge backend. This endpoint is identical for both the mocked and real implementations.

**Endpoint**  
`POST /api/patients/{patientId}/device-data`

**Headers**

| Header            | Value               | Description                      |
|-------------------|---------------------|----------------------------------|
| `Authorization`   | `Bearer <JWT token>`| JWT token for authorization      |
| `Content-Type`    | `application/json`  | Type of content being sent       |

**Request Path Parameters**

| Field       | Type   | Description                |
|-------------|--------|----------------------------|
| `patientId` | string | Unique identifier for patient |

**Request Body Parameters (Real Implementation)**

| Field           | Type    | Description                                       |
|-----------------|---------|---------------------------------------------------|
| `deviceId`      | string  | Unique identifier for the IoT device              |
| `timestamp`     | string  | ISO 8601 timestamp of the data                    |
| `heartRate`     | float   | Heart rate in BPM                                 |
| `stepsCount`    | float   | Number of steps taken                             |
| `caloriesBurned`| float   | Calories burned                                   |
| `oxygenLevel`   | float   | Blood oxygen level (%)                            |
| `temperature`   | float   | Body temperature in Celsius                       |
| `batteryLevel`  | float   | Battery level percentage of the device            |
| `signalStrength`| int     | Signal strength of the device connection (RSSI)   |
| `status`        | string  | Device or reading status (e.g., `active`, `error`) |

**Request Body Parameters (Mock Implementation)**  
Simulated data for testing purposes.

| Field           | Type    | Description                                       |
|-----------------|---------|---------------------------------------------------|
| `deviceId`      | string  | Mock device ID                                    |
| `timestamp`     | string  | Mock ISO 8601 timestamp                           |
| `heartRate`     | float   | Randomly generated heart rate                     |
| `oxygenLevel`   | float   | Randomly generated blood oxygen level (%)         |
| `temperature`   | float   | Randomly generated temperature (Celsius)          |
| `status`        | string  | Always `active` in mocked data                    |

**Example Request (Real Implementation)**

```json
{
  "deviceId": "RPI-001",
  "patientId": "patient123",
  "timestamp": "2024-11-01T14:30:00Z",
  "heartRate": 72,
  "stepsCount": 500,
  "caloriesBurned": 100,
  "oxygenLevel": 95,
  "temperature": 36.5,
  "batteryLevel": 85,
  "signalStrength": -45,
  "status": "active"
}
```

**Response**

- **200 OK**: Data successfully transmitted
- **401 Unauthorized**: Missing or expired token
- **400 Bad Request**: Invalid data format
- **500 Internal Server Error**: Backend error in data processing

---

#### **2.3 Data Retrieval API**

**Purpose**  
Retrieve historical sensor data from the backend for a specific patient.

**Endpoint**  
`GET /api/patients/{patientId}/device-data`

**Headers**

| Header            | Value               | Description                      |
|-------------------|---------------------|----------------------------------|
| `Authorization`   | `Bearer <JWT token>`| JWT token for authorization      |

**Request Path Parameters**

| Field       | Type   | Description                |
|-------------|--------|----------------------------|
| `patientId` | string | Unique identifier for patient |

**Query Parameters (Optional)**

| Field           | Type    | Description                                      |
|-----------------|---------|--------------------------------------------------|
| `startDate`     | string  | ISO 8601 timestamp of the start of the data range |
| `endDate`       | string  | ISO 8601 timestamp of the end of the data range   |

**Example Request**

```
GET /api/patients/patient123/device-data?startDate=2024-11-01T00:00:00Z&endDate=2024-11-01T23:59:59Z
```

**Response**

| Field           | Type            | Description                                  |
|-----------------|-----------------|----------------------------------------------|
| `deviceData`    | Array of Objects| List of data entries                         |

**Example Response**

```json
{
  "deviceData": [
    {
      "deviceId": "RPI-001",
      "timestamp": "2024-11-01T14:30:00Z",
      "heartRate": 72,
      "stepsCount": 500,
      "caloriesBurned": 100,
      "oxygenLevel": 95,
      "temperature": 36.5,
      "batteryLevel": 85,
      "signalStrength": -45,
      "status": "active"
    },
    {
      "deviceId": "RPI-001",
      "timestamp": "2024-11-01T15:00:00Z",
      "heartRate": 75,
      "stepsCount": 550,
      "caloriesBurned": 105,
      "oxygenLevel": 94,
      "temperature": 36.6,
      "batteryLevel": 84,
      "signalStrength": -45,
      "status": "active"
    }
  ]
}
```

---

#### **2.4 Health Alert Notification API**

**Purpose**  
Provide alerts when certain thresholds are exceeded, enabling the backend to notify relevant parties.

**Endpoint**  
`POST /api/alerts`

**Headers**

| Header            | Value               | Description                      |
|-------------------|---------------------|----------------------------------|
| `Authorization`   | `Bearer <JWT token>`| JWT token for authorization      |
| `Content-Type`    | `application/json`  | Type of content being sent       |

**Request Body Parameters**

| Field          | Type    | Description                                       |
|----------------|---------|---------------------------------------------------|
| `alertType`    | string  | Type of alert (e.g., "heartRate", "temperature")  |
| `alertLevel`   | string  | Alert severity (e.g., "critical", "warning")      |
| `deviceId`     | string  | Unique identifier for the IoT device              |
| `patientId`    | string  | Unique identifier for the patient                 |
| `timestamp`    | string  | ISO 8601 timestamp of the alert                   |
| `message`      | string  | Detailed alert message                            |

**Example Request**

```json
{
  "alertType": "heartRate",
  "alertLevel": "critical",
  "deviceId": "RPI-001",
  "patientId": "patient123",
  "timestamp": "2024-11-01T14:31:00Z",
  "message": "Heart rate exceeded 100 BPM"
}
```

**Response**

- **201 Created**: Alert successfully created
- **401 Unauthorized**: Missing or expired token
- **400 Bad Request**: Invalid data format
- **500 Internal Server Error**: Backend error in processing the alert

---

#### **3. Error Handling and Mock Behavior**

**Mocked API Behavior**  
In the mock setup:
- **Authentication**: A fixed token is returned for testing (`mock-jwt-token`).
- **Data Transmission**: Sample data is used, with random values for fields like `heartRate`, `temperature`.
- **Alerts**: Alerts are triggered based on simulated thresholds rather than real data.

**Error Codes**  
The error codes remain consistent across real and mocked environments for consistency in testing.



---

#### **4. Notes for Real-World Usage**

- **JWT Token Expiration**: The Pi system must refresh the JWT token upon expiration, as detected through a `401 Unauthorized` response.
- **Time Synchronization**: Ensure the Raspberry Pi’s clock is synchronized for accurate timestamping.
- **Extended Security**: Consider integrating encryption on top of HTTPS for additional data protection.
