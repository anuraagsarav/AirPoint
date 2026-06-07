import threading

from flask import Flask
from flask import abort
from flask import request
from flask import render_template

from flask_socketio import SocketIO

from server.config import (
    HOST,
    PORT,
    DEBUG,
    SHOW_NETWORK_STATS
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
from server.security.bootstrap import (
    initialize_security
)
from server.security.security_logger import log_warning
from server.security.session_token import (
    get_session_token,
    is_valid_session_token
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


initialize_security()

register_socket_events(socketio)


@app.before_request
def validate_control_request_token():

    if request.endpoint == "static" or request.path == "/favicon.ico":
        return None

    token = request.args.get("token")

    if not is_valid_session_token(token):
        log_warning(
            "Invalid session token",
            ip_address=request.remote_addr,
            path=request.path
        )
        abort(403)

    return None


@app.route('/favicon.ico')
def favicon():
    return '', 204


@app.route("/")
def home():

    return render_template(
        "index.html",
        show_network_stats=SHOW_NETWORK_STATS
    )


if __name__ == "__main__":

    connection_url = generate_connection_url(
        PORT,
        get_session_token()
    )


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

