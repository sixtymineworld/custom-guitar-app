import flet as ft
from models.styles import *
from models.auth import *


def hero_view(page: ft.Page):

    async def go_register(e):
        await page.push_route("/register")

    async def go_login(e):
        await page.push_route("/login")

    async def go_gallery(e):
        await page.push_route("/gallery")
    
    async def go_orders(e):
        if not check_auth_and_show_dialog(page):
            return
        await page.push_route("/orders")

    async def go_hero(e):
        await page.push_route("/")

    return ft.View(
        route="/",
        bgcolor=ft.Colors.TRANSPARENT,
        padding=0,
        controls=[
            ft.AppBar(
                **appbar_STYLE,
                title=ft.Text("Guitar Custom", color=ft.Colors.YELLOW_ACCENT_400, font_family='Title'),
                actions=[
                    ft.TextButton("Увійти", style=button_STYLE, on_click=go_login),
                    ft.Container(width=12),
                ],
            ),
            ft.Stack(
                expand=True,
                controls=[
                    ft.Image(
                        src="hero.png",
                        fit=ft.BoxFit.CONTAIN,
                        expand=True,
                        width=float("inf"),
                        height=float("inf"),
                    ),
                    ft.Container(
                        expand=True,
                        gradient=ft.LinearGradient(
                            begin=ft.Alignment(0, -1),
                            end=ft.Alignment(0, 1),
                            colors=["#00000000", "#CC000000"],
                        ),
                    ),
                    ft.Container(
                        expand=True,
                        alignment=ft.Alignment.BOTTOM_CENTER,
                        padding=ft.Padding(left=0, top=0, right=0, bottom=48),
                        content=ft.FilledButton(
                            "Перейти до реєстрації",
                            icon=ft.Icons.ARROW_FORWARD,
                            on_click=go_register,
                            style=btn_style
                        ),
                    ),
                ],
            ),
        ],
        bottom_appbar=ft.BottomAppBar(
            **bottom_appbar_STYLE,
            content=ft.Column(
                spacing=5,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Text("Guitar Custom", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.YELLOW_ACCENT_400, font_family='Title'),
                            ft.Row(
                                controls=[
                                    ft.TextButton("Головна", style=bars_buttons, on_click=go_hero),
                                    ft.TextButton("Каталог", style=bars_buttons, on_click=go_gallery),
                                    ft.TextButton("Замовлення", style=bars_buttons, on_click=go_orders),
                                ]
                            ),
                            ft.Row(
                                controls=[
                                    ft.IconButton(icon=ft.Icons.FACEBOOK, icon_color=ft.Colors.WHITE, style=icon_button_STYLE, url='https://www.facebook.com/groups/1548580592066473/'),
                                    ft.IconButton(icon=ft.Icons.PLAY_CIRCLE, icon_color=ft.Colors.WHITE, style=icon_button_STYLE, url='https://www.youtube.com/@CrimsonCustomGuitars'),
                                ]
                            ),
                        ],
                    ),
                    ft.Divider(color=ft.Colors.GREY_700, height=16),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[ft.Text("© 2026 Custom Guitar", font_family='Title', color=ft.Colors.WHITE)],
                    ),
                ],
            ),
        ),
    )