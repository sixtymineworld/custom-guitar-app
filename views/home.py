import flet as ft
import os
import json
from models.styles import *

ORDERS_FILE = "orders.json"

_DIR = os.path.dirname(os.path.dirname(__file__))
with open(os.path.join(_DIR, "storage", "prices.json"), encoding="utf-8") as f:
    PRICES = json.load(f)

def calculate_price(model_key, wood, bridge, frets, color):
    base = PRICES["guitars"][model_key]["base"]
    w = PRICES["woods"].get(wood, 0)
    b = PRICES["bridges"].get(bridge, 0)
    f = PRICES["frets"].get(str(frets), 0)
    c = PRICES["colors"].get(color, 0)
    return base + w + b + f + c, {"base": base, "wood": w, "bridge": b, "frets": f, "color": c}


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


def home_view(page):
    bg_container = ft.Ref[ft.Container]()

    def get_gradient():
        if page.theme_mode == ft.ThemeMode.DARK:
            return ft.LinearGradient(
                begin=ft.Alignment(0, -1),
                end=ft.Alignment(0, 1),
                colors=[
                    "#000000",
                    "#0D0D00",
                    "#1A1A00",
                    "#2E2A00",
                    "#0D0D00",
                    "#000000",
                ],
                stops=[0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
            )
        else:
            return ft.LinearGradient(
                begin=ft.Alignment(0, -1),
                end=ft.Alignment(0, 1),
                colors=[
                    "#fffff0",
                    "#fffde7",
                    "#fff9c4",
                    "#fff59d",
                    "#fffde7",
                    "#ffffff",
                ],
                stops=[0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
            )

    def get_page_bgcolor():
        return "#000000" if page.theme_mode == ft.ThemeMode.DARK else "#fffff0"

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

            bg_container.current.gradient = get_gradient()
            page.bgcolor = get_page_bgcolor()
            page.update()

        async def logout(e):
            page.session.store.clear()
            page.theme_mode = ft.ThemeMode.LIGHT
            page.bgcolor = get_page_bgcolor()
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
                    ft.Button(
                        "Вийти з акаунту",
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
    dd_shape = ft.Dropdown(label="Форма гітари", options=[ft.DropdownOption(k) for k in GUITARS], width=340)

    result_text = ft.Text("", text_align=ft.TextAlign.CENTER)
    price_col = ft.Column(visible=False, spacing=4, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
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
        dd_wood.options   = [ft.DropdownOption(o) for o in data["woods"]]
        dd_bridge.options = [ft.DropdownOption(o) for o in data["bridges"]]
        dd_frets.options  = [ft.DropdownOption(o) for o in data["frets"]]
        dd_color.options  = [ft.DropdownOption(o) for o in data["colors"]]
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
            total, parts = calculate_price(
                selected["shape"], dd_wood.value, dd_bridge.value, dd_frets.value, dd_color.value
            )
            price_col.controls = [
                ft.Text(f"База ({selected['shape']}):  {parts['base']} ₴", size=13),
                ft.Text(f"Деревина ({dd_wood.value}): +{parts['wood']} ₴", size=13),
                ft.Text(f"Бридж ({dd_bridge.value}): +{parts['bridge']} ₴", size=13),
                ft.Text(f"Лади ({dd_frets.value}): +{parts['frets']} ₴", size=13),
                ft.Text(f"Колір ({dd_color.value}): +{parts['color']} ₴", size=13),
                ft.Divider(height=8),
                ft.Text(f"Разом: {total} ₴", weight=ft.FontWeight.BOLD, size=16,
                        color=ft.Colors.YELLOW_ACCENT_400),
            ]
            price_col.visible = True
            order_btn.visible = True
        else:
            price_col.visible = False
            order_btn.visible = False
        page.update()

    dd_shape.on_select = on_shape_select
    dd_wood.on_select   = on_option_change
    dd_bridge.on_select = on_option_change
    dd_frets.on_select  = on_option_change
    dd_color.on_select  = on_option_change 

    async def on_order_click(e):
        username = page.session.store.get("current_user")
        shape    = selected["shape"]
        img_src  = f"{shape}.jpg"
        total, parts = calculate_price(shape, dd_wood.value, dd_bridge.value, dd_frets.value, dd_color.value)

        async def close_confirm(e):
            confirm_dialog.open = False
            page.update()

        async def do_order(e):
            confirm_dialog.open = False
            page.update()

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
            price_col.visible = False
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
                title=ft.Text("Замовлення прийнято! 🎸", font_family='Text'),
                content=ft.Text("Вашу гітару успішно створено. Переглянути його можна в розділі замовлень.", font_family='Text'),
                actions=[
                    ft.TextButton("Переглянути", on_click=go_to_orders),
                    ft.TextButton("Закрити", on_click=close),
                ],
            )
            page.overlay.append(img_dialog)
            img_dialog.open = True
            page.update()

        confirm_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"Підтвердити замовлення — {shape}", weight=ft.FontWeight.BOLD, font_family='Text'),
            content=ft.Column(
                width=360,
                tight=True,
                spacing=4,
                controls=[
                    ft.Text(f"База ({shape}):  {parts['base']} ₴", size=13, font_family='Text'),
                    ft.Text(f"Деревина ({dd_wood.value}): +{parts['wood']} ₴", size=13, font_family='Text'),
                    ft.Text(f"Бридж ({dd_bridge.value}): +{parts['bridge']} ₴", size=13, font_family='Text'),
                    ft.Text(f"Лади ({dd_frets.value}): +{parts['frets']} ₴", size=13, font_family='Text'),
                    ft.Text(f"Колір ({dd_color.value}): +{parts['color']} ₴", size=13, font_family='Text'),
                    ft.Divider(height=8),
                    ft.Text(f"Разом: {total} ₴", weight=ft.FontWeight.BOLD, size=16, font_family='Text'),
                ],
            ),
            actions=[
                ft.TextButton("Скасувати", on_click=close_confirm),
                ft.FilledButton(
                    "Підтвердити замовлення",
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.YELLOW_ACCENT_400,
                        color=ft.Colors.BLACK,
                    ),
                    on_click=do_order,
                ),
            ],
        )
        page.overlay.append(confirm_dialog)
        confirm_dialog.open = True
        page.update()

    order_btn.on_click = on_order_click

    return ft.View(
        route="/home",
        bgcolor=ft.Colors.TRANSPARENT,
        padding=0,
        controls=[
            ft.AppBar(
                title=ft.Text("Guitar Custom", color=ft.Colors.YELLOW_ACCENT_400, font_family='Title'),
                **appbar_STYLE,
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
                ref=bg_container,
                expand=True,
                padding=0,
                animate=ft.Animation(400, ft.AnimationCurve.EASE_IN_OUT),
                gradient=get_gradient(),
                content=ft.Column(
                    tight=True,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    scroll=ft.ScrollMode.ADAPTIVE,
                    controls=[
                        ft.Container(height=24),
                        ft.Text(
                            "Зберіть свою гітару",
                            size=24,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.YELLOW_ACCENT_400,
                            font_family='Text'
                        ),
                        ft.Text(
                            "Оберіть параметри нижче",
                            size=13,
                            color=ft.Colors.GREY_500,
                            font_family='Text'
                        ),
                        ft.Container(height=16),
                        dd_shape,
                        dd_wood,
                        dd_bridge,
                        dd_frets,
                        dd_color,
                        ft.Container(height=8),
                        result_text,
                        price_col,
                        order_btn,
                        ft.Container(height=24),
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
                            ft.Text("Guitar Custom", size=20,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.YELLOW_ACCENT_400,
                                    font_family='Title'),
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
                                ],
                            ),
                            ft.Row(
                                controls=[
                                    ft.IconButton(icon=ft.Icons.FACEBOOK,
                                                  icon_color=ft.Colors.WHITE,
                                                  style=icon_button_STYLE,
                                                  url="https://www.facebook.com/groups/1548580592066473/"),
                                    ft.IconButton(icon=ft.Icons.PLAY_CIRCLE,
                                                  icon_color=ft.Colors.WHITE,
                                                  style=icon_button_STYLE,
                                                  url="https://www.youtube.com/@CrimsonCustomGuitars"),
                                ],
                            ),
                        ],
                    ),
                    ft.Divider(color=ft.Colors.GREY_700, height=16),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.Text("© 2026 Guitar Custom", size=11, color=ft.Colors.GREY_500, font_family='Title'),
                        ],
                    ),
                ],
            ),
        ),
    )