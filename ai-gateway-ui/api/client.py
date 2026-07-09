import requests

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


# --------------------------------------------------
# Chat
# --------------------------------------------------

def chat(prompt: str, token: str, session_id: str):
    return requests.post(
        f"{BASE_URL}/chat",
        headers={
            "Authorization": f"Bearer {token}",
        },
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
    return requests.get(
        f"{BASE_URL}/conversations",
        headers={
            "Authorization": f"Bearer {token}",
        },
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
    return requests.delete(
        f"{BASE_URL}/conversation/{session_id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
        timeout=60,
    )