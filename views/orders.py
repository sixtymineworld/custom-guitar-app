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


def save_orders(orders):
    with open(ORDERS_FILE, "w", encoding="utf-8") as f:
        json.dump(orders, f, indent=4, ensure_ascii=False)


def orders_view(page):
    async def go_home(e):
        await page.push_route("/home")
    async def go_gallery(e):
        await page.push_route("/gallery")

    username = page.session.store.get("current_user")

    def build_orders_content():
        all_orders = load_orders()
        user_orders = all_orders.get(username, [])

        if not user_orders:
            return ft.Column(
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

        async def delete_order(index):
            all_orders = load_orders()
            all_orders[username].pop(index)
            if not all_orders[username]:
                del all_orders[username]
            save_orders(all_orders)
            orders_container.content = build_orders_content()
            page.update()

        cards = []
        for i, order in enumerate(user_orders):
            img_path = order.get("image_path")
            img_control = None
            if img_path:
                img_src = os.path.basename(img_path)
                img_control = ft.Container(
                    content=ft.Image(
                        src=img_src,
                        width=160,
                        height=160,
                        fit=ft.BoxFit.CONTAIN,
                    ),
                    border_radius=10,
                    clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                )

            card_controls = ft.Row(
                controls=[
                    img_control if img_control else ft.Container(
                        width=160, height=160, bgcolor="#2A2A2A", border_radius=10
                    ),
                    ft.Column(
                        controls=[
                            ft.Row(
                                controls=[
                                    ft.Text(
                                        f"Замовлення #{i + 1}",
                                        size=16,
                                        weight=ft.FontWeight.BOLD,
                                        color=ft.Colors.YELLOW_ACCENT_400,
                                        expand=True,
                                    ),
                                    ft.IconButton(
                                        icon=ft.Icons.DELETE_OUTLINE,
                                        icon_color=ft.Colors.RED_400,
                                        tooltip="Видалити замовлення",
                                        on_click=lambda e, idx=i: page.run_task(delete_order, idx),
                                    ),
                                ]
                            ),
                            ft.Divider(height=4, color=ft.Colors.GREY_700),
                            ft.Text(f"Форма: {order.get('shape', '—')}", color=ft.Colors.WHITE, font_family='Text'),
                            ft.Text(f"Деревина: {order.get('wood', '—')}", color=ft.Colors.WHITE, font_family='Text'),
                            ft.Text(f"Бридж: {order.get('bridge', '—')}", color=ft.Colors.WHITE, font_family='Text'),
                            ft.Text(f"Лади: {order.get('frets', '—')}", color=ft.Colors.WHITE, font_family='Text'),
                            ft.Text(f"Колір: {order.get('color', '—')}", color=ft.Colors.WHITE, font_family='Text'),
                            ft.Text(f"Ціна: {order.get('total', '—')} ₴", color=ft.Colors.YELLOW_ACCENT_400, font_family='Text'),
                        ],
                        spacing=6,
                        expand=True,
                    ),
                ],
                spacing=16,
                vertical_alignment=ft.CrossAxisAlignment.START,
            )

            cards.append(
                ft.Container(
                    content=card_controls,
                    bgcolor=ft.Colors.GREY_900,
                    border_radius=12,
                    padding=16,
                    margin=ft.Margin(0, 0, 0, 14),
                )
            )

        return ft.Column(cards, scroll=ft.ScrollMode.ADAPTIVE)

    orders_container = ft.Container(
        content=build_orders_content(),
        padding=16,
        expand=True,
    )

    return ft.View(
        route="/orders",
        controls=[
            ft.AppBar(
                title=ft.Text("Мої замовлення", color=ft.Colors.YELLOW_ACCENT_400, font_family='Text'),
                actions=[
                    ft.IconButton(
                        ft.Icons.HOME,
                        icon_color=ft.Colors.YELLOW_ACCENT_400,
                        on_click=go_gallery,
                    ),
                    ft.IconButton(
                        ft.Icons.ARROW_BACK,
                        icon_color=ft.Colors.YELLOW_ACCENT_400,
                        on_click=go_home,
                    )
                ],
                **appbar_STYLE,
            ),
            orders_container,
        ],
    )