import flet as ft
import json
from models.styles import *
import os

_DIR = os.path.dirname(os.path.dirname(__file__))
with open(os.path.join(_DIR, "storage", "prices.json"), encoding="utf-8") as f:
    PRICES = json.load(f)

GUITARS = [
    {
        "name": "Stratocaster",
        "key": "Stratocaster",
        "src": "Stratocaster.jpg",
        "desc": "Створена Fender у 1954. Три звукознімачі, контурний корпус, улюблениця блюзу та рок-н-ролу.",
        "youtube": "https://www.youtube.com/watch?v=5FMDNqfl5bk",
    },
    {
        "name": "Les Paul",
        "key": "Les-Paul",
        "src": "Les-Paul.jpg",
        "desc": "Gibson, 1952. Масивний корпус з махагону, два хамбакери — потужний, теплий звук.",
        "youtube": "https://www.youtube.com/watch?v=oS4C-a6Oyqs",
    },
    {
        "name": "SG",
        "key": "SG",
        "src": "SG.jpg",
        "desc": "Gibson, 1961. Тонкий корпус, гострі ріжки — агресивний вигляд і легкий доступ до верхніх ладів.",
        "youtube": "https://www.youtube.com/watch?v=WPYiNKuL8II",
    },
    {
        "name": "Telecaster",
        "key": "Telecaster",
        "src": "Telecaster.jpg",
        "desc": "Fender, 1950. Перша масова електрогітара. Різкий звук, простота, надійність.",
        "youtube": "https://www.youtube.com/watch?v=bQNpJl1WwH4",
    },
    {
        "name": "Explorer",
        "key": "Explorer",
        "src": "Explorer.jpg",
        "desc": "Gibson, 1958. Футуристична форма, потужний звук — обрана хард-рок та метал музикантами.",
        "youtube": "https://www.youtube.com/watch?v=JWZzgaKMcwI",
    },
    {
        "name": "Flying V",
        "key": "Flying-V",
        "src": "Flying-V.jpg",
        "desc": "Gibson, 1958. V-подібний корпус став символом хард-року та важкого металу.",
        "youtube": "https://www.youtube.com/watch?v=4DgABcXUNcs",
    },
    {
        "name": "Jazzmaster",
        "key": "Jazzmaster",
        "src": "Jazzmaster.jpg",
        "desc": "Fender, 1958. Великий корпус, м'який звук — популярна в джазі та альтернативному році.",
        "youtube": "https://www.youtube.com/watch?v=F5n3bqXifT4",
    },
    {
        "name": "Baritone",
        "key": "Baritone",
        "src": "Baritone.jpg",
        "desc": "Довший мензурний, нижчий стрій — улюблениця метал та саундтрек-композиторів.",
        "youtube": "https://www.youtube.com/watch?v=F1Y6kBL5CEU",
    },
    {
        "name": "Superstrat",
        "key": "Superstrat",
        "src": "Superstrat.jpg",
        "desc": "80-ті роки. Strat-форма з хамбакером на бриджі — створена для швидкої гри та хай-гейну.",
        "youtube": "https://www.youtube.com/watch?v=TpHCJ56xJmk",
    },
    {
        "name": "V-Shape (Dean)",
        "key": "V-Shape-(Dean)",
        "src": "V-Shape-(Dean).jpg",
        "desc": "Dean, 1977. Екстремальна V-форма, фірмовий знак металу та шред-гітаристів.",
        "youtube": "https://www.youtube.com/watch?v=qGp6GGjl_40",
    },
]


def calculate_price(model_key, wood, bridge, frets, color):
    base = PRICES["guitars"][model_key]["base"]
    w    = PRICES["woods"].get(wood, 0)
    b    = PRICES["bridges"].get(bridge, 0)
    f    = PRICES["frets"].get(str(frets), 0)
    c    = PRICES["colors"].get(color, 0)
    return base + w + b + f + c, {"base": base, "wood": w, "bridge": b, "frets": f, "color": c}


def build_order_dialog(page, guitar):
    key = guitar["key"]
    woods   = list(PRICES["woods"].keys())
    bridges = list(PRICES["bridges"].keys())
    frets   = list(PRICES["frets"].keys())
    colors  = list(PRICES["colors"].keys())

    selected = {
        "wood":   woods[0],
        "bridge": bridges[0],
        "frets":  frets[0],
        "color":  colors[0],
    }

    row_base   = ft.Text(f"База ({guitar['name']}):  {PRICES['guitars'][key]['base']} ₴", size=13)
    row_wood   = ft.Text("", size=13)
    row_bridge = ft.Text("", size=13)
    row_frets  = ft.Text("", size=13)
    row_color  = ft.Text("", size=13)
    row_total  = ft.Text("", weight=ft.FontWeight.BOLD, size=16, color=ft.Colors.YELLOW_ACCENT_400)

    def refresh_price():
        total, parts = calculate_price(
            key, selected["wood"], selected["bridge"], selected["frets"], selected["color"]
        )
        row_wood.value   = f"Деревина ({selected['wood']}):  +{parts['wood']} ₴"
        row_bridge.value = f"Бридж ({selected['bridge']}):  +{parts['bridge']} ₴"
        row_frets.value  = f"Лади ({selected['frets']}):  +{parts['frets']} ₴"
        row_color.value  = f"Колір ({selected['color']}):  +{parts['color']} ₴"
        row_total.value  = f"Разом: {total} ₴"
        page.update()  # ← оновлюємо page, не dialog

    def make_dd(label, options, field):
        dd = ft.Dropdown(
            label=label,
            value=options[0],
            options=[ft.dropdown.Option(o) for o in options],
            width=320,
        )
        def on_change(e):
            selected[field] = dd.value
            refresh_price()
        dd.on_change = on_change
        return dd

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
                make_dd("Деревина",        woods,   "wood"),
                make_dd("Бридж",           bridges, "bridge"),
                make_dd("Кількість ладів", frets,   "frets"),
                make_dd("Колір",           colors,  "color"),
                ft.Divider(height=20),
                ft.Column(
                    spacing=4,
                    controls=[row_base, row_wood, row_bridge, row_frets, row_color],
                ),
                ft.Divider(height=8),
                row_total,
            ],
        ),
        actions=[
            ft.TextButton("Скасувати", on_click=close),
            ft.FilledButton(
                "Підтвердити замовлення",
                style=ft.ButtonStyle(
                    bgcolor=ft.Colors.YELLOW_ACCENT_400,
                    color=ft.Colors.BLACK,
                ),
                on_click=close,
            ),
        ],
    )

    # повертаємо разом з refresh щоб викликати після додавання на сторінку
    return dialog, refresh_price


def guitar_card(guitar, page):
    async def open_buy(e):
        dialog, refresh = build_order_dialog(page, guitar)
        page.overlay.append(dialog)
        dialog.open = True
        page.update()
        refresh()  # ← тепер діалог вже на сторінці

    return ft.Container(
        width=260,
        border_radius=16,
        bgcolor=ft.Colors.GREY_900,
        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
        content=ft.Column(
            spacing=0,
            controls=[
                ft.Image(
                    src=guitar["src"],
                    width=260,
                    height=200,
                    fit=ft.BoxFit.COVER,
                ),
                ft.Container(
                    padding=ft.Padding(left=16, right=16, top=12, bottom=16),
                    content=ft.Column(
                        spacing=8,
                        controls=[
                            ft.Text(guitar["name"], style=text_STYLE),
                            ft.Text(
                                guitar["desc"],
                                size=12,
                                color=ft.Colors.GREY_400,
                            ),
                            ft.Row(
                                spacing=8,
                                controls=[
                                    ft.OutlinedButton(
                                        "Дізнатись",
                                        icon=ft.Icons.PLAY_CIRCLE_OUTLINE,
                                        url=guitar["youtube"],
                                        style=ft.ButtonStyle(
                                            color=ft.Colors.YELLOW_ACCENT_400,
                                            side=ft.BorderSide(1, ft.Colors.YELLOW_ACCENT_400),
                                        ),
                                    ),
                                    ft.FilledButton(
                                        "Купити",
                                        icon=ft.Icons.SHOPPING_CART,
                                        on_click=open_buy,
                                        style=ft.ButtonStyle(
                                            bgcolor=ft.Colors.YELLOW_ACCENT_400,
                                            color=ft.Colors.BLACK,
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
    async def go_home(e):
        await page.push_route("/home")

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
                title=ft.Text("Guitar Custom", color=ft.Colors.YELLOW_ACCENT_400),
                actions=[
                    ft.IconButton(
                        icon=ft.Icons.HOME,
                        tooltip="Головна",
                        icon_color=ft.Colors.YELLOW_ACCENT_400,
                        on_click=go_home,
                    ),
                    ft.IconButton(
                        icon=ft.Icons.SETTINGS,
                        icon_color=ft.Colors.YELLOW_ACCENT_400,
                        tooltip="Налаштування",
                        on_click=show_settings_dialog,
                    ),
                    ft.Container(width=12),
                ],
            ),
            ft.Container(
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
                                    color=ft.Colors.YELLOW_ACCENT_400),
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