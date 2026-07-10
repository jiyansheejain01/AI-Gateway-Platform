from nicegui import ui
from api.client import get_conversations
from auth.session import get_token
from components.chat_controller import get_chat_window
from components.sidebar_controller import set_sidebar_refresh
from auth.chat_session import get_session

def conversation_item(
    title: str,
    active: bool = False,
    session_id: str | None = None,
    on_click=None,
):

    bg = (
        "bg-blue-50 border border-blue-200"
        if active
        else "bg-white border border-transparent hover:bg-gray-50"
    )

    card = (
        ui.card()
        .classes(
            f"""
            w-full
            rounded-xl
            shadow-none
            cursor-pointer
            transition-all
            duration-200
            {bg}
            """
        )
        .style("padding:12px;")
    )

    # Attach click handler
    if on_click:
        card.on(
            "click",
            lambda _: (
                print(f"Clicked session: {session_id}"),
                on_click(session_id),
            ),
        )

    with card:

        with ui.row().classes(
            "items-center no-wrap w-full gap-3"
        ):

            ui.icon(
                "chat_bubble_outline"
            ).classes(
                "text-gray-500 text-lg"
            )

            with ui.column().classes(
                "gap-0 flex-grow"
            ):

                ui.label(title).classes(
                    "text-sm font-medium text-gray-800"
                )

                ui.label(
                    "Click to open"
                ).classes(
                    "text-xs text-gray-400"
                )


def build_sidebar(chat_window=None):

    conversations = []

    try:
        token = get_token()

        response = get_conversations(token)

        print("=" * 50)
        print("GET /conversations")
        print("Status:", response.status_code)
        print("Body:", response.text)
        print("=" * 50)

        if response.status_code == 200:
            conversations = response.json()

    except Exception as e:
        print("Failed to load conversations:", e)

    with ui.column().classes(
    "w-72 shrink-0 h-full bg-white border-r border-gray-200 p-3"
    ):

        # ---------------- New Chat ---------------- #

        ui.button(
            "New Chat",
            icon="add",
            on_click=lambda: get_chat_window().new_chat(),
        ).props(
            "unelevated color=primary"
        ).classes(
            "w-full h-11 rounded-xl font-semibold text-sm shadow-sm"
        )

        ui.separator().classes("my-4")

        # ---------------- Today ---------------- #

        ui.label(
            "TODAY"
        ).classes(
            "uppercase tracking-widest text-[11px] font-semibold text-gray-400 px-2 pt-2"
        )

        @ui.refreshable
        def render_conversations():

            conversations = []

            try:
                token = get_token()

                response = get_conversations(token)

                if response.status_code == 200:
                    conversations = response.json()

            except Exception as e:
                print("Failed to load conversations:", e)

            if conversations:

                current_session = get_session()

                for conversation in conversations:

                    conversation_item(
                        title=conversation["title"],
                        session_id=conversation["session_id"],
                        active=(
                            conversation["session_id"]
                            == current_session
                        ),
                        on_click=lambda session_id:
                            get_chat_window().load_conversation(session_id),
                    )

            else:

                ui.label(
                    "No conversations yet"
                ).classes(
                    "text-xs text-gray-400 px-2 py-2"
                )

        set_sidebar_refresh(render_conversations.refresh)

        render_conversations()

        ui.separator().classes("my-3")

        # ---------------- Yesterday ---------------- #

        ui.label(
            "YESTERDAY"
        ).classes(
            "text-xs font-bold text-gray-500"
        )

        ui.space()

        ui.separator()

        with ui.row().classes(
            "items-center justify-center w-full py-2"
        ):

            ui.icon(
                "storage"
            ).classes(
                "text-blue-500"
            )

            ui.label(
                "Gateway v1.0"
            ).classes(
                "text-sm text-gray-500"
            )