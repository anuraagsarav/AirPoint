# =========================================
# ACTIVE DEVICE SESSION
# =========================================

active_device = {

    "sid": None,
    "ip": None,
    "connected": False

}


# =========================================
# REGISTER DEVICE
# =========================================

def register_device(sid, ip_address):

    global active_device


    previous_sid = active_device["sid"]


    active_device = {

        "sid": sid,
        "ip": ip_address,
        "connected": True

    }


    return previous_sid


# =========================================
# REMOVE DEVICE
# =========================================

def remove_device(sid):

    global active_device


    if active_device["sid"] == sid:

        active_device = {

            "sid": None,
            "ip": None,
            "connected": False

        }