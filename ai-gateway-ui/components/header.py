from nicegui import ui

from auth.session import (
    get_username,
    logout,
)


def build_header():

    with ui.header().classes(
    "bg-slate-900 text-white h-20 px-6 shadow-lg flex items-center justify-between"
):

        # ---------------- Logo ---------------- #

        with ui.row().classes("items-center gap-3"):

            ui.icon(
                "hub"
            ).classes(
                "text-4xl text-blue-400"
            )

            with ui.column().classes("gap-0"):

                ui.label(
                    "AI Gateway Platform"
                ).classes(
                    "text-2xl font-bold"
                )

                ui.label(
                    "Intelligent LLM Orchestration"
                ).classes(
                    "text-xs text-slate-300"
                )

        ui.space()

        # ---------------- Status ---------------- #

        with ui.row().classes("items-center gap-2 mr-8"):

            ui.icon(
                "circle"
            ).classes(
                "text-green-400 text-sm"
            )

            ui.label(
                "Gateway Online"
            ).classes(
                "text-sm text-green-300"
            )

        # ---------------- User ---------------- #

        with ui.row().classes("items-center gap-3"):

            ui.avatar(
                icon="person"
            ).classes(
                "bg-blue-500 text-white"
            )

            with ui.column().classes("gap-0"):

                ui.label(
                    get_username() or "User"
                ).classes(
                    "font-semibold"
                )

                ui.label(
                    "Authenticated"
                ).classes(
                    "text-xs text-slate-300"
                )

            ui.button(
                icon="logout",
                on_click=lambda: (
                    logout(),
                    ui.navigate.to("/")
                ),
            ).props(
                "flat round color=white"
            ).tooltip(
                "Logout"
            )