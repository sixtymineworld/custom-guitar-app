import flet as ft
import os
import json
import re
import bcrypt
from models.styles import *

def register_view(page):
    def load_users():
        if not os.path.exists('users.json'):
            return {}
        with open('users.json', "r", encoding="utf-8") as f:
            return json.load(f)

    def save_users(users):
        with open('users.json', "w", encoding="utf-8") as f:
            json.dump(users, f, indent=4, ensure_ascii=False)

    def validate_password(password):
        if len(password) < 6:
            return "Потрібно мінімум 6 символів"
        if not re.search(r'[a-z]', password):
            return "Потрібно хоча б одна мала літера"
        if not re.search(r'[A-Z]', password):
            return "Потрібно хоча б одна велика літера"
        if not re.search(r'\d', password):
            return "Потрібно хоча б одна цифра"
        return None

    async def go_login(e):
        await page.push_route("/login")

    async def register_click(e):
        username = name_user.value.strip()
        password = password_user.value
        confirm  = confirm_user.value

        name_user.error_text     = None
        password_user.error_text = None
        confirm_user.error_text  = None
        message.value            = ""

        has_error = False

        if not username:
            name_user.error_text = "Введіть імʼя користувача"
            has_error = True

        if not password:
            password_user.error_text = "Введіть пароль"
            has_error = True
        else:
            validation_message = validate_password(password)
            if validation_message:
                password_user.error_text = validation_message
                has_error = True

        if not confirm:
            confirm_user.error_text = "Підтвердіть пароль"
            has_error = True
        elif password and confirm != password:
            confirm_user.error_text = "Паролі не співпадають"
            has_error = True

        if not has_error:
            users_db = load_users()
            if username in users_db:
                message.value = "Користувач вже існує!"
            else:
                hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                users_db[username] = hashed.decode('utf-8')
                save_users(users_db)
                await page.push_route("/login")
                return

        page.update()

    title = ft.Text("Вікно реєстрації", size=32, **text_STYLE)
    backtext = ft.Text("Введіть будь ласка свої дані, щоб ввійти в систему", size=14, **text_STYLE)
    name_user = ft.TextField(label="Введіть своє імʼя",  prefix_icon=ft.Icons.PERSON,   hint_text="dmytro_kalitovskyi", **textfield_STYLE)
    password_user = ft.TextField(label="Введіть пароль",     prefix_icon=ft.Icons.PASSWORD, hint_text="Qwerty123",    password=True, can_reveal_password=True, **textfield_STYLE)
    confirm_user = ft.TextField(label="Підтвердіть пароль", prefix_icon=ft.Icons.PASSWORD, hint_text="Qwerty123",    password=True, can_reveal_password=True, **textfield_STYLE)
    accept_button = ft.Button("Підтвердити", on_click=register_click, style=btn_style)
    message = ft.Text("", **error_text_STYLE)

    return ft.View(
        route="/",
        bgcolor=ft.Colors.BLACK,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            title,
            backtext,
            name_user,
            password_user,
            confirm_user,
            accept_button,
            ft.TextButton("Вже є акаунт? Увійти", on_click=go_login, style=button_STYLE),
            message,
        ]
    )