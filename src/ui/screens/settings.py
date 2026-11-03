import flet as ft

def build() -> ft.Control:
    return ft.Container(
        content=ft.Text("Настройки", size=30),
        alignment=ft.Alignment.CENTER,
    )