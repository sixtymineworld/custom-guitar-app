import flet as ft
import os
import json
from models.styles import *

def register_view(page):
    def load_users():
        if not os.path.exists('users.json'):
            return {}
        with open('users.json', "r", encoding="utf-8") as f:
            return json.load(f)
        
    users_db = load_users()

    def save_users(users):
        with open('users.json', "w", encoding="utf-8") as f:
            json.dump(users, f, indent=4, ensure_ascii=False)
        
    async def go_login(e):
        await page.push_route("/login")

    async def register_click(e):
            username = name_user.value
            password = password_user.value
            if not username or not password:
                message.value = "Заповніть всі поля!"
            elif username in users_db:
                message.value = "Користувач вже існує!"
            else:
                users_db[username] = password
                save_users(users_db)
                await page.push_route("/login")
                return
            page.update()



    title = ft.Text('Вікно реєстрації', size=32, **text_STYLE)
    backtext = ft.Text('Введіть будь ласка свої дані, щоб ввійти в систему', size=14, **text_STYLE)
    name_user = ft.TextField(label='Введіть своє імʼя', prefix_icon=ft.Icons.PERSON, hint_text='vasya_pupkin', **textfield_STYLE)
    password_user = ft.TextField(label='Введіть пароль', prefix_icon=ft.Icons.PASSWORD,password=True, hint_text='qwerty123', can_reveal_password=True, **textfield_STYLE)
    accept_button = ft.Button('Підтвердити', on_click=register_click, style=btn_style)
    message = ft.Text('', **error_text_STYLE)


    return ft.View(
        route="/",
        bgcolor=ft.Colors.BLACK,
        horizontal_alignment = ft.CrossAxisAlignment.CENTER,
        vertical_alignment = ft.MainAxisAlignment.CENTER,
        controls=[
            title,
            backtext,
            name_user,
            password_user,
            accept_button,
            ft.TextButton("Вже є акаунт? Увійти", on_click=go_login, style=button_STYLE),
            message
        ])