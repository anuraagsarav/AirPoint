# AirPoint

> A browser-based wireless remote control system that transforms a smartphone into a touchpad, mouse, and presentation controller for a Windows PC.

AirPoint allows users to control their computer directly from a mobile browser without installing a dedicated mobile application. The project evolved from low-level TCP socket experiments into a secure real-time remote control platform featuring QR-based pairing, trusted-device authentication, and encrypted device management.

---

## 🚀 Features

### 🖱️ Mouse Control
- Smooth touchpad-style cursor movement
- Left-click support
- Right-click support
- Dynamic cursor acceleration
- Movement smoothing
- Deadzone filtering for improved precision

### 📜 Scrolling
- Two-finger scrolling gestures
- Smooth scrolling experience

### 🎤 Presentation Mode
- Start slideshow
- Exit slideshow
- Next slide
- Previous slide
- Presentation cursor control

### 🌐 Connectivity
- Browser-based controller
- Local Wi-Fi communication
- QR code pairing
- Real-time Socket.IO communication
- Automatic transport fallback support

### 🔒 Security (V3)
- Session-token authentication
- Trusted-device approval workflow
- Persistent device identification
- Trusted-device management panel
- Encrypted trusted-device database
- Fernet encryption
- Windows DPAPI-protected encryption keys

---

# 📈 Project Evolution

## Alpha Development Journey

The project was developed incrementally to explore networking, real-time communication, desktop automation, and security engineering.

| Phase | Objective | Core Technology |
|---------|-----------|----------------|
| Phase 1 | Single TCP communication | Python Sockets |
| Phase 1 Realtime | Continuous event streaming | TCP + JSON |
| Phase 2 | Browser-based control | Flask + HTTP |
| Phase 3 | Real-time communication | Flask-SocketIO |
| Phase 4A | Web architecture refinement | Templates & Static Assets |
| Phase 5A | Real cursor control | PyAutoGUI |
| Phase 5B | Smart input processing | Smoothing & Acceleration |

---

## Phase 1 — Basic TCP Sockets

### Goal
Establish communication between a client and server.

### Concepts Explored
- TCP networking
- Client-server architecture
- Socket lifecycle management

### Features
- Single TCP connection
- Message transmission
- Message reception

---

## Phase 1 Realtime — Event Streaming

### Goal
Convert one-time messages into continuous event streams.

### Concepts Explored
- JSON serialization
- Continuous packet transmission
- Event-driven architecture
- Packet handling systems

### Features
- Realtime event generation
- JSON packet streaming
- Packet processing layer

---

## Phase 2 — Flask Web

### Goal
Replace the desktop client with a web browser.

### Concepts Explored
- Flask web applications
- HTTP communication
- REST-style APIs
- JSON-based requests

### Features
- Browser-based interface
- Event submission through HTTP POST
- Flask routing

---

## Phase 3 — WebSocket Communication

### Goal
Enable low-latency bidirectional communication.

### Concepts Explored
- WebSockets
- Flask-SocketIO
- Event emitters
- Persistent connections

### Features
- Realtime event communication
- Connect/disconnect handling
- Bidirectional messaging

---

## Phase 4A — Architecture Refinement

### Goal
Improve maintainability and project structure.

### Concepts Explored
- Frontend/backend separation
- Static asset organization
- Template-based architecture

### Features
- Templates directory
- Static assets directory
- Cleaner code organization

---

## Phase 5A — Real Mouse Control

### Goal
Translate network events into operating-system actions.

### Concepts Explored
- Desktop automation
- OS-level cursor control
- Input mapping

### Features
- Actual cursor movement
- PyAutoGUI integration

---

## Phase 5B — Smart Input Engine

### Goal
Create a natural touchpad experience.

### Concepts Explored
- Signal smoothing
- Deadzone filtering
- Dynamic acceleration
- Input processing algorithms

### Features
- Cursor smoothing
- Dynamic acceleration
- Left click
- Right click
- Precision improvements

---

# 🏁 AirPoint Versions

## AirPoint V1.0

### Features
- Browser-based touchpad
- Cursor movement
- Left click
- Right click
- Movement smoothing
- Dynamic acceleration

### Connection Method

```text
Phone Browser
      ↓
Socket.IO
      ↓
AirPoint Server
      ↓
PyAutoGUI
```

### Technologies
- Flask
- Flask-SocketIO
- HTML
- CSS
- JavaScript
- PyAutoGUI

---

## AirPoint V2.0

### New Features
- QR code pairing
- Two-finger scrolling
- Presentation mode
- Network latency monitoring
- Adaptive movement timing
- Socket.IO CDN failover

### Presentation Controls
- Start presentation
- Exit presentation
- Next slide
- Previous slide

### Improvements
- Improved connection reliability
- Better deployment resilience
- Enhanced user experience

---

## AirPoint V3.0

### Security Features
- Session-token authentication
- Device authorization
- Trusted-device approval popup
- Persistent device identity
- Trusted-device management panel
- Encrypted trusted-device database
- Fernet encryption
- Windows DPAPI key protection

### Connection Flow

```text
PC Starts
    ↓
Generate Session Token
    ↓
Generate QR Code
    ↓
Phone Scans QR
    ↓
Open Browser UI
    ↓
Socket.IO Connection
    ↓
Token Validation
    ↓
Trusted Device Check
    ↓
Approval (If Required)
    ↓
Remote Control Active
```

### Security Flow

```text
Session Token
      ↓
Device ID Verification
      ↓
Trusted Device Validation
      ↓
Approval Workflow
      ↓
Encrypted Storage
      ↓
DPAPI-Protected Encryption Keys
```

---

# 🏗️ Technologies Used

## Backend
- Python
- Flask
- Flask-SocketIO

## Frontend
- HTML
- CSS
- JavaScript
- Socket.IO Client

## Desktop Integration
- PyAutoGUI
- Tkinter

## Security
- Cryptography (Fernet)
- Windows DPAPI

## Utilities
- qrcode
- Pillow

---

# 📂 Project Structure

```text
AirPoint/
│
├── Alpha_Versions/
│   ├── phase_1_basic_sockets/
│   ├── phase_1_realtime_sockets/
│   ├── phase_2_flask_web/
│   ├── phase_3_web_socket/
│   ├── phase_4A_web_socket/
│   ├── phase_5A/
│   └── phase_5B/
│
├── AirPoint_V1.0/
├── AirPoint_V2.0/
├── AirPoint_V3.0/
│
└── README.md
```

---

# 🧠 Engineering Concepts Demonstrated

### Networking
- TCP Sockets
- Client-Server Architecture
- HTTP Communication
- WebSockets
- Socket.IO

### Software Engineering
- Modular Architecture
- Event-Driven Design
- Real-Time Systems
- Input Processing Pipelines

### Security Engineering
- Session Authentication
- Device Authorization
- Encryption
- Secure Key Management
- Trusted Device Systems

### Desktop Automation
- Mouse Control
- Gesture Processing
- Presentation Automation

---

# 🔮 Future Roadmap

## AirPoint V4
**Task Switcher Mode**

- Window-switching interface
- Touch-first application navigation
- Productivity-focused controls

## AirPoint V5
**Advanced Workspace Control**

- Multi-monitor awareness
- Smart desktop navigation
- Context-aware controls
- Enhanced productivity features

---

# 👨‍💻 Author

**Anuraag S Sarav**

AirPoint is a personal engineering project developed to explore and combine:

- Networking
- Real-time communication
- Desktop automation
- Web technologies
- Security engineering

The project demonstrates the complete progression from low-level socket programming to a secure, production-style remote control platform.

---

⭐ If you found this project interesting, consider giving it a star.