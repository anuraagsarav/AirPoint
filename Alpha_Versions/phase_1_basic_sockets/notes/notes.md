# Phase 1 — Raw Socket Communication Notes

# Objective

The goal of Phase 1 was to understand the fundamentals of networking and socket communication using Python.

This phase focused on:

- TCP communication
- Client-server architecture
- IP addresses and ports
- Socket lifecycle
- Packet transmission basics
- Encoding and decoding data
- Basic networking debugging

No mouse control or browser communication was implemented in this phase.

---

# What Was Built

A basic TCP communication system where:

- A Python server listens for incoming connections
- A Python client connects to the server
- The client sends a message
- The server receives and prints the message

Architecture:

CLIENT → TCP SOCKET → SERVER

---

# Folder Structure

```text
phase1_basic_sockets/
│
├── server/
│   └── server.py
│
├── client/
│   └── client.py
│
├── shared/
│   └── config.py
│
└── notes/
    └── networking_notes.md
```

---

# Core Networking Concepts Learned

# 1. Client-Server Architecture

A client-server system consists of:

Client:
- initiates communication
- sends requests

Server:
- waits for connections
- processes incoming data

In this project:

- client.py = Client
- server.py = Server

---

# 2. IP Address

An IP address identifies a device on a network.

Example:

```text
192.168.1.5
```

The client uses the server IP address to connect.

---

# 3. Port

A port identifies a specific application running on a device.

Example:

```text
192.168.1.5:5000
```

- 192.168.1.5 → device
- 5000 → application port

---

# 4. TCP Protocol

TCP stands for:

Transmission Control Protocol

Features:
- reliable
- ordered delivery
- connection-oriented
- retransmission support

TCP ensures:
- packets arrive correctly
- packets arrive in order

---

# 5. Socket

A socket is a communication endpoint used for network communication.

Client socket:
- connects to server

Server socket:
- listens for incoming connections

---

# Socket Lifecycle

The server follows this lifecycle:

```text
CREATE SOCKET
    ↓
BIND
    ↓
LISTEN
    ↓
ACCEPT
    ↓
RECEIVE DATA
    ↓
CLOSE CONNECTION
```

---

# Important Python Socket Functions

# socket.socket()

Creates a socket object.

Example:

```python
socket.socket(socket.AF_INET, socket.SOCK_STREAM)
```

---

# socket.AF_INET

Specifies IPv4 addressing.

---

# socket.SOCK_STREAM

Specifies TCP communication.

---

# bind()

Associates the socket with:
- IP address
- port number

---

# listen()

Puts server into listening mode.

The OS starts accepting incoming connection requests.

---

# accept()

Waits for client connection.

Returns:
- client socket
- client address

This is a blocking operation.

---

# recv()

Receives bytes from the socket.

Example:

```python
data = client_socket.recv(1024)
```

1024 = maximum bytes to receive at once.

---

# send()

Sends bytes through socket.

---

# Encoding and Decoding

Networking transmits bytes, not Python strings.

String → Bytes:

```python
message.encode("utf-8")
```

Bytes → String:

```python
data.decode("utf-8")
```

---

# Packet Flow

The communication flow:

```text
CLIENT
   ↓
encode string → bytes
   ↓
TCP packet creation
   ↓
network transfer
   ↓
SERVER receives bytes
   ↓
decode bytes → string
```

---

# TCP Handshake

TCP establishes a connection using a 3-way handshake:

```text
CLIENT → SYN
SERVER → SYN-ACK
CLIENT → ACK
```

Connection becomes established after handshake completes.

---

# Blocking Operations

Certain socket functions pause program execution until something happens.

Examples:
- accept()
- recv()

These are called blocking operations.

---

# Common Errors and Debugging

# ConnectionRefusedError

Causes:
- server not running
- wrong IP
- wrong port

---

# Firewall Issues

Windows Firewall may block Python networking.

Allow Python access through firewall.

---

# Address Already In Use

Occurs when:
- same port is already occupied

Possible fixes:
- wait few seconds
- change port number

---

# Important Engineering Concepts Learned

- basic distributed systems
- networking fundamentals
- socket communication
- TCP reliability
- byte streams
- packet transmission
- blocking I/O
- client-server architecture

---

# Real-World Applications

These same concepts are used in:
- multiplayer games
- chat applications
- SSH
- APIs
- remote desktop software
- IoT systems
- streaming systems

---

# Key Takeaways

Phase 1 established the networking foundation for the remote mouse project.

The system can now:
- create TCP connections
- transmit data between devices
- receive and decode packets
- understand socket lifecycle

This foundation is required before implementing:
- persistent connections
- real-time communication
- browser communication
- WebSockets
- mouse event handling