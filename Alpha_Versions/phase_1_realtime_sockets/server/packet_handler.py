import json

def handle_packet(packet_data):

    try:
        
        packet = json.loads(packet_data)

        event_type = packet.get("event")

        print(f"Received event: {event_type}")

        print(packet)

    except json.JSONDecodeError:

        print("Invalid packet data received.")