import flet as ft

def build() -> ft.Control:
    return ft.Container(
        content=ft.Text("Полки", size=30),
        alignment=ft.Alignment.CENTER,
    )