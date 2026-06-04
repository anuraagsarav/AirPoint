import socket
import json
import time

from phase_1_realtime_sockets.shared.config import (PORT, ENCODING)
from phase_1_realtime_sockets.client.event_generator import generat_fake_event

SERVER_IP = "192.168.1.100"

print("Starting client...")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((SERVER_IP, PORT))
print(f"Connected to server at {SERVER_IP}:{PORT}")

while True:

    event = generat_fake_event()

    json_packet = json.dumps(event)
    encoded_packet = json_packet.encode(ENCODING)

    client_socket.send(encoded_packet)

    print(f"Sent: {json_packet}")

    time.sleep(1)

