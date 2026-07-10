from nicegui import ui

from pages.login import login_page
from pages.register import register_page
from pages.chat import chat_page

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