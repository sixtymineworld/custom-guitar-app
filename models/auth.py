import flet as ft
from models.styles import *

async def check_auth_and_show_dialog(page):
    is_auth = page.session.store.get("authenticated")
    
    if not is_auth:
        async def go_login(e):
            dlg.open = False
            page.update()
            await page.push_route("/login")

        async def go_register(e):
            dlg.open = False
            page.update()
            await page.push_route("/register")

        async def close_dialog(e):
            dlg.open = False
            page.update()

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Необхідна авторизація, увійдіть або зареєструйтеся для продовження", title_text_style=ft.TextStyle(font_family='Text')),
            actions=[
                ft.TextButton("Увійти", on_click=go_login, style=bars_buttons),
                ft.TextButton("Зареєструватися", on_click=go_register, style=bars_buttons),
                ft.TextButton("Відмінити", on_click=close_dialog, style=bars_buttons),
            ],
        )
        page.overlay.append(dlg)
        dlg.open = True
        page.update()
        return False
    return True