import flet as ft
from views import login_view, home_view, register_view, orders_view, hero_view, gallery_view

async def main(page: ft.Page):
    pref = ft.SharedPreferences()
    saved_theme = await pref.get("theme")
    page.theme_mode = ft.ThemeMode.DARK if saved_theme == "dark" else ft.ThemeMode.LIGHT

    async def route_change(e):
        current_route = e.route if hasattr(e, "route") else e
        page.views.clear()

        is_auth = page.session.store.get("authenticated")

        if not is_auth and current_route not in ("/", "/login", "/register"):
            await page.push_route("/login")
            return

        if current_route == "/":
            page.views.append(hero_view(page))
        elif current_route == "/login":
            page.views.append(login_view(page))
        elif current_route == "/register":
            page.views.append(register_view(page))
        elif current_route == "/home":
            page.views.append(home_view(page))
        elif current_route == "/gallery":
            page.views.append(gallery_view(page))
        elif current_route == "/orders":
            page.views.append(orders_view(page))
        else:
            page.views.append(login_view(page))

        page.update()

    async def view_pop(e: ft.ViewPopEvent):
        if len(page.views) > 1:
            page.views.pop()
            top_view = page.views[-1]
            await page.push_route(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    initial_route = page.route if page.route else "/"
    await route_change(initial_route)

ft.run(main, assets_dir="assets", view=ft.AppView.WEB_BROWSER)