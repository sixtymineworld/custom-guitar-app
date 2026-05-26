import flet as ft
import json
from models.styles import *
import os

ORDERS_FILE = "orders.json"

_DIR = os.path.dirname(os.path.dirname(__file__))
with open(os.path.join(_DIR, "storage", "prices.json"), encoding="utf-8") as f:
    PRICES = json.load(f)

GUITARS = [
    {
        "name": "Stratocaster",
        "key": "Stratocaster",
        "src": "Stratocaster.jpg",
        "desc": "Створена Fender у 1954. Три звукознімачі, контурний корпус, улюблениця блюзу та рок-н-ролу.",
        "youtube": "https://youtu.be/7g_uA4GBXf8?si=YKc9w1CVXLg6tlvl",
    },
    {
        "name": "Les Paul",
        "key": "Les-Paul",
        "src": "Les-Paul.jpg",
        "desc": "Gibson, 1952. Масивний корпус з махагону, два хамбакери — потужний, теплий звук.",
        "youtube": "https://youtu.be/y_Aima0D5Dc?si=6uaq9Fz8rle8fP14",
    },
    {
        "name": "SG",
        "key": "SG",
        "src": "SG.jpg",
        "desc": "Gibson, 1961. Тонкий корпус, гострі ріжки — агресивний вигляд і легкий доступ до верхніх ладів.",
        "youtube": "https://youtu.be/ZwZeO5SpDus?si=6wdg8Tf-jeIXXXNr",
    },
    {
        "name": "Telecaster",
        "key": "Telecaster",
        "src": "Telecaster.jpg",
        "desc": "Fender, 1950. Перша масова електрогітара. Різкий звук, простота, надійність.",
        "youtube": "https://youtu.be/WonBtP-Bihg?si=mtqaRE2KaezMffO5",
    },
    {
        "name": "Explorer",
        "key": "Explorer",
        "src": "Explorer.jpg",
        "desc": "Gibson, 1958. Футуристична форма, потужний звук — обрана хард-рок та метал музикантами.",
        "youtube": "https://youtu.be/2EOYNUPPQb4?si=N5nCXHPIbC1ce1eq",
    },
    {
        "name": "Flying V",
        "key": "Flying-V",
        "src": "Flying-V.jpg",
        "desc": "Gibson, 1958. V-подібний корпус став символом хард-року та важкого металу.",
        "youtube": "https://youtu.be/ju8Wu42hhbk?si=CsD9VfaduUpo38Lh",
    },
    {
        "name": "Jazzmaster",
        "key": "Jazzmaster",
        "src": "Jazzmaster.jpg",
        "desc": "Fender, 1958. Великий корпус, м'який звук — популярна в джазі та альтернативному році.",
        "youtube": "https://youtu.be/rqb1bv2IIxs?si=igHv6l7K0JUj_Vb-",
    },
    {
        "name": "Baritone",
        "key": "Baritone",
        "src": "Baritone.jpg",
        "desc": "Довший мензурний, нижчий стрій — улюблениця метал та саундтрек-композиторів.",
        "youtube": "https://youtu.be/RQop7woOVYY?si=0RqMRLfTy6hY1WsT",
    },
    {
        "name": "Superstrat",
        "key": "Superstrat",
        "src": "Superstrat.jpg",
        "desc": "80-ті роки. Strat-форма з хамбакером на бриджі — створена для швидкої гри та хай-гейну.",
        "youtube": "https://youtu.be/lIOg8c_lyqs?si=42_rcUhgfLTifCgQ",
    },
    {
        "name": "V-Shape (Dean)",
        "key": "V-Shape-(Dean)",
        "src": "V-Shape-(Dean).jpg",
        "desc": "Dean, 1977. Екстремальна V-форма, фірмовий знак металу та шред-гітаристів.",
        "youtube": "https://youtu.be/WApS6oFEmfY?si=TU7ZFC7FH3fVNyVG",
    },
]
def save_order(username, order):
    if not os.path.exists(ORDERS_FILE):
        all_orders = {}
    else:
        with open(ORDERS_FILE, "r", encoding="utf-8") as f:
            all_orders = json.load(f)
    if username not in all_orders:
        all_orders[username] = []
    all_orders[username].append(order)
    with open(ORDERS_FILE, "w", encoding="utf-8") as f:
        json.dump(all_orders, f, indent=4, ensure_ascii=False)


def calculate_price(model_key, wood, bridge, frets, color):
    base = PRICES["guitars"][model_key]["base"]
    w = PRICES["woods"].get(wood, 0)
    b = PRICES["bridges"].get(bridge, 0)
    f = PRICES["frets"].get(str(frets), 0)
    c = PRICES["colors"].get(color, 0)
    return base + w + b + f + c, {"base": base, "wood": w, "bridge": b, "frets": f, "color": c}


def build_order_dialog(page, guitar):
    key = guitar["key"]
    woods = list(PRICES["woods"].keys())
    bridges = list(PRICES["bridges"].keys())
    frets_list = list(PRICES["frets"].keys())
    colors = list(PRICES["colors"].keys())

    # Фіксовані дефолтні значення
    fixed = {
        "wood": woods[0],
        "bridge": bridges[0],
        "frets": frets_list[0],
        "color": colors[0],
    }

    total, parts = calculate_price(key, fixed["wood"], fixed["bridge"], fixed["frets"], fixed["color"])

    def make_dd(label, options, value):
        return ft.Dropdown(
            label=label,
            value=value,
            options=[ft.DropdownOption(o) for o in options],
            width=320,
            disabled=True,
        )

    async def confirm(e):
        dialog.open = False
        page.update()

        username = page.session.store.get("current_user")
        order = {
            "user": username,
            "shape": guitar["name"],
            "wood": fixed["wood"],
            "bridge": fixed["bridge"],
            "frets": fixed["frets"],
            "color": fixed["color"],
            "image_path": guitar["src"],
        }
        save_order(username, order)

        async def close(e2):
            confirm_dialog.open = False
            page.update()

        async def go_to_orders(e2):
            confirm_dialog.open = False
            page.update()
            await page.push_route("/orders")

        confirm_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Замовлення прийнято! 🎸", color=ft.Colors.YELLOW_ACCENT_400),
            content=ft.Text("Вашу гітару успішно створено. Переглянути його можна в розділі замовлень."),
            actions=[
                ft.TextButton("Переглянути", on_click=go_to_orders),
                ft.TextButton("Закрити", on_click=close),
            ],
        )
        page.overlay.append(confirm_dialog)
        confirm_dialog.open = True
        page.update()

    async def close(e):
        dialog.open = False
        page.update()

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text(f"Замовити — {guitar['name']}", weight=ft.FontWeight.BOLD),
        content=ft.Column(
            scroll=ft.ScrollMode.ADAPTIVE,
            width=360,
            controls=[
                make_dd("Деревина", woods, fixed["wood"]),
                make_dd("Бридж", bridges, fixed["bridge"]),
                make_dd("Кількість ладів", frets_list, fixed["frets"]),
                make_dd("Колір", colors, fixed["color"]),
                ft.Divider(height=20),
                ft.Column(
                    spacing=4,
                    controls=[
                        ft.Text(f"База ({guitar['name']}):  {parts['base']} ₴", size=13),
                        ft.Text(f"Деревина ({fixed['wood']}): +{parts['wood']} ₴", size=13),
                        ft.Text(f"Бридж ({fixed['bridge']}): +{parts['bridge']} ₴", size=13),
                        ft.Text(f"Лади ({fixed['frets']}): +{parts['frets']} ₴", size=13),
                        ft.Text(f"Колір ({fixed['color']}): +{parts['color']} ₴", size=13),
                    ],
                ),
                ft.Divider(height=8),
                ft.Text(f"Разом: {total} ₴", weight=ft.FontWeight.BOLD, size=16),
            ],
            tight=True,
        ),
        actions=[
            ft.TextButton("Скасувати", on_click=close),
            ft.FilledButton(
                "Підтвердити замовлення",
                style=ft.ButtonStyle(
                    bgcolor=ft.Colors.YELLOW_ACCENT_400,
                    color=ft.Colors.BLACK,
                ),
                on_click=confirm,
            ),
        ],
    )
    return dialog


def guitar_card(guitar, page):
    async def open_buy(e):
        dialog = build_order_dialog(page, guitar)
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    return ft.Container(
        width=320,
        border_radius=20,
        bgcolor="#1A1A1A",
        content=ft.Column(
            spacing=0,
            controls=[
                ft.Image(
                    src=guitar["src"],
                    width=320,
                    height=210,
                    fit=ft.BoxFit.COVER,
                ),
                ft.Container(
                    padding=16,
                    content=ft.Column(
                        spacing=10,
                        controls=[
                            ft.Text(
                                guitar["name"],
                                size=17,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.WHITE,
                            ),
                            ft.Text(
                                guitar["desc"],
                                size=12,
                                color="#9E9E9E",
                                max_lines=3,
                                overflow=ft.TextOverflow.ELLIPSIS,
                            ),
                            ft.Divider(height=1, color="#2A2A2A"),
                            ft.Row(
                                spacing=10,
                                controls=[
                                    ft.OutlinedButton(
                                        "Дізнатись",
                                        icon=ft.Icons.PLAY_CIRCLE_OUTLINE_ROUNDED,
                                        url=guitar["youtube"],
                                        expand=1,
                                        style=ft.ButtonStyle(
                                            color="#FFD600",
                                            side=ft.BorderSide(1, "#FFD600"),
                                            shape=ft.RoundedRectangleBorder(radius=10),
                                            padding=12,
                                        ),
                                    ),
                                    ft.FilledButton(
                                        "Купити",
                                        icon=ft.Icons.SHOPPING_CART_ROUNDED,
                                        on_click=open_buy,
                                        expand=1,
                                        style=ft.ButtonStyle(
                                            bgcolor="#FFD600",
                                            color=ft.Colors.BLACK,
                                            shape=ft.RoundedRectangleBorder(radius=10),
                                            padding=12,
                                        ),
                                    ),
                                ],
                            ),
                        ],
                    ),
                ),
            ],
        ),
    )


def gallery_view(page):
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
    
    async def go_home(e):
        await page.push_route("/home")
    
    async def go_orders(e):
        await page.push_route("/orders")

    async def go_hero(e):
        await page.push_route("/")

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

    cards = ft.Row(
        wrap=True,
        spacing=20,
        run_spacing=20,
        controls=[guitar_card(g, page) for g in GUITARS],
    )

    return ft.View(
        route="/gallery",
        padding=0,
        controls=[
            ft.AppBar(
                **appbar_STYLE,
                title=ft.Text("Guitar Custom", color=ft.Colors.YELLOW_ACCENT_400, font_family='AppleGaramond'),
                actions=[
                    ft.Button(
                        'Створити свою',
                        icon=ft.Icons.ADD,
                        tooltip="Створення своєї гітари",
                        style=btn_style,
                        on_click=go_home,
                    ),
                    ft.IconButton(
                        icon=ft.Icons.SETTINGS,
                        icon_color=ft.Colors.YELLOW_ACCENT_400,
                        tooltip="Налаштування",
                        on_click=show_settings_dialog,
                    ),
                    ft.IconButton(icon=ft.Icons.SHOPPING_BASKET,
                                  icon_color=ft.Colors.YELLOW_ACCENT_400,
                                  tooltip="Ваші замовлення",
                                  on_click=go_orders),
                    ft.Container(width=12),
                ],
            ),
            ft.Container(
                ref=bg_container, 
                gradient=get_gradient(),
                expand=True,
                padding=ft.Padding(left=32, right=32, top=24, bottom=24),
                content=ft.Column(
                    scroll=ft.ScrollMode.ADAPTIVE,
                    expand=True,
                    controls=[
                        ft.Text("Форми гітар", size=28, weight=ft.FontWeight.BOLD),
                        ft.Text("Обери форму та дізнайся її історію", size=14),
                        ft.Container(height=16),
                        cards,
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
                            ft.Text("Guitar Custom", size=20, weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.YELLOW_ACCENT_400, font_family='AppleGaramond'),
                            ft.Row(controls=[
                                ft.TextButton("Головна",
                                              style=ft.ButtonStyle(color=ft.Colors.WHITE),
                                              on_click=go_hero),
                                ft.TextButton("Каталог",
                                              style=ft.ButtonStyle(color=ft.Colors.WHITE)),
                                ft.TextButton("Замовлення",
                                              style=ft.ButtonStyle(color=ft.Colors.WHITE)),
                            ]),
                            ft.Row(controls=[
                                ft.IconButton(
                                    icon=ft.Icons.FACEBOOK,
                                    icon_color=ft.Colors.WHITE,
                                    style=icon_button_STYLE,
                                    url='https://www.facebook.com/groups/1548580592066473/',
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.PLAY_CIRCLE,
                                    icon_color=ft.Colors.WHITE,
                                    style=icon_button_STYLE,
                                    url='https://www.youtube.com/@CrimsonCustomGuitars',
                                ),
                            ]),
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