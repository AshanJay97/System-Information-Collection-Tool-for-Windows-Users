# System-Information-Collection-Tool-for-Windows-Users
This project provides a tool to collect and manage detailed system information, save the data locally, and push it to a Firebase Realtime Database. The tool is written in Python and can be converted into an executable for running on devices without Python installed.
# System Information Collection Tool

This project provides a tool to collect and manage detailed system information, save the data locally, and push it to a Firebase Realtime Database. The tool is written in Python and can be converted into an executable for running on devices without Python installed.

---

## Features
- **Collect System Information**: Gathers details such as device name, serial number, OS version, processor, RAM, disk capacity, logged-in users, installed software, and more.
- **Save to Desktop**: Saves the collected information as a JSON file on the user's desktop.
- **Push to Firebase**: Uploads the system information to a Firebase Realtime Database, uniquely identified by the device’s serial number.
- **Silent Execution**: Runs without showing a terminal or PowerShell window (using `--noconsole`).

---

## Installation

### Prerequisites
- Python 3.8 or higher
- Pip
- Firebase Realtime Database
- Git (optional)

### Clone the Repository
```bash
git clone https://github.com/your-username/system-info-tool.git
cd system-info-tool
```

### Install Dependencies
Install the required Python packages:
```bash
pip install -r requirements.txt
```

---

## Usage

### Run the Script with Python
```bash
python system_info.py
```

### Convert to Executable
If you want to run the tool on devices without Python installed:
1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```
2. Convert the script to an executable:
   ```bash
   pyinstaller --onefile --noconsole system_info.py
   ```
3. The `.exe` file will be available in the `dist` folder.

### Output
- The system information will be saved as a JSON file on the desktop with the filename format: `<Device_Serial_Number>_system_info.json`.
- The data will also be pushed to the Firebase Realtime Database.

---

## Firebase Setup
1. Create a Firebase Realtime Database.
2. Note the database URL (e.g., `https://your-project-id.firebaseio.com/`).
3. Replace the placeholder URL in `push_to_firebase` function with your database URL:
   ```python
   firebase_url = "https://your-project-id.firebaseio.com/system_info.json"
   ```

---

## Example JSON Output
```json
{
    "Device Name": "DESKTOP-12345",
    "Model": "HP ProBook 450 G5",
    "Serial Number": "5CD12345",
    "OS Version": "Windows 10 (Build 19045)",
    "Processor": "Intel(R) Core(TM) i5-8250U CPU @ 1.60GHz",
    "RAM": "16.00 GB (12.00 GB usable)",
    "Disk Capacity": "256.00 GB",
    "Last Login": "2024-12-27T10:00:00",
    "Logged-in Users": ["John", "Admin"],
    "All User Accounts": ["Admin", "Guest", "John"],
    "Connected Network": "Home_WiFi",
    "Device IP": "192.168.1.5",
    "Installed Software": [
        {"Name": "Google Chrome", "Version": "117.0.5938.132"},
        {"Name": "Python", "Version": "3.10.0"}
    ]
}
```

---

## Contributing

### Reporting Issues
If you find a bug or have a feature request, please open an issue in this repository.

### Pull Requests
1. Fork the repository.
2. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add your feature description here"
   ```
4. Push to your branch:
   ```bash
   git push origin feature/your-feature-name
   ```
5. Open a pull request.

---

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Author
**Your Name**
- [GitHub](https://github.com/AshanJay97)
- [Email](mailto:wmashan97@yahoo.com)

---

## Acknowledgments
Special thanks to the open-source community and Firebase for providing the platform.

