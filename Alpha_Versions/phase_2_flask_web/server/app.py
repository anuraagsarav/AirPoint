from flask import Flask

from phase_2_flask_web.shared.config import HOST, PORT, DEBUG
from phase_2_flask_web.server.routes import register_routes


# Create Flask application
app = Flask(__name__)


# Register all routes
register_routes(app)


# Start Flask server
if __name__ == "__main__":

    app.run(
        host=HOST,
        port=PORT,
        debug=DEBUG
    )