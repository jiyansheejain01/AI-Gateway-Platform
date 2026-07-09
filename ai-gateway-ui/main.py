from nicegui import ui

from pages.login import login_page
from pages.register import register_page
from pages.chat import chat_page

"""
ui.colors(
    primary="#2563eb",
    secondary="#64748b",
    accent="#3b82f6",
    positive="#10b981",
    negative="#ef4444",
    warning="#f59e0b",
)
"""

@ui.page("/")
def home():
    login_page()


@ui.page("/register")
def register():
    register_page()


@ui.page("/chat")
def chat():
    chat_page()


ui.run(
    title="AI Gateway",
    reload=True,
    storage_secret="my_super_secret_key",
)