import flet as ft

def settings_view(page):
    async def go_home(e):
        await page.push_route("/home")
    
    return ft.View(
        route="/settings",
            controls=[ft.Column([
                ft.AppBar(
                    title=ft.Text("Налаштування"),
                    actions=[ft.IconButton(ft.Icons.HOME, on_click=go_home)]),
                ft.Divider()])] )