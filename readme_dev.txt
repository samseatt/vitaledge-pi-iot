# Installing the emulator:

cd ~/projects/vitaledge/pi-emulator
git clone https://github.com/raspberrypi/piserver.git

cd piserver/
docker build -t pi-emulator .


# Starting the emulator
cd /Users/samseatt/projects/vitaledge/pi-emulator
docker run -it --rm --name pi-emulator-instance   -v ~/projects/vitaledge/pi-emulator:/home/pi/vitaledge-pi-monitoring pi-emulator
# This should start the emulator and take you in the emulator's Raspberry Pi OS/terminal

# Mount the emulator directory on Mac
ssh pi@localhost -p 5022

# A cleanup/diagnostic step to clear cache
ls cache_retry/
rm cache_retry/
ls -la __pycache__



# Inside the emulator

cd vitaledge-pi-monitoring/

apt-get update && apt-get install -y less
# sudo apt-get install -y python3-pip
apt-get update && apt-get install -y sqlite3


python3 -u collect_data.py > ../../logs/sensor_data.log &
jobs -l
tail -f ../../logs/sensor_data.log

export PYTHONPATH=/home/pi/vitaledge-pi-monitoring/src:$PYTHONPATH
# /home/pi/vitaledge-pi-monitoring/src
echo $PATH
# /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

curl -X POST http://host.docker.internal:8080/authenticate -H "Content-Type: application/json" -d '{"username": "admin", "password": "password"}'



# Blue tooth - to do on actual hardware - bluepy doesn't work from within this Pi emulator
sudo systemctl start bluetooth
sudo apt-get update
# sudo apt-get install -y python3-pip

pip3 install bluepy
sudo python3 -m bluepy.blescan
which systemctl
sudo systemctl start bluetooth


python3 main.py


sqlite3 sensor_data.db

# SQLite3 commands

sqlite> SELECT * FROM sensor_data;
sqlite> SELECT * FROM sensor_data WHERE patient_id = 'p_v2_1000';
sqlite> SELECT * FROM sensor_data WHERE heart_rate > 80;


sqlite> .tables
sqlite> .schema sensor_data
sqlite> DELETE FROM sensor_data;
sqlite> DROP TABLE IF EXISTS sensor_data;

sqlite> CREATE TABLE IF NOT EXISTS sensor_data (
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
        );

sqlite> ALTER TABLE sensor_data ADD COLUMN status TEXT DEFAULT 'unsent';


sqlite> .exit
