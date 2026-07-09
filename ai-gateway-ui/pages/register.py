from nicegui import ui

from api.client import register


def register_page():

    with ui.column().classes(
        "absolute-center items-center w-96 gap-4"
    ):

        ui.label("AI Gateway Platform").classes(
            "text-3xl font-bold"
        )

        ui.label(
            "Create your account"
        ).classes("text-grey")

        username = ui.input(
            "Username"
        ).classes("w-full")

        email = ui.input(
            "Email"
        ).classes("w-full")

        password = ui.input(
            "Password",
            password=True,
            password_toggle_button=True,
        ).classes("w-full")

        confirm_password = ui.input(
            "Confirm Password",
            password=True,
            password_toggle_button=True,
        ).classes("w-full")

        def handle_register():

            if not username.value or not email.value or not password.value:

                ui.notify(
                    "Please fill all fields",
                    type="negative",
                )
                return

            if password.value != confirm_password.value:

                ui.notify(
                    "Passwords do not match",
                    type="negative",
                )
                return

            response = register(
                username.value,
                email.value,
                password.value,
            )

            if response.status_code in [200, 201]:

                ui.notify(
                    "Registration Successful!",
                    type="positive",
                )

                ui.navigate.to("/")

            else:

                try:
                    message = response.json().get(
                        "detail",
                        "Registration Failed",
                    )
                except Exception:
                    message = "Registration Failed"

                ui.notify(
                    message,
                    type="negative",
                )

        ui.button(
            "Register",
            on_click=handle_register,
            icon="person_add",
        ).classes("w-full")

        ui.link(
            "Already have an account? Login",
            "/",
        )