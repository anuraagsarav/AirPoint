def handle_event(data):

    event_type = data.get("event")

    print("\n======================")
    print(f"EVENT: {event_type}")
    print("======================")

    print(data)

    print()