from nicegui import ui

from components.header import build_header
from components.sidebar import build_sidebar
from components.analytics import build_analytics
from components.chat_window import build_chat_window


def chat_page():
    # ---------------- Header ---------------- #
    build_header()

    # ---------------- Main Layout ---------------- #
    with ui.row().classes(
    "w-full h-screen no-wrap items-stretch overflow-hidden"
    ):

        # Left Sidebar
        build_sidebar()

        # Middle Chat
        chat_window = build_chat_window()

        # Right Analytics Panel
        analytics = build_analytics()

        # Connect Chat Window with Analytics
        chat_window.set_analytics(analytics)