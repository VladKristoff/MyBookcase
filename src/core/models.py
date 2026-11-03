from dataclasses import dataclass, field


@dataclass
class BookData:
    title: str
    authors: list[str] = field(default_factory=list)
    description: str | None = None
    page_count: int | None = None
    language: str | None = None
    published_year: int | None = None
    cover_url: str | None = None
    source: str = "open_library"
    external_id: str | None = None