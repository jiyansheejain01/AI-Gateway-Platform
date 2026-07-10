from nicegui import context

chat_windows = {}


def _client_id():
    return context.client.id


def set_chat_window(window):
    print("SET CHAT:", context.client.id)
    chat_windows[_client_id()] = window


def get_chat_window():
    print("GET CHAT:", context.client.id)
    return chat_windows.get(_client_id())