import httpx

from core.models import BookData

SEARCH_URL = "https://openlibrary.org/search.json"
COVER_URL = "https://covers.openlibrary.org/b/id/{cover_id}-M.jpg"
TIMEOUT = 10.0

# Open Library просит представляться в User-Agent (с ним лимит 3 запроса в секунду)
# Подставь свою настоящую почту
HEADERS = {"User-Agent": "MyBookcase/0.1 (your_email@example.com)"}

# editions.* возвращают данные лучшего издания под запрос и язык пользователя
FIELDS = (
    "key,title,author_name,first_publish_year,number_of_pages_median,cover_i,"
    "editions,editions.key,editions.title,editions.language"
)

# Open Library отдаёт трёхбуквенные коды, в базе удобнее двухбуквенные
LANG_CODES = {
    "rus": "ru", "eng": "en", "ukr": "uk", "deu": "de", "ger": "de",
    "fre": "fr", "spa": "es",
}
# и обратно: для фильтра language:rus в запросе
TO_OL_CODE = {
    "ru": "rus", "en": "eng", "uk": "ukr", "de": "ger", "fr": "fre", "es": "spa",
}


class BooksApiError(Exception):
    """Ошибка поиска. Текст можно показывать пользователю."""


async def search_books(query: str, *, limit: int = 20, page: int = 1, lang: str | None = None, strict: bool = False) -> list[BookData]:
    """Ищет книги в Open Library.

    lang   - язык пользователя ("ru"): поднимает издания на этом языке выше.
    strict - если True, показываются только книги с изданием на языке lang.
    page   - номер страницы, нумерация с 1.
    """
    query = query.strip()
    if not query:
        return []

    q = query
    if lang and strict:
        q += f" language:{TO_OL_CODE.get(lang, lang)}"

    params = {"q": q, "limit": limit, "page": page, "fields": FIELDS}
    if lang:
        params["lang"] = lang

    try:
        async with httpx.AsyncClient(timeout=TIMEOUT, headers=HEADERS) as client:
            response = await client.get(SEARCH_URL, params=params)
            response.raise_for_status()
    except httpx.TimeoutException as e:
        raise BooksApiError("Сервер не отвечает, попробуйте позже") from e
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 429:
            raise BooksApiError("Слишком много запросов, подождите секунду") from e
        raise BooksApiError(f"Ошибка сервера ({e.response.status_code})") from e
    except httpx.HTTPError as e:
        raise BooksApiError("Нет соединения с интернетом") from e

    docs = response.json().get("docs", [])
    books = (_parse_doc(doc) for doc in docs)
    return [b for b in books if b is not None]


def _parse_doc(doc: dict) -> BookData | None:
    # лучшее издание под запрос; если его нет, берём данные произведения
    editions = doc.get("editions", {}).get("docs") or [{}]
    edition = editions[0]

    title = edition.get("title") or doc.get("title")
    if not title:
        return None

    return BookData(
        title=title,
        authors=doc.get("author_name", []),
        page_count=doc.get("number_of_pages_median") or None,
        language=_parse_language(edition.get("language")),
        published_year=doc.get("first_publish_year"),
        cover_url=_parse_cover(doc.get("cover_i")),
        source="open_library",
        external_id=doc.get("key"),  # ключ произведения, по нему потом берём описание
    )


def _parse_language(codes: list[str] | None) -> str | None:
    if not codes:
        return None
    return LANG_CODES.get(codes[0], codes[0])


def _parse_cover(cover_id: int | None) -> str | None:
    if not cover_id:
        return None
    return COVER_URL.format(cover_id=cover_id)