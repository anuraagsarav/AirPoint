import threading

from flask import Flask
from flask import render_template

from flask_socketio import SocketIO

from server.config import (
    HOST,
    PORT,
    DEBUG
)

from server.networking.socket_handler import (
    register_socket_events
)

from server.qr.qr_generator import (
    generate_connection_url
)

from server.qr.qr_popup import (
    show_qr_popup
)

app = Flask(
    __name__,
    template_folder="../ui/templates",
    static_folder="../ui/static"
)


socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode="threading",
    logger=False,
    engineio_logger=False
)


register_socket_events(socketio)


@app.route("/")
def home():

    return render_template("index.html")


if __name__ == "__main__":

    connection_url = generate_connection_url(PORT)


    # =====================================
    # START QR POPUP THREAD
    # =====================================

    popup_thread = threading.Thread(

        target=show_qr_popup,

        args=(connection_url,),

        daemon=True

    )

    popup_thread.start()


    # =====================================
    # START SERVER
    # =====================================

    socketio.run(

        app,

        host=HOST,

        port=PORT,

        debug=DEBUG,

        allow_unsafe_werkzeug=True

    )

