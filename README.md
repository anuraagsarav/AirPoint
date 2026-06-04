# AirPoint V2.0

AirPoint is a web-based remote control system that transforms a smartphone into a wireless touchpad, mouse, and presentation controller for a computer. It enables users to control their PC directly from a mobile browser without requiring a dedicated mobile application.

---

## Features

### Core Mouse Controls

- Real-time cursor movement
- Left-click support
- Right-click support
- Smooth scrolling
- Touch-based cursor control
- Arrow key navigation

### Connectivity

- QR Code connection system
- Automatic device pairing
- Local network communication
- Browser-based access
- No mobile application required

### Performance Enhancements

- Advanced cursor smoothing
- Dynamic mouse acceleration
- Gesture-based input processing
- Optimized cursor tracking
- Low-latency communication

### Presentation Mode

- Next slide navigation
- Previous slide navigation
- Presentation mode switching
- PowerPoint and slideshow support

### Security

- Session management
- Controlled device connections
- Secure Socket.IO communication

### User Interface

- Mobile-first responsive design
- Real-time connection status
- Clean and intuitive controls
- Touch-optimized interactions

---

## Technology Stack

### Backend

- Python
- Flask
- Flask-SocketIO

### Frontend

- HTML5
- CSS3
- JavaScript

### Communication

- WebSockets
- Socket.IO

### System Control

- PyAutoGUI

### Additional Libraries

- qrcode
- Pillow
- python-dotenv
- eventlet

---

## Project Architecture

AirPoint V2 follows a modular architecture that separates networking, input processing, device control, and user interface components.

### Architecture Layers

#### Controllers Layer

Responsible for executing actions on the host machine.

- Mouse Controller
- Keyboard Controller
- Presentation Controller

#### Input Engine Layer

Processes and optimizes incoming touch and gesture data.

- Movement Processing
- Scroll Processing
- Gesture Recognition
- Cursor Smoothing
- Mouse Acceleration

#### Networking Layer

Handles real-time communication between the mobile device and computer.

- Socket.IO Communication
- Event Handling
- Connection Management

#### Mode Management Layer

Controls application states.

- Normal Mouse Mode
- Presentation Mode

#### QR Connection Layer

Provides fast and easy device pairing.

- QR Generation
- QR Display Popup

---

## Project Structure

```text
AIRPOINT_V_2.0/
│
├── server/
│   │
│   ├── controllers/
│   │   ├── keyboard_controller.py
│   │   ├── mouse_controller.py
│   │   └── presentation_controller.py
│   │
│   ├── input_engine/
│   │   ├── acceleration_engine.py
│   │   ├── gesture_processor.py
│   │   ├── movement_processor.py
│   │   ├── scroll_processor.py
│   │   └── smoothing_engine.py
│   │
│   ├── modes/
│   │   └── mode_manager.py
│   │
│   ├── networking/
│   │   └── socket_handler.py
│   │
│   ├── qr/
│   │   ├── qr_generator.py
│   │   └── qr_popup.py
│   │
│   ├── session/
│   │   └── __init__.py
│   │
│   ├── app.py
│   └── config.py
│
├── ui/
│   │
│   ├── static/
│   │   ├── css/
│   │   │   └── styles.css
│   │   │
│   │   └── js/
│   │       └── controller.js
│   │
│   └── templates/
│       └── index.html
│
├── requirements.txt
│
└── venv/
```

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/anuraagsarav/Mouse_Pointer_Project.git
cd Mouse_Pointer_Project
```

### 2. Create a Virtual Environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Running AirPoint

### Start the Server

From the project root directory:

```bash
python server/app.py
```

The application will automatically:

- Start the Flask server
- Initialize Socket.IO communication
- Generate a connection QR code
- Display the QR code popup
- Wait for mobile device connections

When successful, the terminal will display a local network address similar to:

```text
http://192.168.x.x:5000
```

---

## Connecting Your Phone

### Method 1: QR Code (Recommended)

1. Launch AirPoint.
2. Wait for the QR code popup to appear.
3. Scan the QR code using your phone.
4. Open the detected URL.
5. Start controlling your computer.

### Method 2: Direct URL

Open the displayed local network address on your phone browser.

Example:

```text
http://192.168.1.10:5000
```

### Requirements

- Both devices must be connected to the same Wi-Fi network.
- The server must be running.
- Firewall settings must allow local network communication.

---

## Mouse Controls

| Action | Function |
|----------|----------|
| Touch Drag | Cursor Movement |
| Single Tap | Left Click |
| Right Click Button | Right Click |
| Scroll Gesture | Vertical Scrolling |
| Arrow Keys | Keyboard Navigation |

---

## Presentation Controls

Presentation Mode is designed for:

- Microsoft PowerPoint
- Google Slides
- LibreOffice Impress
- PDF Presentations

### Available Controls

| Action | Function |
|----------|----------|
| Previous Button | Previous Slide |
| Next Button | Next Slide |
| Mode Toggle | Switch Presentation Mode |
| Touch Input | Presentation Interaction |

---

## Configuration

Application settings are managed through:

```text
server/config.py
```

Optional environment variables:

```env
HOST=0.0.0.0
PORT=5000
SECRET_KEY=your_secret_key
```

---

## Dependencies

Main project dependencies include:

```txt
Flask
Flask-SocketIO
eventlet
pyautogui
qrcode
Pillow
python-dotenv
```

Install all dependencies using:

```bash
pip install -r requirements.txt
```

---

## Troubleshooting

### Phone Cannot Connect

- Ensure both devices are connected to the same Wi-Fi network.
- Verify the server is running.
- Check the displayed IP address.
- Allow Python through the Windows Firewall.

### QR Code Does Not Work

- Verify the QR code contains the correct IP address.
- Restart the server.
- Generate a new QR code.

### Cursor Does Not Move

- Ensure PyAutoGUI is installed correctly.
- Verify the application has permission to control the mouse.
- Check Socket.IO connection status.

### Connection Drops Frequently

- Verify network stability.
- Refresh the mobile browser.
- Restart the AirPoint server.

---

## Future Roadmap

### AirPoint V3

Planned improvements include:

- Multi-device support
- Media playback controls
- Advanced gesture recognition
- Custom key bindings
- User profiles
- Enhanced authentication
- File transfer support
- Dark mode improvements
- Device management dashboard
- Performance analytics
- Cross-platform desktop companion

---

## Learning Objectives

This project was developed to explore and understand:

- Flask web development
- Real-time WebSocket communication
- Socket.IO architecture
- Human-computer interaction
- Gesture-based input systems
- Mobile-first UI design
- Network-based remote control systems
- Software architecture and modular design

---

## License

This project is licensed under the MIT License.

---

## Author

**Anuraag S Sarav**

AirPoint V2.0 is a modular smartphone-to-PC remote control platform developed as part of a continuous learning journey in software engineering, networking, real-time systems, and user interface design.