from flask import ( render_template, jsonify, request )
from phase_2_flask_web.server.event_handler import handle_event

def register_routes(app):

    @app.route("/")
    def home():

        return render_template("index.html")
    
    @app.route("/event", methods=["POST"])
    def receive_event():

        data = request.get_json()

        event_name = data.get("event")

        handle_event(event_name)

        return jsonify({"status": "success", "event" : event_name}) 