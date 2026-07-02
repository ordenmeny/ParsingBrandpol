import asyncio
import logging

from app.run_parsing import parse_cards_by_links, parse_cards_by_search
from app.writers import WriteToCsv

logger = logging.getLogger(__name__)
HOST_URL = "https://magbo.ru"


def split_user_values(user_input: str) -> list[str]:
    return [value.strip() for value in user_input.split(",") if value.strip()]


async def run_search_scenario() -> None:
    user_input = input("Введите поисковые запросы через запятую без кавычек: ")
    text_search = split_user_values(user_input)

    for search_query in text_search:
        writer = WriteToCsv(filename=search_query)
        await parse_cards_by_search(HOST_URL, search_query, writer)


async def run_links_scenario() -> None:
    user_input = input("Введите ссылки на карточки через запятую: ")
    links = split_user_values(user_input)

    filename = input("Введите имя CSV файла: ").strip() or "cards"
    writer = WriteToCsv(filename=filename)
    await parse_cards_by_links(links, writer)


async def main() -> None:
    print("Выберите режим работы:")
    print("1) Через поиск")
    print("2) По ссылкам")

    mode = input("Введите 1 или 2: ").strip()

    if mode == "1":
        await run_search_scenario()
    elif mode == "2":
        await run_links_scenario()
    else:
        print("Неизвестный режим")


if __name__ == "__main__":
    asyncio.run(main())
