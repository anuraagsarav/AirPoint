import secrets


SESSION_TOKEN = secrets.token_urlsafe(32)


def get_session_token():
    return SESSION_TOKEN


def is_valid_session_token(token):
    return bool(token) and secrets.compare_digest(str(token), SESSION_TOKEN)
