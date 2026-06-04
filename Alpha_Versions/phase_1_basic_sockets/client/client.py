import socket

from phase_1_basic_sockets.shared.config import PORT

SERVER_IP = "192.168.1.100"

print("Starting client...")


# Create TCP Socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# Connect to the server
client_socket.connect((SERVER_IP, PORT))
print(f"Client connect to server at {SERVER_IP}...")


# Create and encode message
message = "Hello from client!"
encoded_message = message.encode("utf-8")


# Send message to the server
client_socket.send(encoded_message)
print("Message sent to server.")


# Close the socket
client_socket.close()

print("Client is shutting down...")