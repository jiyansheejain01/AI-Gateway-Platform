from nicegui import ui

from api.client import login
from auth.session import save_session


def login_page():

    with ui.column().classes(
        "absolute-center items-center w-96 gap-4"
    ):

        ui.label("AI Gateway Platform").classes(
            "text-3xl font-bold"
        )

        ui.label(
            "Sign in to continue"
        ).classes("text-grey")

        username = ui.input(
            "Username"
        ).classes("w-full")

        password = ui.input(
            "Password",
            password=True,
            password_toggle_button=True,
        ).classes("w-full")

        def handle_login():

            response = login(
                username.value,
                password.value,
            )

            print("STATUS CODE:", response.status_code)

            if response.status_code == 200:

                data = response.json()

                print("LOGIN RESPONSE:")
                print(data)

                save_session(
                    data["access_token"],
                    username.value,
                )

                ui.notify(
                    "Login Successful!",
                    type="positive",
                )

                ui.navigate.to("/chat")

            else:

                print("LOGIN FAILED")
                print(response.text)

                try:
                    message = response.json().get(
                        "detail",
                        "Login Failed",
                    )
                except Exception:
                    message = "Login Failed"

                ui.notify(
                    message,
                    type="negative",
                )

        ui.button(
            "Login",
            on_click=handle_login,
            icon="login",
        ).classes("w-full")

        ui.link(
            "Create an account",
            "/register",
        )