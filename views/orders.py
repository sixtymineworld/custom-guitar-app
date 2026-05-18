import flet as ft
import json
import os
from models.styles import *

ORDERS_FILE = "orders.json"


def load_orders():
    if not os.path.exists(ORDERS_FILE):
        return {}
    with open(ORDERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def orders_view(page):
    async def go_home(e):
        await page.push_route("/home")

    username = page.session.store.get("current_user")
    all_orders = load_orders()
    user_orders = all_orders.get(username, [])

    if not user_orders:
        orders_content = ft.Column(
            [
                ft.Container(height=40),
                ft.Icon(ft.Icons.MUSIC_OFF, size=64, color=ft.Colors.GREY_600),
                ft.Text(
                    "Замовлень ще немає 🎸",
                    size=18,
                    color=ft.Colors.GREY_400,
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    else:
        cards = []
        for i, order in enumerate(user_orders, 1):

            img_path = order.get("image_path")
            img_control = None
            if img_path:
                img_src = os.path.basename(img_path)
                img_control = ft.Container(
                    content=ft.Image(
                        src=img_src,
                        width=260,
                        height=260,
                        fit=ft.BoxFit.CONTAIN,
                    ),
                )

            card_controls = [
                ft.Text(
                    f"Замовлення #{i}",
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.YELLOW_ACCENT_400,
                ),
                ft.Divider(height=4, color=ft.Colors.GREY_700),
                ft.Text(f"Форма: {order.get('shape', '—')}", color=ft.Colors.WHITE),
                ft.Text(f"Деревина: {order.get('wood', '—')}", color=ft.Colors.WHITE),
                ft.Text(f"Бридж: {order.get('bridge', '—')}", color=ft.Colors.WHITE),
                ft.Text(f"Лади: {order.get('frets', '—')}", color=ft.Colors.WHITE),
                ft.Text(f"Колір: {order.get('color', '—')}", color=ft.Colors.WHITE),
            ]

            if img_control:
                card_controls.append(img_control)

            cards.append(
                ft.Container(
                    content=ft.Column(card_controls, spacing=6),
                    bgcolor=ft.Colors.GREY_900,
                    border_radius=12,
                    padding=16,
                    margin=ft.Margin(0, 0, 0, 14),
                )
            )

        orders_content = ft.Column(cards, scroll=ft.ScrollMode.ADAPTIVE)

    return ft.View(
        route="/orders",
        controls=[
            ft.AppBar(
                title=ft.Text("Мої замовлення", color=ft.Colors.YELLOW_ACCENT_400),
                actions=[
                    ft.IconButton(
                        ft.Icons.HOME,
                        icon_color=ft.Colors.YELLOW_ACCENT_400,
                        on_click=go_home,
                    )
                ],
                **appbar_STYLE,
            ),
            ft.Container(
                content=orders_content,
                padding=16,
                expand=True,
            ),
        ],
    )