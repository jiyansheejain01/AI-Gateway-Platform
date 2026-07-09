from nicegui import ui


class MessageBubble:

    def __init__(
        self,
        message: str,
        sender: str,
        is_user: bool = False,
    ):

        align = "justify-end" if is_user else "justify-start"

        bubble = (
            "bg-blue-50 text-slate-800 border border-blue-200"
            if is_user
            else "bg-white text-slate-800 border border-gray-200"
        )

        icon = "person" if is_user else "smart_toy"

        with ui.row().classes(f"w-full {align}"):

            if not is_user:
                ui.avatar(
                    icon=icon
                ).classes(
                    "bg-blue-500 text-white mt-1"
                )

            with ui.column().classes("max-w-[72%] gap-1"):

                ui.label(sender).classes(
                    "text-[11px] font-medium text-gray-400 px-1"
                )

                with ui.card().classes(
                    f"{bubble} w-full rounded-2xl px-4 py-3 shadow-sm border-0"
                ):

                    ui.markdown(message).classes(
                        "prose prose-sm max-w-none"
                    )

            if is_user:
                ui.avatar(
                    icon=icon
                ).classes(
                    "bg-blue-500 text-white w-9 h-9 mt-1"
                )