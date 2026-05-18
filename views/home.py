import flet as ft
import os
import json
from models.styles import *

ORDERS_FILE = "orders.json"


def load_orders():
    if not os.path.exists(ORDERS_FILE):
        return {}
    with open(ORDERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_order(username, order):
    all_orders = load_orders()
    if username not in all_orders:
        all_orders[username] = []
    all_orders[username].append(order)
    with open(ORDERS_FILE, "w", encoding="utf-8") as f:
        json.dump(all_orders, f, indent=4, ensure_ascii=False)


def home_view(page: ft.Page):
    async def show_settings_dialog(e):
        prefs = ft.SharedPreferences()
        saved_theme = await prefs.get("theme")
        page.theme_mode = ft.ThemeMode.DARK if saved_theme == "dark" else ft.ThemeMode.LIGHT

        async def toggle_theme(e):
            if page.theme_mode == ft.ThemeMode.DARK:
                page.theme_mode = ft.ThemeMode.LIGHT
                await prefs.set("theme", "light")
            else:
                page.theme_mode = ft.ThemeMode.DARK
                await prefs.set("theme", "dark")
            page.update()

        async def logout(e):
            page.session.store.clear()
            page.theme_mode = ft.ThemeMode.LIGHT
            await page.push_route("/login")

        theme_switch = ft.Switch(
            label="Темна тема" if page.theme_mode == ft.ThemeMode.DARK else "Світла тема",
            value=(page.theme_mode == ft.ThemeMode.DARK),
            on_change=toggle_theme,
        )

        async def close_dialog(e):
            dialog.open = False
            page.update()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Налаштування"),
            content=ft.Column(
                [
                    theme_switch,
                    ft.Divider(),
                    ft.Button("Вийти з акаунту",
                              color=ft.Colors.RED,
                              icon=ft.Icons.LOGOUT,
                              on_click=logout,
                    ),
                ],
                tight=True,
                width=300,
            ),
            actions=[ft.TextButton("Закрити", on_click=close_dialog)],
        )
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    async def go_orders(e):
        await page.push_route("/orders")

    async def go_hero(e):
        await page.push_route("/")

    async def go_gallery(e):
        await page.push_route("/gallery")

    def load_data():
        try:
            path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "storage", "guitars.json",
            )
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    return json.load(f)
            return {}
        except Exception:
            return {}

    GUITARS = load_data()

    dd_wood = ft.Dropdown(label="Деревина", options=[], width=340)
    dd_bridge = ft.Dropdown(label="Бридж", options=[], width=340)
    dd_frets = ft.Dropdown(label="Кількість ладів", options=[], width=340)
    dd_color = ft.Dropdown(label="Колір", options=[], width=340)

    result_text = ft.Text("", text_align=ft.TextAlign.CENTER)
    selected = {"shape": None}

    order_btn = ft.Button(
        "Замовити",
        icon=ft.Icons.SHOPPING_CART,
        visible=False,
        style=button_STYLE,
    )

    def on_shape_select(e):
        shape = e.control.value
        selected["shape"] = shape
        data = GUITARS[shape]
        dd_wood.options = [ft.DropdownOption(o) for o in data["woods"]]
        dd_bridge.options = [ft.DropdownOption(o) for o in data["bridges"]]
        dd_frets.options = [ft.DropdownOption(o) for o in data["frets"]]
        dd_color.options = [ft.DropdownOption(o) for o in data["colors"]]
        dd_wood.value = dd_bridge.value = dd_frets.value = dd_color.value = None
        result_text.value = ""
        order_btn.visible = False
        page.update()

    def on_option_change(e):
        if all([selected["shape"], dd_wood.value, dd_bridge.value, dd_frets.value, dd_color.value]):
            result_text.value = (
                f"✅ {selected['shape']} | {dd_wood.value} | "
                f"{dd_bridge.value} | {dd_frets.value} ладів | {dd_color.value}"
            )
            order_btn.visible = True
        else:
            order_btn.visible = False
        page.update()

    dd_wood.on_select   = on_option_change
    dd_bridge.on_select = on_option_change
    dd_frets.on_select  = on_option_change
    dd_color.on_select  = on_option_change

    dd_shape = ft.Dropdown(
        label="Форма гітари",
        options=[ft.DropdownOption(k) for k in GUITARS],
        on_select=on_shape_select,
        width=340,
    )

    async def on_order_click(e):
        username = page.session.store.get("current_user")
        shape = selected["shape"]
        img_src = f"{shape}.jpg"

        order = {
            "user": username,
            "shape": shape,
            "wood": dd_wood.value,
            "bridge": dd_bridge.value,
            "frets": dd_frets.value,
            "color": dd_color.value,
            "image_path": img_src,
        }
        save_order(username, order)

        selected["shape"] = None
        dd_shape.value = None
        dd_wood.options = dd_bridge.options = dd_frets.options = dd_color.options = []
        dd_wood.value = dd_bridge.value = dd_frets.value = dd_color.value = None
        result_text.value = ""
        order_btn.visible = False
        page.update()

        async def close(e):
            img_dialog.open = False
            page.update()

        async def go_to_orders(e):
            img_dialog.open = False
            page.update()
            await page.push_route("/orders")

        img_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Замовлення прийнято! 🎸", color=ft.Colors.YELLOW_ACCENT_400),
            content=ft.Text("Вашу гітару успішно створено. Переглянути його можна в розділі замовлень."),
            actions=[
                ft.TextButton("Переглянути",
                              on_click=go_to_orders),
                ft.TextButton("Закрити",
                              on_click=close),
            ],
        )
        page.overlay.append(img_dialog)
        img_dialog.open = True
        page.update()

    order_btn.on_click = on_order_click

    return ft.View(
        route="/home",
        controls=[
            ft.AppBar(
                title=ft.Text("Guitar Custom", color=ft.Colors.YELLOW_ACCENT_400),
                bgcolor=ft.Colors.GREY_900,
                actions=[
                    ft.IconButton(icon=ft.Icons.SETTINGS,
                                  icon_color=ft.Colors.YELLOW_ACCENT_400,
                                  tooltip="Налаштування",
                                  on_click=show_settings_dialog),
                    ft.IconButton(icon=ft.Icons.SHOPPING_BASKET,
                                  icon_color=ft.Colors.YELLOW_ACCENT_400,
                                  tooltip="Ваші замовлення",
                                  on_click=go_orders),
                    ft.IconButton(icon=ft.Icons.HOME,
                                  icon_color=ft.Colors.YELLOW_ACCENT_400,
                                  tooltip="Головна",
                                  on_click=go_hero),
                    ft.IconButton(icon=ft.Icons.MUSIC_NOTE,
                                  icon_color=ft.Colors.YELLOW_ACCENT_400,
                                  tooltip="Галерея гітар",
                                  on_click=go_gallery),
                ],
            ),

            ft.Container(
                expand=True,
                alignment=ft.Alignment(0, 0),
                content=ft.Column(
                    tight=True,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    scroll=ft.ScrollMode.ADAPTIVE,
                    controls=[
                        ft.Text(
                            "Зберіть свою гітару",
                            size=24,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.YELLOW_ACCENT_400,
                        ),
                        ft.Text(
                            "Оберіть параметри нижче",
                            size=13,
                            color=ft.Colors.GREY_500,
                        ),
                        ft.Container(height=16),
                        dd_shape,
                        dd_wood,
                        dd_bridge,
                        dd_frets,
                        dd_color,
                        ft.Container(height=8),
                        result_text,
                        order_btn,
                    ],
                ),
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
                                    ft.TextButton("Головна",
                                                  style=ft.ButtonStyle(color=ft.Colors.WHITE),
                                                  on_click=go_hero),
                                    ft.TextButton("Каталог",
                                                  style=ft.ButtonStyle(color=ft.Colors.WHITE),
                                                  on_click=go_gallery),
                                    ft.TextButton("Замовлення",
                                                  style=ft.ButtonStyle(color=ft.Colors.WHITE),
                                                  on_click=go_orders),
                                ]
                            ),
                            ft.Row(
                                controls=[
                                    ft.IconButton(icon=ft.Icons.FACEBOOK,
                                                  icon_color=ft.Colors.WHITE,
                                                  style=icon_button_STYLE,
                                                  url='https://www.facebook.com/'),
                                    ft.IconButton(icon=ft.Icons.MAIL,
                                                  icon_color=ft.Colors.WHITE,
                                                  style=icon_button_STYLE,
                                                  url='https://mail.google.com/'),
                                ]
                            ),
                        ],
                    ),
                    ft.Divider(color=ft.Colors.GREY_700, height=16),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.Text("© 2026 Guitar Custom", size=11, color=ft.Colors.GREY_500),
                        ],
                    ),
                ],
            ),
        ),
    )