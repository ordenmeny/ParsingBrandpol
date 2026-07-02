from dataclasses import dataclass


@dataclass
class CardScheme:
    """
    * Название товара
    * Цену со скидкой
    * Цену без скидки
    * Артикул
    * Производитель
    * Наличие
    * Ссылку на товар
    """

    name: str
    price_with_discount: float | int
    price_with_out_discount: float | int
    articul: str
    manufacturer: str
    is_available: bool
    link: str
