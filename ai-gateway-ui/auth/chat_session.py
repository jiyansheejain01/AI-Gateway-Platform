import uuid
from nicegui import app


def create_session():
    session_id = uuid.uuid4().hex
    app.storage.user["session_id"] = session_id
    return session_id


def get_session():
    session_id = app.storage.user.get("session_id")

    if session_id is None:
        session_id = create_session()

    return session_id


def new_session():
    return create_session()


def set_session(session_id: str):
    app.storage.user["session_id"] = session_id


def clear_session():
    app.storage.user.pop("session_id", None)