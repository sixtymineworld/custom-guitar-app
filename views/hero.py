import flet as ft
from models.styles import *


def hero_view(page: ft.Page):

    async def go_register(e):
        await page.push_route("/register")

    async def go_login(e):
        await page.push_route("/login")

    return ft.View(
        route="/",
        bgcolor=ft.Colors.TRANSPARENT,
        padding=0,
        controls=[
            ft.AppBar(
                **appbar_STYLE,
                title=ft.Text("Guitar Custom", color=ft.Colors.YELLOW_ACCENT_400),
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
                        alignment=ft.Alignment(0, 1),
                        padding=ft.Padding.only(bottom=32),
                        content=ft.ElevatedButton(
                            "Перейти до реєстрації",
                            icon=ft.Icons.ARROW_FORWARD,
                            style=btn_style,
                            on_click=go_register,
                        ),
                    ),
                ],
            ),
        ],

        bottom_appbar=ft.BottomAppBar(
            **bottom_appbar_STYLE,
            content=ft.Column(
                spacing=8,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Text("Guitar Custom", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.YELLOW_ACCENT_400),
                            ft.Row(
                                controls=[
                                    ft.FilledButton("Головна", style=button_STYLE),
                                    ft.FilledButton("Каталог", style=button_STYLE),
                                    ft.FilledButton("Замовлення", style=button_STYLE),
                                    ft.FilledButton("Про нас", style=button_STYLE),
                                    ft.FilledButton("Контакти", style=button_STYLE),
                                ]
                            ),
                            ft.Row(
                                controls=[
                                    ft.IconButton(icon=ft.Icons.FACEBOOK, style=icon_button_STYLE),
                                    ft.IconButton(icon=ft.Icons.CAMERA_ALT, style=icon_button_STYLE),
                                ]
                            ),
                        ],
                    ),
                    ft.Divider(color=ft.Colors.GREY_700, height=16),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.Text("© 2025 Custom Guitar")
                        ],
                    ),
                ],
            ),
        ),
    )