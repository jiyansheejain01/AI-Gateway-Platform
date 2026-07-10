sidebar_refresh = None


def set_sidebar_refresh(refresh_func):
    global sidebar_refresh
    sidebar_refresh = refresh_func


def refresh_sidebar():
    if sidebar_refresh:
        sidebar_refresh()