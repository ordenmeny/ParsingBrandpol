import httpx
import logging

from app.exceptions import PageNotFoundException

logger = logging.getLogger(__name__)


async def get_page_by_search(
    client: httpx.AsyncClient,
    host_url: str,
    text_search: str,
) -> str | None:
    text_search = "+".join(text_search.split())

    url = f"{host_url}/catalog/?q={text_search}&s=Найти"

    logger.info(f"Requesting {url}")

    response = await client.get(url)

    if hasattr(response, "text"):
        return response.text

    raise PageNotFoundException()


async def get_card_page(client: httpx.AsyncClient, link: str) -> str | None:
    response = await client.get(link)
    response.raise_for_status()

    return response.text
