from nicegui import ui


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

    if on_click:
        card.on(
            "click",
            lambda _: on_click(session_id),
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