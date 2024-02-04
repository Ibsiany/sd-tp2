import threading
import queue

# Adjusted simulation for Ring Election Algorithm
class Device:
    def __init__(self, device_id, is_active=True):
        self.device_id = device_id
        self.is_active = is_active
        self.next_device = None

    def set_next_device(self, next_device):
        self.next_device = next_device

    def send_election_message(self, message):
        if self.is_active:
            message.append(self.device_id)
            print(f"Device {self.device_id} added itself to the message: {message}")
            self.next_device.receive_election_message(message)
        else:
            print(f"Device {self.device_id} is down. Passing message to next device.")
            self.next_device.send_election_message(message)

    def receive_election_message(self, message):
        # If message has returned to the initiator
        if message[0] == self.device_id:
            new_leader_id = max(message)
            print(f"Election complete. New leader is Device {new_leader_id}.")
            # Broadcast new leader to all devices (simplified for this simulation)
        else:
            self.send_election_message(message)

def simulate_ring_election(devices):
    for i, device in enumerate(devices):
        next_index = (i + 1) % len(devices)  # Circular reference to the next device
        device.set_next_device(devices[next_index])

    # Simulate device failure and election process
    failed_device_id = random.randint(0, len(devices) - 1)
    devices[failed_device_id].is_active = False
    print(f"Device {devices[failed_device_id].device_id} has failed.")

    # Start election from a random device
    initiator_id = random.randint(0, len(devices) - 1)
    print(f"Device {devices[initiator_id].device_id} noticed the failure and is starting the election.")
    devices[initiator_id].send_election_message([devices[initiator_id].device_id])

# Create devices
device_count = 4  # Minimum of 4 devices
devices = [Device(i) for i in range(device_count)]

# Simulate the ring election
simulate_ring_election(devices)

# Note: This simulation runs once to demonstrate the election process. In a real system, this would be part of a continuous monitoring and election mechanism.
