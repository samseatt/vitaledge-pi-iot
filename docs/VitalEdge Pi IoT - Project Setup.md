## VitalEdge Pi IoT - Project Setup: Pi Emulator and Pi Hardware

### PART I - Raspberry Pi Emulator Setup for VitalEdge IoT Project

This is a comprehensive **Cookbook** for setting up the Raspberry Pi emulator environment and running the Pi IoT project, from installation to testing, including terminal commands, SQLite queries, and essential notes to streamline the process.


#### 1. **Environment Setup**

**Platform**: macOS (Intel)

**Primary Tools**: Docker, QEMU (optional), SQLite, Python

---

#### 2. **Installation and Configuration**

1. **Install Docker**:
   - Docker Desktop version compatible with macOS Intel (version 4.3.2 or higher).
   - [Download Docker](https://www.docker.com/products/docker-desktop) and follow installation steps.

2. **Install QEMU (Optional, for Emulated Environment)**:
   ```bash
   brew install qemu
   ```

3. **Prepare Raspberry Pi OS Image**:
   - Download the **Raspberry Pi OS Lite** image from the [Raspberry Pi OS Archives](https://downloads.raspberrypi.org/raspios_oldstable_lite_armhf/images/).
   - Place the image in the `~/pi-emulator` directory (or similar).

4. **Set Up Docker Image for Pi Emulation**:
   - Clone the PiServer repository:
     ```bash
     git clone https://github.com/raspberrypi/piserver.git ~/projects/vitaledge/pi-emulator/piserver
     ```
   - **Build the Docker Image**:
     ```bash
     cd ~/projects/vitaledge/pi-emulator/piserver
     docker build -t pi-emulator .
     ```
   - **Run the Emulator**:
     ```bash
     docker run -it --rm --name pi-emulator-instance pi-emulator
     ```

---

#### 3. **Inside the Pi Emulator: Project Directory Structure**

Create the following project structure under `/home/pi/vitaledge-pi-monitoring`:
   ```plaintext
   vitaledge-pi-monitoring/
   ├── src/
   │   ├── data_collection/
   │   ├── data_processing/
   │   ├── data_transmission/
   │   └── utils/
   ├── main.py
   ├── requirements.txt
   ├── sensor_data.db
   └── logs/
   ```

---

#### 4. **Install Required Python Packages**

Run the following commands inside the emulator to install dependencies (note that `sqlite3` and `logging` are built-in):
```bash
cd /home/pi/vitaledge-pi-monitoring
pip3 install -r requirements.txt
```

---

#### 5. **SQLite Setup and Database Queries**

1. **Initialize the Database**:
   ```bash
   sqlite3 sensor_data.db
   ```
   - Create the `sensor_data` table:
     ```sql
     CREATE TABLE IF NOT EXISTS sensor_data (
         id INTEGER PRIMARY KEY AUTOINCREMENT,
         device_id TEXT,
         patient_id TEXT,
         data TEXT,
         status TEXT,
         timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
     );
     ```

2. **Basic SQLite Commands**:
   - **Show Tables**:
     ```sql
     .tables
     ```
   - **View Schema**:
     ```sql
     .schema sensor_data
     ```
   - **Query Data**:
     ```sql
     SELECT * FROM sensor_data;
     ```
   - **Delete Entries**:
     ```sql
     DELETE FROM sensor_data WHERE status = 'sent';
     ```
   - **Exit SQLite**:
     ```bash
     .exit
     ```

---

#### 6. **Running and Testing the Project**

1. **Start the Project**:
   - Run `main.py` to simulate data collection, processing, and transmission.
   ```bash
   python3 main.py
   ```

2. **Send Synthetic Data to the Backend**:
   - Run `main.py` to send data directly to the backend REST API:
   ```bash
   python3 main.py
   ```

3. **Debugging Commands**:
   - Check Docker logs for backend:
     ```bash
     docker logs <backend_container_name>
     ```
   - To restart the emulator:
     ```bash
     docker restart pi-emulator-instance
     ```

4. **Retry Unsent Data**:
   - Runs automatically, but can also be triggered by calling `retry_unsent_data()` within `transmitter.py`.

---

#### 7. **Mock Sensor Configuration**

1. **Add Mock Sensor Interface** in `/src/data_collection/mock_sensors.py`:
   - **Temperature Sensor**:
     ```python
     class MockTemperatureSensor:
         def read(self):
             return {"temperature": round(random.uniform(36.5, 37.5), 1)}
     ```
2. **Replace Synthetic Data Generator** in `main.py`:
   - Integrate mock sensor classes to simulate real data sources.

---

#### 8. **Authentication and Backend Integration**

1. **Get JWT Token**:
   - Use `get_jwt_token` function to retrieve a valid token from the backend.

2. **Configure Authentication Endpoint**:
   - Replace `AUTH_ENDPOINT` and `DATA_ENDPOINT` with actual backend URLs:
     ```python
     AUTH_ENDPOINT = "http://host.docker.internal:8080/authenticate"
     DATA_ENDPOINT = "http://host.docker.internal:8080/api/patients/{patientId}/device-data"
     ```

3. **Run CURL Command for Testing**:
   - Test connection and data transmission to backend directly:
     ```bash
     curl -X POST http://host.docker.internal:8080/authenticate -H "Content-Type: application/json" -d '{"username": "admin", "password": "password"}'
     ```

---

#### 9. **Potential Gotchas**

- **Emulator Connectivity Issues**:
  - If the emulator fails to connect to `host.docker.internal`, restart the emulator or verify backend URL configurations.

- **SQLite Issues**:
  - Confirm SQLite writes and reads by manually querying the `sensor_data.db` file.

- **CORS & Authentication**:
  - Ensure `CORS` settings in the backend allow requests from the emulator’s IP.
  - Handle JWT token expiration in `transmitter.py` to avoid unnecessary re-authentications.

- **High CPU Usage on Emulator**:
  - The emulator may have high CPU usage; limit QEMU configurations if using QEMU or allocate resources in Docker Desktop settings.

---

### Summary

This cookbook should serve as a practical guide for setting up, running, and troubleshooting the Raspberry Pi emulator environment for the VitalEdge IoT project. Use this document as a reference during development to keep the environment aligned and functioning smoothly before moving to the physical Pi hardware.

---

### PART II - VitalEdge IoT Project: Transitioning to Physical Hardware

This is a comprehensive **Cookbook (Part 2)** for transitioning the VitalEdge IoT project from the emulator environment to the physical Raspberry Pi hardware and real sensors. This guide provides step-by-step instructions on selecting hardware, setting up the board, installing necessary software, connecting sensors, and debugging on the Raspberry Pi.


### 1. **Hardware Selection and Setup**

#### Recommended Hardware Components
1. **Raspberry Pi Board**:
   - **Model**: Raspberry Pi 4 Model B (recommended for sufficient CPU and RAM).
   - **Accessories**: Heat sinks, fan, and case for heat management.

2. **Power Supply**:
   - **Output**: 5V, 3A USB-C power adapter.

3. **MicroSD Card**:
   - **Capacity**: 32GB or larger (minimum 16GB).
   - **Speed**: Class 10 or higher for optimal performance.
   - **Setup**: Install **Raspberry Pi OS Lite** (64-bit recommended).

4. **Temperature and Other Sensors**:
   - **Example**: Govee Bluetooth Hygrometer Thermometer (for temperature).
   - **Other sensors**: For heart rate, blood oxygen, or custom requirements.
   
5. **Connectivity**:
   - **Bluetooth**: For wireless sensors.
   - **Wi-Fi**: To connect the Pi to a network for backend communication.

6. **Additional Accessories**:
   - HDMI cable, external monitor, USB keyboard and mouse (optional for direct setup).
   - Alternatively, use **SSH for headless configuration** via Wi-Fi.

---

### 2. **Assembling the Raspberry Pi and Initial Setup**

#### Physical Setup
1. **Insert the MicroSD Card** with pre-installed Raspberry Pi OS Lite.
2. **Assemble the Pi in the Case**:
   - Place the Pi board in the case and attach heat sinks and fan if available.
   - Connect power, HDMI, keyboard, and mouse (if using a monitor).

#### Headless Configuration (Optional)
1. **Enable SSH**: If using headless setup, insert the SD card into a computer, create an empty file named `ssh` in the `boot` partition to enable SSH.
2. **Enable Wi-Fi (optional)**:
   - Create a file called `wpa_supplicant.conf` in the `boot` partition:
     ```plaintext
     country=US
     ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
     update_config=1

     network={
         ssid="Your_SSID"
         psk="Your_WiFi_Password"
     }
     ```

---

### 3. **Connecting the Raspberry Pi to Your Mac**

#### Option 1: SSH Over Wi-Fi
   - Power up the Raspberry Pi, connect it to Wi-Fi, and find its IP address.
   - Use the following command from your Mac:
     ```bash
     ssh pi@<raspberry_pi_ip_address>
     ```

#### Option 2: USB-Serial Connection
   - Connect the Pi to your Mac using a USB-to-serial adapter if you need direct access without a network.

---

### 4. **Installing Essential Software on the Raspberry Pi**

1. **Update System Packages**:
   ```bash
   sudo apt update
   sudo apt upgrade -y
   ```

2. **Install Python and Pip**:
   ```bash
   sudo apt install python3 python3-pip -y
   ```

3. **Install Project Dependencies**:
   - Clone the project from GitHub and navigate to the project directory:
     ```bash
     git clone <project_repo_url>
     cd vitaledge-pi-monitoring
     ```
   - Install dependencies from `requirements.txt`:
     ```bash
     pip3 install -r requirements.txt
     ```

4. **Install SQLite** (if not pre-installed):
   ```bash
   sudo apt install sqlite3 -y
   ```

5. **Install Bluetooth Libraries (bluepy)**:
   ```bash
   sudo apt install bluetooth libbluetooth-dev -y
   sudo pip3 install bluepy
   ```

6. **Set Up Logging and Create Directories**:
   - Set up a `logs/` directory for logging:
     ```bash
     mkdir logs
     ```

---

### 5. **Connecting and Testing Bluetooth Sensors**

1. **Check Bluetooth Connectivity**:
   - Confirm that Bluetooth is enabled:
     ```bash
     sudo systemctl enable bluetooth
     sudo systemctl start bluetooth
     ```

2. **Scan for Bluetooth Devices**:
   - Use `bluepy` to scan for sensors (e.g., temperature or heart rate sensors):
     ```python
     sudo python3 -m bluepy.blescan
     ```

3. **Connect to a Bluetooth Sensor**:
   - Create a Python script to pair with the sensor and read data.

#### Example Code to Connect and Retrieve Data
   ```python
   from bluepy.btle import Scanner, Peripheral

   scanner = Scanner()
   devices = scanner.scan(5.0)

   for dev in devices:
       print(f"Device {dev.addr} ({dev.addrType}), RSSI={dev.rssi} dB")
   ```

---

### 6. **Development and Debugging on the Pi**

1. **File Transfer and Synchronization**:
   - Use `scp` or Git for version control and syncing changes from your Mac to the Pi.

2. **Remote Access to Logs**:
   - Set up logging configurations to output log files in `/home/pi/vitaledge-pi-monitoring/logs/`.
   - Access logs with `tail -f`:
     ```bash
     tail -f logs/app.log
     ```

3. **Database Access**:
   - Open SQLite for querying the database directly:
     ```bash
     sqlite3 sensor_data.db
     ```

4. **Convenient Python REPL for Testing**:
   - Use an interactive Python shell to test functions interactively:
     ```bash
     python3
     >>> from src.data_collection import data_collector
     >>> data_collector.get_sensor_data()
     ```

---

### 7. **Final Configuration and Testing**

1. **Configure Backend URL and Authentication**:
   - Update `transmitter.py` with the production backend URL and credentials.

2. **Run the Project and Observe Behavior**:
   - Start the application:
     ```bash
     python3 main.py
     ```
   - Observe data being sent to the backend and retry logic in action.

3. **Monitor and Test Alerts and Error Handling**:
   - Confirm alerts trigger based on specified conditions (e.g., temperature threshold).
   - Observe logging for any unexpected behavior or errors.

---

### 8. **Additional Tips for Working with the Pi**

- **Enable VNC for Remote Desktop Access**:
   - Allows remote desktop access if you prefer a graphical interface. Enable VNC through `raspi-config`.
   
- **Automate Startup with Systemd**:
   - Create a `systemd` service file to run the application on boot.

   ```bash
   sudo nano /etc/systemd/system/vitaledge.service
   ```
   - Example service file content:
     ```plaintext
     [Unit]
     Description=VitalEdge IoT Monitoring Service
     After=multi-user.target

     [Service]
     Type=simple
     ExecStart=/usr/bin/python3 /home/pi/vitaledge-pi-monitoring/main.py
     Restart=always

     [Install]
     WantedBy=multi-user.target
     ```

   - **Enable the service**:
     ```bash
     sudo systemctl enable vitaledge.service
     sudo systemctl start vitaledge.service
     ```

---

### Summary and Key Points

- **Hardware Selection**: Use Pi 4 with Bluetooth-enabled sensors.
- **Setup Essentials**: Install Python, Bluetooth tools, bluepy, and SQLite.
- **Connectivity**: Use SSH or VNC for easier access from your Mac.
- **Testing and Debugging**: Log data, access SQLite, and monitor Bluetooth interactions.
- **Systemd Setup**: Automate app startup on boot for continuous operation.

This guide provides the foundational setup and tools for developing and testing the VitalEdge IoT project on real hardware, complete with efficient debugging and deployment practices.

---

## APPENDIX A - Final Considerations Before Moving Development to Physical Raspberry Pi Board

Here are a few final checks and considerations before transitioning from the emulator to real hardware:

### 1. **Final Code Review and Cleanup**
   - **Logging**: Confirm that logs are clear, and log levels (info, warning, error) are set appropriately to track operations and troubleshoot issues on real hardware.
   - **Error Handling**: Ensure that exceptions, especially around sensor communication and database operations, are handled gracefully.
   - **Code Modularity**: Check that all primary functions (data generation, transmission, retries, etc.) are modular and encapsulated, making it easy to adapt to real sensor input without major rewrites.

### 2. **Testing with Mock Data**
   - **Realistic Data Simulation**: For final emulator testing, adjust the synthetic data generator to better mimic actual sensor outputs, particularly in format and range, so the transition to hardware is smoother.
   - **Database Check**: Verify that all required fields for the backend and local database schema match expected formats to avoid data issues on real hardware.

### 3. **Prepare for Real Sensor Integration**
   - **Mock Sensor Interfaces**: Replace the synthetic data generator with mock classes for each intended sensor (like temperature or heart rate), structured similarly to the real sensors’ expected data and timing.
   - **Bluetooth/Wi-Fi Testing (if applicable)**: If planning Bluetooth or Wi-Fi connections, confirm compatibility with libraries on your emulator, though actual tests will need the hardware.

### 4. **Testing Plan for Hardware Transition**
   - **Stepwise Testing**: Plan incremental tests on real hardware, starting with the basic setup and sensor connectivity, and then testing data transmission.
   - **Network Configuration**: Ensure that network settings (IP addresses, Docker configurations, etc.) align with the hardware environment.

### 5. **Transition Setup Instructions**
   - **Hardware-Specific Instructions**: Document the setup process for any necessary libraries and configurations on the physical Raspberry Pi to replicate the emulator environment.
   - **Automation**: Consider setting up scripts or configurations that streamline setup on the hardware, including dependencies, environment variables, and any startup scripts.

Once these steps are complete, you’ll be well-prepared to switch to physical hardware, start testing real sensor integrations, and further refine the project’s capabilities and robustness.