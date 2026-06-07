from socket import inet_aton

from zeroconf import Zeroconf, ServiceInfo

from server.qr.qr_generator import get_local_ip


SERVICE_NAME = "AirPoint"
SERVICE_TYPE = "_http._tcp.local."

_zeroconf = None
_service_info = None


def start_mdns_service(port: int):

    global _zeroconf
    global _service_info

    ip_address = get_local_ip()

    _service_info = ServiceInfo(
        SERVICE_TYPE,
        f"{SERVICE_NAME}.{SERVICE_TYPE}",
        addresses=[inet_aton(ip_address)],
        port=port,
        properties={
            b"name": b"AirPoint",
            b"version": b"3.0"
        },
        server="airpoint.local."
    )

    _zeroconf = Zeroconf()

    _zeroconf.register_service(_service_info)

    print("\n=================================")
    print("AIRPOINT MDNS ACTIVE")
    print(f"IP       : {ip_address}")
    print(f"PORT     : {port}")
    print("=================================\n")