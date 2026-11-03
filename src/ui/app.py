import flet as ft

from ui.screens import search, collections, shelf, settings
from ui.screens.search import SearchScreen

search_screen = SearchScreen()

TABS = [
    (ft.Icons.SEARCH, "Поиск", search_screen.build),
    (ft.Icons.COLLECTIONS_BOOKMARK, "Коллекции", collections.build),
    (ft.Icons.LIBRARY_BOOKS, "Полки", shelf.build),
    (ft.Icons.SETTINGS, "Настройки", settings.build),
]

def build_app(page: ft.Page) -> None:

    body = ft.Container(content=TABS[0][2](), expand=True)

    def on_nav_change(e):
        index = e.control.selected_index
        body.content = TABS[index][2]()

    page.navigation_bar = ft.NavigationBar(
        selected_index=0,
        on_change=on_nav_change,
        destinations=[
            ft.NavigationBarDestination(icon=icon, label=label)
            for icon, label, _ in TABS
        ],
    )

    page.add(ft.SafeArea(expand=True, content=body))