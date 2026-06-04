HOST ="0.0.0.0"
PORT = 5000
DEBUG = False

# ==================================
# SECURITY SETTINGS
# ==================================

DEVELOPER_MODE = False

TRUSTED_DEVICES_JSON = "trusted_devices.json"
TRUSTED_DEVICES_ENC = "trusted_devices.enc"
SECURITY_KEY_FILE = "security.key"
SECURITY_LOG_FILE = "logs/security.log"
SECURITY_LOG_DETAILS = False

# ==================================
# MOVEMENT SETTINGS
# ==================================

BASE_SENSITIVITY = 2.2
SMOOTHING_ALPHA = 0.6
ACCELERATION_FACTOR = 0.02
MAX_ACCELERATION = 3.5
DEADZONE = 0.5

TAP_MAX_DURATION = 180
TAP_MAX_MOVEMENT = 12

SCROLL_SENSITIVITY = 1.2
