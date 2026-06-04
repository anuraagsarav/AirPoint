def handle_event(data):

    event_type = data.get("event")


    if event_type == "move":

        dx = data.get("dx")
        dy = data.get("dy")

        print(
            f"MOVE EVENT | dx={dx} | dy={dy}"
        )