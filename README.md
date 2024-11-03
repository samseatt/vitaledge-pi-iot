# VitalEdge Pi IoT Project

## Overview
This project is an IoT edge system designed for healthcare applications, running on a Raspberry Pi. It collects data from multiple sensors, performs basic analysis, and securely transmits critical health data to a backend.

## Features
- Sensor data collection and analysis on a Raspberry Pi
- Real-time transmission to a backend server
- Local database for data buffering and logging
- Edge-based alerting on critical conditions

## Project Structure
- `src/`: Source code for the Pi application, including data collection, processing, and transmission.
- `docs/`: Project documentation files, including vision, requirements, design, API specifications, and user manuals.
- `requirements.txt`: Python dependencies required for the project.
- `sensor_data.db`: Local SQLite database for storing buffered sensor data.

## Documentation
Detailed documentation is available in the `docs/` directory:
- **[Vision](docs/Vision.md)**: Project vision and objectives.
- **[Requirements](docs/Requirements.md)**: System requirements.
- **[Design](docs/Design.md)**: High-level and detailed system design.
- **[API Specification](docs/API_Specification.md)**: API endpoints and data schemas.
- **[Cookbook](docs/Cookbook.md)**: Installation and usage instructions, including setup for both emulated and physical hardware.

## Getting Started
1. **Installation**: See [Cookbook](docs/Cookbook.md) for setup and installation instructions.
2. **Running the Project**: Run `main.py` to start data collection and transmission from the Pi to the backend.
3. **Configuration**: Ensure correct backend URLs and authentication tokens are set in `src/config.py`.

## License
This project is currently private but may be made public in the future. License details will be added upon public release.
