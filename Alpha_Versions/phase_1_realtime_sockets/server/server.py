import socket

from phase_1_realtime_sockets.shared.config import (HOST, PORT, BUFFER_SIZE, ENCODING)
from phase_1_realtime_sockets.server.packet_handler import handle_packet
from phase_1_realtime_sockets.server.connection_manager import print_connection_info

print("Starting server...")

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((HOST, PORT))

server_socket.listen()

print(f"Server listening on port: {PORT}")

client_socket, client_address = server_socket.accept()
print_connection_info(client_address)

while True:

    data = client_socket.recv(BUFFER_SIZE)

    if not data:
        print("Client disconnected.")
        break

    decoded_data = data.decode(ENCODING)

    handle_packet(decoded_data)

client_socket.close()
server_socket.close()

print("Server shut down.")

