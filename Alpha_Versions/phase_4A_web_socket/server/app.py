from flask import Flask
from flask import render_template

from flask_socketio import SocketIO

from phase_3_web_socket.shared.config import (
    HOST,
    PORT,
    DEBUG
)

from phase_4A_web_socket.server.socket_handler import (
    register_socket_events
)


app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../static"
)


socketio = SocketIO(app)


register_socket_events(socketio)


@app.route("/")
def home():

    return render_template("index.html")


if __name__ == "__main__":

    socketio.run(
        app,
        host=HOST,
        port=PORT,
        debug=DEBUG
    )