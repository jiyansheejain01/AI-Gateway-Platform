import requests
from auth.session import (
    get_refresh_token,
    save_session,
    get_username,
)

BASE_URL = "http://127.0.0.1:8000/api/v1"


# --------------------------------------------------
# Authentication
# --------------------------------------------------

def login(username: str, password: str):
    return requests.post(
        f"{BASE_URL}/auth/login",
        json={
            "username": username,
            "password": password,
        },
        timeout=60,
    )


def register(username: str, email: str, password: str):
    return requests.post(
        f"{BASE_URL}/auth/register",
        json={
            "username": username,
            "email": email,
            "password": password,
        },
        timeout=60,
    )

def refresh_access_token():

    response = requests.post(
        f"{BASE_URL}/auth/refresh",
        json={
            "refresh_token": get_refresh_token(),
        },
        timeout=60,
    )

    if response.status_code != 200:
        return None

    data = response.json()

    save_session(
        data["access_token"],
        get_refresh_token(),
        get_username(),
    )

    return data["access_token"]

def authorized_request(method, url, token, **kwargs):

    headers = kwargs.pop("headers", {})
    headers["Authorization"] = f"Bearer {token}"

    response = requests.request(
        method,
        url,
        headers=headers,
        **kwargs,
    )

    if response.status_code != 401:
        return response

    new_token = refresh_access_token()

    if new_token is None:
        return response

    headers["Authorization"] = f"Bearer {new_token}"

    return requests.request(
        method,
        url,
        headers=headers,
        **kwargs,
    )

# --------------------------------------------------
# Chat
# --------------------------------------------------

def chat(prompt: str, token: str, session_id: str):
    return authorized_request(
        "POST",
        f"{BASE_URL}/chat",
        token,
        json={
            "session_id": session_id,
            "prompt": prompt,
        },
        timeout=300,
    )


# --------------------------------------------------
# Conversations
# --------------------------------------------------

def get_conversations(token: str):
    return authorized_request(
        "GET",
        f"{BASE_URL}/conversations",
        token,
        timeout=60,
    )


def get_conversation(session_id: str, token: str):
    return requests.get(
        f"{BASE_URL}/conversation/{session_id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
        timeout=60,
    )


def delete_conversation(session_id: str, token: str):
    return authorized_request(
        "DELETE",
        f"{BASE_URL}/conversation/{session_id}",
        token,
        timeout=60,
    )