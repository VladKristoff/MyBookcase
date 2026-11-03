import flet as ft

from core.db import init_db
from ui.app import build_app
from services.books_api import search_books

def main(page: ft.Page):
    init_db()
    build_app(page)

ft.run(main)