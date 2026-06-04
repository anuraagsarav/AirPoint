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

def generate_connection_url(port, token=None):

    ip = get_local_ip()

    url = f"http://{ip}:{port}"

    if token:
        return f"{url}?token={token}"

    return url
