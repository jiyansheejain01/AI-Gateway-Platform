from nicegui import ui


def metric_row(icon: str, title: str):

    with ui.row().classes(
        "w-full items-center justify-between py-3"
    ):

        with ui.row().classes(
            "items-center gap-3"
        ):

            ui.icon(icon).classes(
                "text-blue-600 text-lg"
            )

            ui.label(title).classes(
                "text-sm text-gray-600 font-medium"
            )

        value = ui.label("-").classes(
            "text-sm font-semibold text-slate-800"
        )

    ui.separator()

    return value


def build_analytics():

    with ui.column().classes(
        "w-80 h-full bg-white border-l border-gray-200 p-5"
    ):

        ui.label(
            "Gateway Analytics"
        ).classes(
            "text-2xl font-bold"
        )

        ui.label(
            "Live gateway information"
        ).classes(
            "text-sm text-gray-500 mb-4"
        )

        with ui.card().classes(
            "w-full rounded-2xl shadow-none border border-gray-200 p-4"
        ):

            model = metric_row(
                "smart_toy",
                "Selected Model",
            )

            source = metric_row(
                "route",
                "Response Source",
            )

            redis = metric_row(
                "storage",
                "Redis Cache",
            )

            semantic = metric_row(
                "psychology",
                "Semantic Cache",
            )

            latency = metric_row(
                "timer",
                "Latency",
            )

    return {
        "model": model,
        "source": source,
        "redis": redis,
        "semantic": semantic,
        "latency": latency,
    }