from nicegui import app


def save_session(token: str, username: str):
    app.storage.user["token"] = token
    app.storage.user["username"] = username


def get_token():
    return app.storage.user.get("token")


def get_username():
    return app.storage.user.get("username")


def logout():
    app.storage.user.clear()