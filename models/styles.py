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
    bgcolor="#111111",
    border_color="#FFD700",
    focused_border_color="#FFEA00",
    color="#FFD700",
    cursor_color="#FFEA00",
    border_radius=5,
    label_style=ft.TextStyle(color="#FFC200"),
)

text_STYLE = dict(
    weight=ft.FontWeight.BOLD,
    color="#FFD700",
    font_family='Text'

)

error_text_STYLE = dict(
    size=12,
    weight=ft.FontWeight.W_900,
    color="#FF6F00",
    font_family='Text'
)

icon_button_STYLE = ft.ButtonStyle(
    color={
        ft.ControlState.HOVERED: "#FFEA00",
        ft.ControlState.DEFAULT: "#FFD700",
    },
)

appbar_STYLE = dict(
    bgcolor=ft.Colors.with_opacity(0.85, "#1A1200"),
    center_title=True,
    elevation=12,
    shadow_color="#FFD700",
)

bottom_appbar_STYLE = dict(
    bgcolor=ft.Colors.with_opacity(0.92, "#0D0D00"),
    height=120,
    padding=ft.Padding(left=48, right=48, top=16, bottom=12),
)


SOFT_BG_GRADIENT = ft.Container(
    expand=True,
    gradient=ft.LinearGradient(
        begin=ft.Alignment.TOP_CENTER,
        end=ft.Alignment.BOTTOM_CENTER,
        colors=[
            "#000000",
            "#0D0D00",  
            "#1A1A00", 
            "#2E2A00",  
            "#0D0D00", 
            "#000000",  
        ],
        stops=[0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
    ),
)