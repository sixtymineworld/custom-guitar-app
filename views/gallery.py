import flet as ft
from models.styles import *


GUITARS = [
    {
        "name": "Stratocaster",
        "src": "Stratocaster.jpg",
        "desc": "Створена Fender у 1954. Три звукознімачі, контурний корпус, улюблениця блюзу та рок-н-ролу.",
    },
    {
        "name": "Les Paul",
        "src": "Les-Paul.jpg",
        "desc": "Gibson, 1952. Масивний корпус з махагону, два хамбакери — потужний, теплий звук.",
    },
    {
        "name": "SG",
        "src": "SG.jpg",
        "desc": "Gibson, 1961. Тонкий корпус, гострі ріжки — агресивний вигляд і легкий доступ до верхніх ладів.",
    },
    {
        "name": "Telecaster",
        "src": "Telecaster.jpg",
        "desc": "Fender, 1950. Перша масова електрогітара. Різкий звук, простота, надійність.",
    },
    {
        "name": "Explorer",
        "src": "Explorer.jpg",
        "desc": "Gibson, 1958. Футуристична форма, потужний звук — обрана хард-рок та метал музикантами.",
    },
    {
        "name": "Flying V",
        "src": "Flying-V.jpg",
        "desc": "Gibson, 1958. V-подібний корпус став символом хард-року та важкого металу.",
    },
    {
        "name": "Jazzmaster",
        "src": "Jazzmaster.jpg",
        "desc": "Fender, 1958. Великий корпус, м'який звук — популярна в джазі та альтернативному році.",
    },
    {
        "name": "Baritone",
        "src": "Baritone.jpg",
        "desc": "Довший мензурний, нижчий стрій — улюблениця метал та саундтрек-композиторів.",
    },
    {
        "name": "Superstrat",
        "src": "Superstrat.jpg",
        "desc": "80-ті роки. Strat-форма з хамбакером на бриджі — створена для швидкої гри та хай-гейну.",
    },
    {
        "name": "V-Shape (Dean)",
        "src": "V-Shape-(Dean).jpg",
        "desc": "Dean, 1977. Екстремальна V-форма, фірмовий знак металу та шред-гітаристів.",
    },
]


def guitar_card(guitar):
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
                        spacing=6,
                        controls=[
                            ft.Text(
                                guitar["name"],
                                style=text_STYLE),
                            ft.Text(
                                guitar["desc"],
                                size=12,
                                color=ft.Colors.GREY_400,
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

    cards = ft.Row(
        wrap=True,
        spacing=20,
        run_spacing=20,
        controls=[guitar_card(g) for g in GUITARS],
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
                        on_click=show_settings_dialog),
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
                        ft.Text(
                            "Форми гітар",
                            size=28,
                            weight=ft.FontWeight.BOLD,
                        ),
                        ft.Text(
                            "Обери форму та дізнайся її історію",
                            size=14,
                        ),
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
                            ft.Text("Guitar Custom", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.YELLOW_ACCENT_400),
                            ft.Row(
                                controls=[
                                    ft.TextButton("Головна",
                                                  style=ft.ButtonStyle(color=ft.Colors.WHITE),
                                                  on_click=go_hero),
                                    ft.TextButton("Каталог",
                                                  style=ft.ButtonStyle(color=ft.Colors.WHITE)),
                                    ft.TextButton("Замовлення",
                                                  style=ft.ButtonStyle(color=ft.Colors.WHITE)),
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