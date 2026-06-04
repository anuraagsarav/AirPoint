from phase_5B.server.app import socketio
from phase_5B.server.app import app


if __name__ == "__main__":

    socketio.run(
        app,
        host="0.0.0.0",
        port=5000,
        debug=False
    )