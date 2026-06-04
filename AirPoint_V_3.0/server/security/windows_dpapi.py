import ctypes
from ctypes import wintypes


CRYPTPROTECT_UI_FORBIDDEN = 0x01


class DATA_BLOB(ctypes.Structure):
    _fields_ = [
        ("cbData", wintypes.DWORD),
        ("pbData", ctypes.POINTER(ctypes.c_char))
    ]


crypt32 = ctypes.windll.crypt32
kernel32 = ctypes.windll.kernel32


def protect_data(data):
    return _crypt_protect_data(data, protect=True)


def unprotect_data(data):
    return _crypt_protect_data(data, protect=False)


def _crypt_protect_data(data, protect):
    input_blob = _bytes_to_blob(data)
    output_blob = DATA_BLOB()

    if protect:
        success = crypt32.CryptProtectData(
            ctypes.byref(input_blob),
            None,
            None,
            None,
            None,
            CRYPTPROTECT_UI_FORBIDDEN,
            ctypes.byref(output_blob)
        )
    else:
        success = crypt32.CryptUnprotectData(
            ctypes.byref(input_blob),
            None,
            None,
            None,
            None,
            CRYPTPROTECT_UI_FORBIDDEN,
            ctypes.byref(output_blob)
        )

    if not success:
        raise OSError(ctypes.GetLastError())

    try:
        return ctypes.string_at(output_blob.pbData, output_blob.cbData)
    finally:
        kernel32.LocalFree(output_blob.pbData)


def _bytes_to_blob(data):
    buffer = ctypes.create_string_buffer(data, len(data))

    blob = DATA_BLOB(
        len(data),
        ctypes.cast(buffer, ctypes.POINTER(ctypes.c_char))
    )

    blob._buffer = buffer

    return blob
