import asyncio

import httpx

from app.card_scheme import CardScheme
from app.writers import CardWriter
from app.html_getters import get_page_by_search, get_card_page
from app.parse_html import parse_page_with_cards, ParseCard

MAX_CONCURRENT_REQUESTS = 5


async def parse_card(
    client: httpx.AsyncClient,
    semaphore: asyncio.Semaphore,
    link: str,
) -> CardScheme:
    async with semaphore:
        page = await get_card_page(client, link)

    card = ParseCard(page)

    return CardScheme(
        name=card.get_name(),
        price_with_discount=card.price_with_discount(),
        price_with_out_discount=card.price_with_out_discount(),
        articul=card.articul(),
        manufacturer=card.manufacturer(),
        is_available=card.is_available(),
        link=link,
    )


async def collect_cards(
    client: httpx.AsyncClient,
    links_of_cards: list[str],
) -> list[CardScheme]:
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)
    tasks = [parse_card(client, semaphore, link) for link in links_of_cards]
    return await asyncio.gather(*tasks)


async def parse_cards_by_search(
    host_url: str,
    text_search: str,
    writer: CardWriter,
):
    async with httpx.AsyncClient() as client:
        main_page = await get_page_by_search(client, host_url, text_search)

        links_of_cards = parse_page_with_cards(
            text_html=main_page,
            host_url=host_url,
        )

        cards = await collect_cards(client, links_of_cards)

    writer.save(cards)


async def parse_cards_by_links(links_of_cards: list[str], writer: CardWriter):
    async with httpx.AsyncClient() as client:
        cards = await collect_cards(client, links_of_cards)

    writer.save(cards)
