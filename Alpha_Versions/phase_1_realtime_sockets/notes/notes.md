# Phase 1 — Persistent Real-Time Socket Architecture Notes

# Objective

The goal of Phase 1.1 was to move from simple one-time communication to continuous real-time communication.

This phase focused on:

- persistent socket connections
- continuous event streaming
- JSON packet communication
- event-driven architecture
- packet serialization
- protocol design
- server loops
- structured packet handling

This phase represents the transition from basic networking to real-time systems architecture.

---

# What Was Built

A persistent TCP communication system where:

- client connects once
- connection remains open
- client continuously sends event packets
- server continuously receives packets
- server processes events in real-time

Architecture:

CLIENT ↔ PERSISTENT TCP CONNECTION ↔ SERVER

---

# Folder Structure

```text
phase1_realtime_sockets/
│
├── server/
│   ├── server.py
│   ├── packet_handler.py
│   └── connection_manager.py
│
├── client/
│   ├── client.py
│   └── event_generator.py
│
├── shared/
│   ├── config.py
│   └── protocol.py
│
├── notes/
│   └── realtime_notes.md
│
└── logs/
    └── server.log
```

---

# Difference Between Phase 1 and Phase 1.1

# Phase 1

```text
connect
send one message
disconnect
```

---

# Phase 1.1

```text
connect once
stay connected
continuously exchange packets
```

This architecture is used in real-time systems.

---

# Persistent Connections

A persistent connection remains active after initial communication.

Benefits:
- lower latency
- faster communication
- continuous event streaming
- reduced connection overhead

Real-time systems rely heavily on persistent connections.

---

# Event-Driven Architecture

The system operates using events.

Examples:
- move
- click
- scroll

Each user action becomes an event packet.

Example:

```json
{
  "event": "move",
  "dx": 10,
  "dy": -5
}
```

---

# Communication Flow

```text
CLIENT
   ↓
generate event
   ↓
convert dict → JSON
   ↓
encode JSON → bytes
   ↓
send over TCP
   ↓
SERVER receives bytes
   ↓
decode bytes → JSON string
   ↓
deserialize JSON → dict
   ↓
process event
```

---

# JSON Communication

JSON was used because it is:
- human readable
- structured
- language independent
- widely used in networking systems

---

# Serialization

Serialization converts data into transferable format.

Example:

```python
json.dumps(data)
```

Converts:
- Python dictionary
→ JSON string

---

# Deserialization

Deserialization converts serialized data back into usable form.

Example:

```python
json.loads(data)
```

Converts:
- JSON string
→ Python dictionary

---

# Event Loop

The server continuously processes incoming packets using:

```python
while True:
```

This creates:
- continuous packet handling
- real-time communication behavior

This architecture is common in:
- game servers
- chat systems
- WebSocket servers
- live streaming systems

---

# Packet Handler

packet_handler.py was introduced to separate responsibilities.

Responsibilities:
- parse packets
- validate packets
- identify event types
- process commands

This follows separation of concerns principle.

---

# Separation of Concerns

The project structure separates:
- networking logic
- packet processing
- event generation
- protocol definitions

Benefits:
- cleaner architecture
- scalability
- maintainability
- easier debugging

---

# Protocol Design

A communication protocol defines:
- packet structure
- event names
- expected fields
- communication rules

Example protocol packet:

```json
{
  "event": "click",
  "button": "left"
}
```

---

# Event Types

Current events:
- move
- click
- scroll

Future events may include:
- drag
- keyboard
- gestures
- multitouch

---

# Defensive Programming

The server validates packets before processing.

Example:
- checking missing fields
- handling invalid JSON

This prevents server crashes from malformed data.

---

# TCP Stream Concept

Important concept:

TCP is stream-oriented, NOT message-oriented.

This means:
- one recv() call may contain partial messages
- multiple messages may arrive together

This introduces:
- framing problems
- packet boundary issues

These are important real-world networking challenges.

---

# Buffer Size

recv(1024)

Means:
- receive maximum 1024 bytes at once

Larger packets may require multiple recv() operations.

---

# Simulated Event Generation

event_generator.py simulates:
- mouse movement
- clicks
- scrolling

This prepares architecture for future real browser touch events.

---

# Real-World Systems Using Similar Architecture

These concepts are used in:
- remote desktop systems
- multiplayer games
- Discord
- SSH
- collaborative editors
- WebSocket applications
- live streaming systems

---

# Important Engineering Concepts Learned

- persistent socket systems
- event streams
- protocol architecture
- serialization/deserialization
- real-time communication
- event-driven systems
- separation of concerns
- packet processing
- stateful communication

---

# Key Takeaways

Phase 1.1 transformed the project from:
- basic networking demo

into:
- real-time communication architecture

The system can now:
- maintain persistent connections
- stream events continuously
- process structured packets
- handle event-based communication

This phase provides the foundation required for:
- Flask browser communication
- WebSockets
- touch event handling
- real-time mouse control
- gesture systems
- low-latency communication