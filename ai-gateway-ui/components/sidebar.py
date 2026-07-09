from nicegui import ui


def conversation_item(title: str, active: bool = False):

    bg = (
        "bg-blue-50 border border-blue-200"
        if active
        else "bg-white border border-transparent hover:bg-gray-50"
    )

    with ui.card().classes(
        f"""
        w-full
        rounded-xl
        shadow-none
        cursor-pointer
        transition-all
        duration-200
        {bg}
        """
    ).style(
        "padding:12px;"
    ):

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


def build_sidebar():

    with ui.column().classes(
    "w-72 h-full bg-white border-r border-gray-200 p-3"
    ):

        # ---------------- New Chat ---------------- #

        ui.button(
            "New Chat",
            icon="add",
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

        conversation_item(
            "How does Redis work?",
            active=True
        )

        conversation_item(
            "JWT Authentication"
        )

        conversation_item(
            "Semantic Cache"
        )

        ui.separator().classes("my-3")

        # ---------------- Yesterday ---------------- #

        ui.label(
            "YESTERDAY"
        ).classes(
            "text-xs font-bold text-gray-500"
        )

        conversation_item(
            "Docker Compose"
        )

        conversation_item(
            "LLM Routing"
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