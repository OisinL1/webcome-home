import subprocess
import re
import BlynkLib
import time

# Blynk Authentication Token
BLYNK_AUTH = 'u4YKSxIAIOFSPr5UBq4ZFnCkrZglqaop'
blynk = BlynkLib.Blynk(BLYNK_AUTH)

# Known devices and their corresponding Blynk Virtual Pins
known_devices = {
    "192.168.8.95": {"name": "Mam's Phone", "pin": 0},
    "moto-e20 (192.168.8.13)": {"name": "Dad's Phone", "pin": 1},
    "M2012K11AG (192.168.8.14)": {"name": "My Phone", "pin": 2},
    "192.168.8.85": {"name": "Cian's Phone", "pin": 3}
}

# List of IPs or hostnames to ignore (e.g., router and other networked devices)
ignored_devices = [
    "homerouter.cpe (192.168.8.1)",  # Router IP
    "homerouter.cpe",  # Router hostname
    "HDipRPi",
    "192.168.8.96",  # Raspberry Pi hostname or other device hostname
    "192.168.8.38",
    "192.168.8.85",
    "192.168.8.83",
    "HDipRPi (192.168.8.96)"

]

UNKNOWN_DEVICE_PIN = 4  # Virtual Pin for Unknown Device Alert

# Function to scan connected devices using nmap
def scan_devices():
    print("Scanning for devices...")
    result = subprocess.run(["nmap", "-sn", "192.168.8.0/24"], capture_output=True, text=True)
    output = result.stdout
    devices = re.findall(r"Nmap scan report for (.+?)\n", output)
    return devices

# Function to update Blynk LEDs
def update_blynk():
    connected_devices = scan_devices()
    unknown_detected = False

    # Update LEDs for known devices
    for ip, info in known_devices.items():
        if ip in connected_devices:
            blynk.virtual_write(info["pin"], 1)  # LED ON for known device
            print(f"{info['name']} is at home. LED ON")
        else:
            blynk.virtual_write(info["pin"], 0)  # LED OFF for known device
            print(f"{info['name']} is not at home. LED OFF")
    
    # Check for unknown devices, ignoring the ones in the exceptions list
    for device in connected_devices:
        if device not in known_devices and device not in ignored_devices:
            print(f"Unknown device detected: {device}")
            unknown_detected = True
    
    # Handle unknown devices
    if unknown_detected:
        blynk.virtual_write(UNKNOWN_DEVICE_PIN, 1)  # LED ON for Unknown Device
        print("Unknown device detected! Triggering alert...")
    else:
        blynk.virtual_write(UNKNOWN_DEVICE_PIN, 0)  # LED OFF for Unknown Device

if __name__ == "__main__":
    while True:
        blynk.run()
        update_blynk()
        time.sleep(300)
