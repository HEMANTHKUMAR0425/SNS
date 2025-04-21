import random
import time

# Simulated Devices in the network with MAC addresses
devices = {
    "Device1": "00:0a:95:9d:68:16",
    "Device2": "00:0a:95:9d:68:17",
    "Device3": "00:0a:95:9d:68:18",
}

# Network Access Control List (ACL)
authorized_devices = {
    "00:0a:95:9d:68:16",  # Device1
    "00:0a:95:9d:68:17",  # Device2
}

# Simulated malware MAC address trying to access the network
malware_device = "00:0a:95:9d:68:99"  # Spoofed MAC address

def access_network(device_mac):
    """Simulates a device trying to access the network."""
    if device_mac in authorized_devices:
        print(f"Access granted to device with MAC: {device_mac}")
        return True
    else:
        print(f"Access denied for MAC: {device_mac}. Unauthorized access attempt detected!")
        return False

def simulate_normal_device_access():
    """Simulates legitimate devices accessing the network."""
    print("\n--- Normal Device Access Simulation Started ---")
    for _ in range(5):  # Limit number of access attempts for demonstration
        device = random.choice(list(devices.values()))
        access_network(device)
        time.sleep(random.randint(1, 3))  # Delay between accesses

def simulate_malware_attack():
    """Simulates malware trying to bypass NAC."""
    print("\n--- Malware Attack Simulation Started ---")
    for _ in range(5):  # Malware tries multiple times
        access_granted = access_network(malware_device)
        if not access_granted:
            print("Malware trying again...")
        time.sleep(1)

def simulate_dos_attack():
    """Simulates a Denial of Service attack."""
    print("\n--- DoS Attack Simulation Started ---")
    for _ in range(10):  # Rapid access attempts
        access_network(malware_device)
        time.sleep(0.5)

if __name__ == "__main__":
    simulate_normal_device_access()
    time.sleep(2)
    simulate_malware_attack()
    time.sleep(2)
    simulate_dos_attack()
