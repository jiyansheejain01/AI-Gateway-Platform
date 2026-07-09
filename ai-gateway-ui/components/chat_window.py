from urllib import response

from nicegui import ui
from api.client import (
    chat,
    get_conversation,
)
from auth.session import get_token
from components.message import MessageBubble
from auth.chat_session import (
    get_session,
    new_session,
    set_session,
)
import traceback

class ChatWindow:

    def __init__(self):
        self.session_id = get_session()
        self.analytics = None
        self.thinking = None 

        with ui.column().classes(
            "flex-grow max-w-6xl mx-auto px-6 py-4"
        ):

            self.chat_container = ui.column().classes(
                "w-full h-[78vh] overflow-auto rounded-2xl bg-white border border-gray-200 p-5 gap-4"
            )

            with self.chat_container:
                self._add_welcome_message()

            with ui.row().classes(
                "w-full items-center gap-3 mt-3"
            ):

                self.prompt = (
                    ui.textarea(
                        placeholder="Ask Gateway AI anything..."
                    ).props(
                        "outlined autogrow rounded"
                    ).classes(
                        "flex-grow text-base"
                    )
                )
                self.prompt.on(
                    "keydown.enter",
                    lambda _: self.send(),
                )

                ui.button(
                    "Send",
                    icon="send",
                    on_click=self.send,
                ).props(
                    "unelevated color=primary"
                ).classes(
                    "h-12 px-6 rounded-xl shadow-sm"
                )

    def set_analytics(self, analytics):
        self.analytics = analytics

    # --------------------------------------------------
    # UI Helpers
    # --------------------------------------------------

    def _add_welcome_message(self):
        MessageBubble(
        message="""
        Welcome 👋

        I'm your AI Gateway.

        I can:

        • Route prompts to different LLMs

        • Check Redis Cache

        • Search Semantic Cache

        • Maintain conversation memory

        Ask me anything!
        """,
        sender="Gateway AI",
        is_user=False,
    )

    def add_user_message(self, message: str):
        with self.chat_container:
            MessageBubble(
                message=message,
                sender="You",
                is_user=True,
            )

    def add_ai_message(self, message: str):
        with self.chat_container:
            MessageBubble(
                message=message,
                sender="Gateway AI",
                is_user=False,
            )

    def show_thinking(self):
        with self.chat_container:
            self.thinking = ui.row().classes("items-center gap-3")

            with self.thinking:
                ui.spinner(size="md")

                ui.label(
                    "Thinking..."
                ).classes(
                    "text-sm text-gray-500"
                )


    def hide_thinking(self):
        if self.thinking:
            self.thinking.delete()
            self.thinking = None

    def clear_chat(self):
        """
        Clear the chat window and show the welcome message.
        """
        self.chat_container.clear()

        with self.chat_container:
            self._add_welcome_message()

    def new_chat(self):
        """
        Start a fresh chat session.
        """
        self.session_id = new_session()

        self.clear_chat()

    def load_conversation(self, session_id: str):
        """
        Load an existing conversation from the backend.
        """

        set_session(session_id)
        self.session_id = session_id

        token = get_token()

        response = get_conversation(
            session_id=session_id,
            token=token,
        )

        if response.status_code != 200:
            ui.notify(
                "Failed to load conversation",
                color="negative",
            )
            return

        history = response.json()

        # Clear current chat
        self.chat_container.clear()

        # Render conversation
        with self.chat_container:

            for message in history:

                if message["role"] == "user":

                    MessageBubble(
                        message=message["content"],
                        sender="You",
                        is_user=True,
                    )

                else:

                    MessageBubble(
                        message=message["content"],
                        sender="Gateway AI",
                        is_user=False,
                    )

    def show_error(self, message: str):
        self.add_ai_message(message)

    # --------------------------------------------------
    # Analytics
    # --------------------------------------------------

    def update_analytics(self, model: str, source: str):

        if not self.analytics:
            return

        # ---------------- Model ---------------- #
        self.analytics["model"].set_text(model)
        self.analytics["model"].classes(
            replace="text-sm font-semibold text-blue-600"
        )

        # ---------------- Source ---------------- #
        self.analytics["source"].set_text(source.upper())
        self.analytics["source"].classes(
            replace="text-sm font-semibold text-purple-600"
        )

        # ---------------- Reset ---------------- #
        self.analytics["redis"].set_text("-")
        self.analytics["redis"].classes(
            replace="text-sm font-semibold text-slate-700"
        )

        self.analytics["semantic"].set_text("-")
        self.analytics["semantic"].classes(
            replace="text-sm font-semibold text-slate-700"
        )

        self.analytics["latency"].set_text("-")
        self.analytics["latency"].classes(
            replace="text-sm font-semibold text-slate-700"
        )

        # ---------------- Cache Status ---------------- #
        if source == "redis":

            self.analytics["redis"].set_text("HIT")
            self.analytics["redis"].classes(
                replace="text-sm font-semibold text-green-600"
            )

            self.analytics["semantic"].set_text("-")

        elif source == "semantic_cache":

            self.analytics["redis"].set_text("MISS")
            self.analytics["redis"].classes(
                replace="text-sm font-semibold text-red-500"
            )

            self.analytics["semantic"].set_text("HIT")
            self.analytics["semantic"].classes(
                replace="text-sm font-semibold text-green-600"
            )

        else:

            self.analytics["redis"].set_text("MISS")
            self.analytics["redis"].classes(
                replace="text-sm font-semibold text-red-500"
            )

            self.analytics["semantic"].set_text("MISS")
            self.analytics["semantic"].classes(
                replace="text-sm font-semibold text-red-500"
            )

    # --------------------------------------------------
    # Backend
    # --------------------------------------------------

    def call_backend(self, question: str):

        token = get_token()

        print("=" * 50)
        print("TOKEN USED IN CHAT:")
        print(token)
        print("=" * 50)

        return chat(
            prompt=question,
            token=token,
            session_id=self.session_id,
        )

    # --------------------------------------------------
    # Main Send Function
    # --------------------------------------------------

    def send(self):

        question = self.prompt.value.strip()

        if not question:
            return

        self.prompt.value = ""

        self.add_user_message(question)

        self.show_thinking()

        try:

            response = self.call_backend(question)

            self.hide_thinking()

            if response.status_code != 200:

                try:
                    error = response.json().get(
                        "detail",
                        "Backend Error",
                    )
                except Exception:
                    error = "Backend Error"

                self.show_error(error)
                return

            print("STATUS:", response.status_code)
            print("TEXT:", response.text)

            data = response.json()

            print("=" * 50)
            print("BACKEND RESPONSE:")
            print(data)
            print("=" * 50)

            print("Reached A")

            answer = data["response"]["response"]
            print("Reached B:", answer)

            model = data["response"]["model"]
            print("Reached C:", model)

            source = data["source"]
            print("Reached D:", source)

            self.add_ai_message(answer)
            print("Reached E")

            self.update_analytics(
                model=model,
                source=source,
            )
            print("Reached F")

        except Exception as e:

            
            traceback.print_exc()

            self.hide_thinking()

            self.show_error(
                f"ERROR: {e}"
            )


def build_chat_window():
    return ChatWindow()