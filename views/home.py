import flet as ft
import os
import json
from models.styles import *

ORDERS_FILE = "orders.json"
ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")

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
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.LOGOUT, color=ft.Colors.RED),
                        title=ft.Text("Вийти з акаунту", color=ft.Colors.RED),
                        on_click=logout,
                    ),
                ],
            ),
            actions=[ft.TextButton("Закрити", on_click=close_dialog)],
        )
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    async def go_orders(e):
        await page.push_route("/orders")

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

    dd_wood   = ft.Dropdown(label="Деревина", options=[], width=300)
    dd_bridge = ft.Dropdown(label="Бридж", options=[], width=300)
    dd_frets  = ft.Dropdown(label="Кількість ладів", options=[], width=300)
    dd_color  = ft.Dropdown(label="Колір", options=[], width=300)

    result_text = ft.Text("")
    selected = {"shape": None}

    order_btn = ft.Button(
        "Замовити",
        icon=ft.Icons.SHOPPING_CART,
        visible=False,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.YELLOW_ACCENT_700,
            color=ft.Colors.BLACK,
        ),
    )

    def on_shape_select(e):
        shape = e.control.value
        selected["shape"] = shape
        data = GUITARS[shape]

        dd_wood.options   = [ft.dropdown.Option(o) for o in data["woods"]]
        dd_bridge.options = [ft.dropdown.Option(o) for o in data["bridges"]]
        dd_frets.options  = [ft.dropdown.Option(o) for o in data["frets"]]
        dd_color.options  = [ft.dropdown.Option(o) for o in data["colors"]]

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
        options=[ft.dropdown.Option(k) for k in GUITARS],
        on_select=on_shape_select,
        width=300,
    )

    async def on_order_click(e):
        username = page.session.store.get("current_user")
        shape = selected["shape"]

        img_path = os.path.join(ASSETS_DIR, f"{shape}.jpg")

        print(f"ASSETS_DIR: {ASSETS_DIR}")
        print(f"img_path: {img_path}")
        print(f"exists: {os.path.exists(img_path)}")

        order = {
            "user": username,
            "shape": shape,
            "wood": dd_wood.value,
            "bridge": dd_bridge.value,
            "frets": dd_frets.value,
            "color": dd_color.value,
            "image_path": img_path,
        }
        save_order(username, order)

        # скидання полів
        selected["shape"] = None
        dd_shape.value = None
        dd_wood.options = dd_bridge.options = dd_frets.options = dd_color.options = []
        dd_wood.value = dd_bridge.value = dd_frets.value = dd_color.value = None
        result_text.value = ""
        order_btn.visible = False

        page.snack_bar = ft.SnackBar(
            content=ft.Text(f"✅ Замовлення прийнято, {username}!"),
            bgcolor=ft.Colors.GREEN_700,
            duration=3000,
        )
        page.snack_bar.open = True
        page.update()

        if os.path.exists(img_path):
            async def close(e):
                img_dialog.open = False
                page.update()

            img_dialog = ft.AlertDialog(
                modal=True,
                title=ft.Text("Приблизний вигляд", color=ft.Colors.YELLOW_ACCENT_400),
                content=ft.Image(src=img_path, width=400, height=400),  # ← без fit
                actions=[ft.TextButton("Закрити", on_click=close)],
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
                    ft.IconButton(
                        icon=ft.Icons.SETTINGS,
                        icon_color=ft.Colors.YELLOW_ACCENT_400,
                        on_click=show_settings_dialog,
                    ),
                    ft.IconButton(
                        icon=ft.Icons.SHOPPING_BASKET_SHARP,
                        icon_color=ft.Colors.YELLOW_ACCENT_400,
                        on_click=go_orders,
                    ),
                ],
            ),
            ft.Column(
                [
                    dd_shape,
                    dd_wood,
                    dd_bridge,
                    dd_frets,
                    dd_color,
                    result_text,
                    order_btn,
                ],
                scroll=ft.ScrollMode.ADAPTIVE,
                expand=True,
            ),
        ],
    )