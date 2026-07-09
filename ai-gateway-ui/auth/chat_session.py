import uuid

SESSION_ID = None


def create_session():
    """
    Create a brand new chat session.
    """
    global SESSION_ID

    SESSION_ID = uuid.uuid4().hex

    return SESSION_ID


def get_session():
    """
    Return current session.
    Create one if it doesn't exist.
    """
    global SESSION_ID

    if SESSION_ID is None:
        SESSION_ID = create_session()

    return SESSION_ID


def new_session():
    """
    Generate a fresh session.
    """
    return create_session()


def set_session(session_id: str):
    """
    Set the active session.
    Used when opening an old conversation.
    """
    global SESSION_ID

    SESSION_ID = session_id


def clear_session():
    """
    Clear the current session.
    """
    global SESSION_ID

    SESSION_ID = None