TOKEN = None
USERNAME = None


def save_session(token: str, username: str):
    global TOKEN, USERNAME
    TOKEN = token
    USERNAME = username


def get_token():
    return TOKEN


def get_username():
    return USERNAME


def logout():
    global TOKEN, USERNAME
    TOKEN = None
    USERNAME = None