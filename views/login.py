import flet as ft
import os
import json
import bcrypt
from models.styles import *

def login_view(page):
    def load_users():
        if not os.path.exists('users.json'):
            return {}
        with open('users.json', "r", encoding="utf-8") as f:
            return json.load(f)

    async def go_register(e):
        await page.push_route("/register")

    async def login_click(e):
        username = name_user.value
        password = password_user.value
        users_db = load_users()

        stored = users_db.get(username)
        
        if stored and bcrypt.checkpw(password.encode('utf-8'), stored.encode('utf-8')):
            page.session.store.set("authenticated", True)
            page.session.store.set("current_user", username)
            await page.push_route("/gallery")
        else:
            message.value = "Невірний логін або пароль!"
            page.update()

    title = ft.Text('Вітаємо у нашому магазині!', size=32, **text_STYLE)
    backtext = ft.Text('Введіть будь ласка свої дані, щоб ввійти в систему', size=14, **text_STYLE)
    name_user = ft.TextField(label='Введіть своє імʼя', prefix_icon=ft.Icons.PERSON, hint_text='dmytro_kalitovskyi', **textfield_STYLE)
    password_user = ft.TextField(label='Введіть пароль', prefix_icon=ft.Icons.PASSWORD, password=True, hint_text='Qwerty123', can_reveal_password=True, **textfield_STYLE)
    accept_button = ft.Button('Підтвердити', on_click=login_click, style=btn_style)
    message = ft.Text('', **error_text_STYLE)

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
            accept_button,
            ft.TextButton("Немає акаунту? Реєстрація", on_click=go_register, style=button_STYLE),
            message
        ])