import flet as ft

def build() -> ft.Control:
    return ft.Container(
        content=ft.Text("Коллекции", size=30),
        alignment=ft.Alignment.CENTER,
    )