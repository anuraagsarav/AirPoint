import socket


# =========================================
# GET LOCAL IP
# =========================================

def get_local_ip():

    sock = socket.socket(

        socket.AF_INET,

        socket.SOCK_DGRAM

    )

    try:

        sock.connect(

            ("8.8.8.8", 80)

        )

        ip = sock.getsockname()[0]

    except Exception:

        ip = "127.0.0.1"

    finally:

        sock.close()

    return ip


# =========================================
# GENERATE CONNECTION URL
# =========================================

def generate_connection_url(port, token=None, server_id=None):

    ip = get_local_ip()

    url = f"http://{ip}:{port}"

    params = []

    if token:
        params.append(f"token={token}")

    if server_id:
        params.append(f"server_id={server_id}")

    if params:
        return f"{url}?{'&'.join(params)}"

    return url
