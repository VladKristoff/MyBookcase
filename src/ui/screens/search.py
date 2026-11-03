import flet as ft
from services.books_api import search_books

class SearchScreen:

    def build(self) -> ft.Control:
            title_label = ft.Text("Введите название книги", size=50)
    
            self.book_entry = ft.TextField(label="Название", hint_text="Мартин Иден")
    
            search_btn = ft.Button(content="Поиск", on_click=self.search_book)

            return ft.Container(
                content=ft.Column(
                      controls=[title_label, self.book_entry, search_btn],
                      alignment=ft.MainAxisAlignment.CENTER,
                      horizontal_alignment=ft.CrossAxisAlignment.CENTER
                 ),
                 alignment=ft.Alignment.CENTER
            )
    
    async def search_book(self, e):
        name = self.book_entry.value

        result = await search_books(query=name)
        print(result)

        

search_screen = SearchScreen

