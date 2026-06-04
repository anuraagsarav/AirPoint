import socket

from phase_1_basic_sockets.shared.config import HOST, PORT, BUFFER_SIZE

print("Server is starting...")


# Create TCP Socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# Bind the socket to the host and port
server_socket.bind((HOST, PORT))


# Listen for incoming connections
server_socket.listen()
print(f"Server is listenin on {PORT}....")


# Wait for a client to connect and accept the connection
client_socket, client_address = server_socket.accept()
print(f"Client {client_address} has connected.")


# Receive data from the client
data = client_socket.recv(BUFFER_SIZE)


# Decode the received data
decoded_data = data.decode("utf-8")
print(f"Recceived data from clinet: {decoded_data}")

# Close the sockets
client_socket.close()
server_socket.close()

print("Server is shutting down...")