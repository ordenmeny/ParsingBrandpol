from urllib.parse import urljoin
from bs4 import BeautifulSoup
import logging
import re

logger = logging.getLogger(__name__)


def parse_page_with_cards(text_html: str, host_url: str) -> list[str]:
    soup = BeautifulSoup(text_html, "html.parser")

    links = [
        urljoin(host_url, tag["href"]) for tag in soup.select(".item-title a[href]")
    ]

    uniq_links = list(dict.fromkeys(links))

    return uniq_links


class ParseCard:
    def __init__(self, text_html: str):
        self.text_html = text_html
        self.soup = BeautifulSoup(text_html, "html.parser")

    def get_name(self, text_html: str | None = None) -> str:
        soup = BeautifulSoup(text_html, "html.parser") if text_html else self.soup
        title = soup.select_one("h1#pagetitle, h1")

        if title:
            return title.get_text(strip=True)

        title = soup.select_one("meta[itemprop='name']")
        return title.get("content", "").strip() if title else ""

    def price_with_discount(self) -> int | float:
        price = self.soup.select_one("[itemprop='offers'] meta[itemprop='price']")
        if price and price.get("content"):
            return int(float(price["content"]))

        price_tag = self.soup.select_one(".price .price_value, .price_value")
        if price_tag:
            price_text = re.sub(r"\D", "", price_tag.get_text())
            return int(price_text) if price_text else 0

        return 0

    def price_with_out_discount(self) -> int | float:
        old_price_tag = self.soup.select_one(
            ".price.discount .price_value, "
            ".price_old .price_value, "
            ".old_price .price_value, "
            ".price.discount, "
            ".price_old, "
            ".old_price"
        )
        if old_price_tag:
            old_price = re.sub(r"\D", "", old_price_tag.get_text())
            return int(old_price) if old_price else 0

        return self.price_with_discount()

    def articul(self) -> str:
        for item in self.soup.select(".js-prop-replace"):
            title = item.select_one(".js-prop-title")
            value = item.select_one(".js-prop-value")

            if title and value and title.get_text(strip=True) == "Артикул":
                return value.get_text(strip=True)

        return ""

    def manufacturer(self) -> str:
        for item in self.soup.select(".js-prop-replace"):
            title = item.select_one(".js-prop-title")
            value = item.select_one(".js-prop-value")

            if title and value and title.get_text(strip=True) == "Производитель":
                return value.get_text(strip=True)

        brand = self.soup.select_one("[itemprop='brand'] meta[itemprop='name']")
        return brand.get("content", "").split("(", 1)[0].strip() if brand else ""

    def is_available(self) -> bool:
        availability = self.soup.select_one(
            "[itemprop='offers'] [itemprop='availability']"
        )
        if availability and availability.get("href"):
            return availability["href"].endswith("/InStock")

        stock = self.soup.select_one(".item-stock .value, .item-stock")
        stock_text = stock.get_text(strip=True).lower() if stock else ""

        return "в наличии" in stock_text and "нет в наличии" not in stock_text
