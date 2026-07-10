from nicegui import context

sidebar_refresh = {}


def _client_id():
    return context.client.id


def set_sidebar_refresh(refresh_func):
    print("SET SIDEBAR:", context.client.id)
    sidebar_refresh[_client_id()] = refresh_func


def refresh_sidebar():
    print("REFRESH:", context.client.id)
    func = sidebar_refresh.get(_client_id())

    if func:
        func()