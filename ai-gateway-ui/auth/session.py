from nicegui import app


def save_session(
    access_token: str,
    refresh_token: str,
    username: str,
):
    app.storage.user["token"] = access_token
    app.storage.user["refresh_token"] = refresh_token
    app.storage.user["username"] = username

def get_token():
    return app.storage.user.get("token")

def get_refresh_token():
    return app.storage.user.get("refresh_token")

def get_username():
    return app.storage.user.get("username")


def logout():
    app.storage.user.clear()