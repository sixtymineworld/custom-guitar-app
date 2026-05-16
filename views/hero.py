import flet as ft
from models.styles import *


def hero_view(page: ft.Page):

    async def go_register(e):
        await page.push_route("/register")

    async def go_login(e):
        await page.push_route("/login")

    def build(e=None):
        is_mobile = page.width < 600

        # ── BOTTOM APPBAR CONTENT ──
        if is_mobile:
            bottom_content = ft.Column(
                spacing=4,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text("Guitar Custom", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.YELLOW_ACCENT_400),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.IconButton(icon=ft.Icons.HOME_ROUNDED, icon_color=ft.Colors.YELLOW_ACCENT_400, style=icon_button_STYLE),
                            ft.IconButton(icon=ft.Icons.MUSIC_NOTE, icon_color=ft.Colors.YELLOW_700, style=icon_button_STYLE),
                            ft.IconButton(icon=ft.Icons.SHOPPING_BASKET_SHARP, icon_color=ft.Colors.YELLOW_700, style=icon_button_STYLE),
                            ft.IconButton(icon=ft.Icons.INFO_OUTLINE, icon_color=ft.Colors.YELLOW_700, style=icon_button_STYLE),
                            ft.IconButton(icon=ft.Icons.FACEBOOK, icon_color=ft.Colors.YELLOW_700, style=icon_button_STYLE),
                            ft.IconButton(icon=ft.Icons.CAMERA_ALT, icon_color=ft.Colors.YELLOW_700, style=icon_button_STYLE),
                        ],
                    ),
                    ft.Text("© 2025 Guitar Custom", size=10, color=ft.Colors.GREY_500),
                ],
            )
        else:
            bottom_content = ft.Column(
                spacing=8,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Text("Guitar Custom", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.YELLOW_ACCENT_400),
                            ft.Row(
                                controls=[
                                    ft.TextButton("Головна", style=ft.ButtonStyle(color=ft.Colors.WHITE)),
                                    ft.TextButton("Каталог", style=ft.ButtonStyle(color=ft.Colors.WHITE)),
                                    ft.TextButton("Замовлення", style=ft.ButtonStyle(color=ft.Colors.WHITE)),
                                    ft.TextButton("Про нас", style=ft.ButtonStyle(color=ft.Colors.WHITE)),
                                    ft.TextButton("Контакти", style=ft.ButtonStyle(color=ft.Colors.WHITE)),
                                ]
                            ),
                            ft.Row(
                                controls=[
                                    ft.IconButton(icon=ft.Icons.FACEBOOK, icon_color=ft.Colors.WHITE, style=icon_button_STYLE),
                                    ft.IconButton(icon=ft.Icons.CAMERA_ALT, icon_color=ft.Colors.WHITE, style=icon_button_STYLE),
                                ]
                            ),
                        ],
                    ),
                    ft.Divider(color=ft.Colors.GREY_700, height=16),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.Text("© 2025 Guitar Custom", size=11, color=ft.Colors.GREY_500),
                        ],
                    ),
                ],
            )

        view.controls = [
            ft.AppBar(
                **appbar_STYLE,
                title=ft.Text(
                    "Guitar Custom",
                    color=ft.Colors.YELLOW_ACCENT_400,
                    size=16 if is_mobile else 20,
                ),
                actions=[
                    ft.TextButton("Увійти", style=button_STYLE, on_click=go_login),
                    ft.Container(width=8 if is_mobile else 12),
                ],
            ),
            ft.Stack(
                expand=True,
                controls=[
                    ft.Image(
                        src="hero.png",
                        fit=ft.BoxFit.COVER if is_mobile else ft.BoxFit.CONTAIN,
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
                        padding=ft.Padding.only(bottom=24 if is_mobile else 32),
                        content=ft.ElevatedButton(
                            "Перейти до реєстрації",
                            icon=ft.Icons.ARROW_FORWARD,
                            style=btn_style,
                            on_click=go_register,
                        ),
                    ),
                ],
            ),
        ]

        view.bottom_appbar = ft.BottomAppBar(
            **{**bottom_appbar_STYLE, "height": 90 if is_mobile else 120},
            content=bottom_content,
        )

        page.update()

    view = ft.View(
        route="/",
        bgcolor=ft.Colors.TRANSPARENT,
        padding=0,
        controls=[],
    )

    page.on_resized = build
    build()

    return view