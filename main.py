import asyncio
import logging

from app.run_parsing import parse_cards_by_search
from app.writers import WriteToCsv

logger = logging.getLogger(__name__)


async def main() -> None:
    host_url = "https://magbo.ru"
    text_search = "Биде Sole"
    writer = WriteToCsv(filename=text_search)
    await parse_cards_by_search(host_url, text_search, writer)


if __name__ == "__main__":
    asyncio.run(main())
