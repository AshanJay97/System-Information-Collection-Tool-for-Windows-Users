import platform
import os
import socket
import psutil
import subprocess
import win32com.client
import requests
import json
import subprocess

def get_system_info():
    """Collects system information."""
    system_info = {
        "Device Name": platform.node(),
        "Model": get_system_model(),
        "Serial Number": get_serial_number(),
        "OS Version": get_os_info(),
        "Processor": get_processor_info(),
        "RAM": get_ram_info(),
        "Disk Capacity": get_disk_capacity(),
        "Last Login": get_last_login(),
        "Logged-in Users": get_logged_in_users(),
        "All User Accounts": get_all_user_accounts(),
        "Connected Network": get_connected_network(),
        "Installed software": get_installed_software(),
        "Device IP": socket.gethostbyname(socket.gethostname())
    }
    return system_info

def run_powershell_command(command):
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW  # Prevents the console window from appearing
    try:
        output = subprocess.check_output(
            ["powershell", "-Command", command],
            text=True,
            startupinfo=startupinfo
        ).strip()
        return output
    except Exception as e:
        return str(e)

def get_system_model():
    """Fetches the system model."""
    try:
        output = subprocess.check_output(
            ["powershell", "-Command", "Get-CimInstance -ClassName Win32_ComputerSystem | Select-Object -ExpandProperty Model"],
            text=True
        ).strip()
        return output if output else "Unknown"
    except Exception as e:
        return str(e)

def get_serial_number():
    """Fetches the system serial number."""
    try:
        output = subprocess.check_output(
            ["powershell", "-Command", "Get-CimInstance -ClassName Win32_BIOS | Select-Object -ExpandProperty SerialNumber"],
            text=True
        ).strip()
        return output if output else "Unknown"
    except Exception as e:
        return str(e)

def get_os_info():
    """Fetches detailed OS information."""
    try:
        os_info = platform.uname()
        return f"{os_info.system} {os_info.release} (Build {os_info.version})"
    except Exception as e:
        return str(e)

def get_processor_info():
    """Fetches detailed processor information."""
    try:
        output = subprocess.check_output(
            ["powershell", "-Command", "Get-CimInstance -ClassName Win32_Processor | Select-Object -ExpandProperty Name"],
            text=True
        ).strip()
        return output if output else "Unknown"
    except Exception as e:
        return str(e)

def get_ram_info():
    """Fetches RAM details including usable memory."""
    try:
        total_ram = round(psutil.virtual_memory().total / (1024 * 1024 * 1024), 2)
        available_ram = round(psutil.virtual_memory().available / (1024 * 1024 * 1024), 2)
        return f"{total_ram:.2f} GB ({available_ram:.2f} GB usable)"
    except Exception as e:
        return str(e)

def get_disk_capacity():
    """Fetches the total disk capacity."""
    try:
        disk_usage = psutil.disk_usage('/')
        return f"{disk_usage.total / (1024 ** 3):.2f} GB"
    except Exception as e:
        return str(e)

def get_last_login():
    """Fetches the last login time."""
    try:
        wmi = win32com.client.GetObject("winmgmts:")
        users = wmi.ExecQuery("SELECT * FROM Win32_NetworkLoginProfile")
        last_login = max(user.LastLogon for user in users if user.LastLogon)
        return last_login if last_login else "No logins found"
    except Exception as e:
        return str(e)

def get_logged_in_users():
    """Fetches currently logged-in user accounts."""
    try:
        return [user.name for user in psutil.users()]
    except Exception as e:
        return str(e)

def get_all_user_accounts():
    """Fetches all user accounts on the device."""
    try:
        output = subprocess.check_output(
            ["powershell", "-Command", "Get-LocalUser | Select-Object -ExpandProperty Name"],
            text=True
        ).strip()
        return output.split('\n') if output else []
    except Exception as e:
        return str(e)

def get_connected_network():
    """Fetches the connected Wi-Fi network."""
    try:
        output = subprocess.check_output("netsh wlan show interfaces", shell=True, text=True)
        for line in output.splitlines():
            if "SSID" in line:
                return line.split(":")[1].strip()
        return "Not Connected"
    except Exception as e:
        return str(e)

def get_installed_software():
    """Fetches a list of installed software with their versions."""
    try:
        output = subprocess.check_output(
            ["powershell", "-Command", "Get-WmiObject -Class Win32_Product | Select-Object -Property Name, Version | Format-Table -AutoSize"],
            text=True
        ).strip()
        software_list = []
        for line in output.splitlines()[2:]:  # Skip header lines
            if line.strip():  # Skip empty lines
                parts = line.split(None, 1)
                if len(parts) == 2:
                    name, version = parts
                    software_list.append({"Name": name, "Version": version})
                else:
                    software_list.append({"Name": parts[0], "Version": "Unknown"})
        return software_list
    except Exception as e:
        return str(e)

def save_to_desktop(data):
    """Saves system information as a JSON file on the desktop."""
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    file_name = f"{data['Device Name']}_system_info.json"
    file_path = os.path.join(desktop_path, file_name)
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)
    print(f"System information saved to {file_path}")


def push_to_firebase(data):
    """Pushes system information to the Firebase Realtime Database."""
    try:
        serial_number = data["Serial Number"]  # Use the serial number as the unique key
        if not serial_number or serial_number == "Unknown":
            raise ValueError("Serial Number is missing or invalid.")

        firebase_url = "https://your-project-id.firebaseio.com/system_info.json"
        response = requests.put(firebase_url, json=data)

        if response.status_code == 200:
            print(f"Data successfully pushed to Firebase for serial number: {serial_number}.")
        else:
            print(f"Failed to push data: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error pushing data to Firebase: {e}")

if __name__ == "__main__":
    info = get_system_info()  # Collect system info
    save_to_desktop(info)     # Save locally
    push_to_firebase(info)    # Push to Firebase
