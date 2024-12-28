import subprocess
import re
import BlynkLib
import time
import paho.mqtt.client as mqtt
import json
from urllib.parse import urlparse

BLYNK_AUTH = 'u4YKSxIAIOFSPr5UBq4ZFnCkrZglqaop'
blynk = BlynkLib.Blynk(BLYNK_AUTH)

known_devices = {
    "192.168.8.95": {"name": "Mam's Phone", "pin": 0},
    "moto-e20 (192.168.8.13)": {"name": "Dad's Phone", "pin": 1},
    "M2012K11AG (192.168.8.14)": {"name": "My Phone", "pin": 2},
    "192.168.8.85": {"name": "Cian's Phone", "pin": 3}
}

ignored_devices = [
    "homerouter.cpe (192.168.8.1)", 
    "homerouter.cpe", 
    "HDipRPi",
    "192.168.8.96",  
    "192.168.8.38",
    "192.168.8.85",
    "192.168.8.83",
    "HDipRPi (192.168.8.96)"
]

UNKNOWN_DEVICE_PIN = 4  


URL = urlparse("mqtt://broker.emqx.io:1883/olark/home/presence")
BASE_TOPIC = URL.path[1:]


mqtt_client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
    else:
        print(f"Failed to connect to MQTT broker. Code: {rc}")

mqtt_client.on_connect = on_connect
mqtt_client.connect(URL.hostname, URL.port) 
mqtt_client.loop_start()  

def scan_devices():
    """Scan the local network using nmap and return connected devices."""
    print("Scanning for devices...")
    result = subprocess.run(["nmap", "-sn", "192.168.8.0/24"], capture_output=True, text=True)
    output = result.stdout
    devices = re.findall(r"Nmap scan report for (.+?)\n", output)
    return devices

def update_blynk_and_mqtt():
    """Update Blynk LEDs and publish presence data to MQTT."""
    connected_devices = scan_devices()
    unknown_detected = False

    presence_data = []  

    for ip, info in known_devices.items():
        device_present = ip in connected_devices
        presence_data.append({"name": info["name"], "present": device_present})

        if device_present:
            blynk.virtual_write(info["pin"], 1)  
            print(f"{info['name']} is at home. LED ON")
        else:
            blynk.virtual_write(info["pin"], 0) 
            print(f"{info['name']} is not at home. LED OFF")

    for device in connected_devices:
        if device not in known_devices and device not in ignored_devices:
            print(f"Unknown device detected: {device}")
            unknown_detected = True

    if unknown_detected:
        blynk.virtual_write(UNKNOWN_DEVICE_PIN, 1)  
        print("Unknown device detected! Triggering alert...")
    else:
        blynk.virtual_write(UNKNOWN_DEVICE_PIN, 0) 

    try:
        mqtt_payload = json.dumps(presence_data)
        mqtt_client.publish(BASE_TOPIC, mqtt_payload, qos=1)
        print(f"Published to MQTT: {mqtt_payload}")
    except Exception as e:
        print(f"Failed to publish to MQTT: {e}")

if __name__ == "__main__":
    try:
        while True:
            blynk.run()
            update_blynk_and_mqtt()
            time.sleep(300) 
    except KeyboardInterrupt:
        print("Script stopped by user.")
    finally:
        mqtt_client.loop_stop()
        print("Disconnected from MQTT.")
