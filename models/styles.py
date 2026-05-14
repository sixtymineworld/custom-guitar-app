import flet as ft 

btn_style = ft.ButtonStyle(
    bgcolor={
        ft.ControlState.HOVERED: ft.Colors.YELLOW_ACCENT_100,
        ft.ControlState.DEFAULT: ft.Colors.YELLOW_ACCENT_700,
        },
    color=ft.Colors.BLACK,
    padding=12,
    shape=ft.RoundedRectangleBorder(radius=8),
)

button_STYLE = ft.ButtonStyle(
    bgcolor=ft.Colors.BLACK,
    color=ft.Colors.YELLOW_ACCENT_400,
    padding=12,
    side=ft.BorderSide(2, ft.Colors.YELLOW_ACCENT_700),
)

textfield_STYLE = dict(
    bgcolor=ft.Colors.GREY_900,
    border_color=ft.Colors.YELLOW_700,
    focused_border_color=ft.Colors.YELLOW_ACCENT_400,
    color=ft.Colors.WHITE,
    cursor_color=ft.Colors.YELLOW_ACCENT_400,
    border_radius=5,
    label_style=ft.TextStyle(color=ft.Colors.YELLOW),
)

text_STYLE = dict(
    weight=ft.FontWeight.BOLD,
    color=ft.Colors.YELLOW_700,
    font_family='Segoe UI',
)

error_text_STYLE = dict(
    size=12,
    weight=ft.FontWeight.W_900,
    color=ft.Colors.ORANGE_ACCENT_400,
    font_family='Consolas',
)
dropdown_STYLE = dict(
    bgcolor=ft.Colors.GREY_900,
    border_color=ft.Colors.YELLOW_700,
    focused_border_color=ft.Colors.YELLOW_ACCENT_400,
    color=ft.Colors.WHITE,
    border_radius=5,
    label_style=ft.TextStyle(color=ft.Colors.YELLOW),
    text_style=ft.TextStyle(color=ft.Colors.WHITE),
)

appbar_STYLE = dict(
    bgcolor=ft.Colors.GREY_900,
    center_title=True,
    elevation=4,
)
icon_button_STYLE = ft.ButtonStyle(
    color={
        ft.ControlState.HOVERED: ft.Colors.YELLOW_ACCENT_400,
        ft.ControlState.DEFAULT: ft.Colors.YELLOW_700,
    },
)

bottom_appbar_STYLE = dict(
    bgcolor=ft.Colors.GREY_900,
    height=70,
    padding=10,
)

COLOR_BLACK = "#000000"
COLOR_YELLOW = "#FFD700"