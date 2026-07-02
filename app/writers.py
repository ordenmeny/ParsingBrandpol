import csv
from abc import ABC, abstractmethod
from dataclasses import asdict
from pathlib import Path

from app.card_scheme import CardScheme


class CardWriter(ABC):
    @abstractmethod
    def save(self, cards: list[CardScheme]) -> None:
        pass


class WriteToCsv(CardWriter):
    def __init__(self, filename: str) -> None:
        self.filename = Path(filename)
        if not self.filename.suffix:
            self.filename = self.filename.with_suffix(".csv")

    def save(self, cards: list[CardScheme]) -> None:
        if not cards:
            return

        fieldnames = list(asdict(cards[0]).keys())

        with open(self.filename, "w", encoding="utf-8-sig", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

            for card in cards:
                writer.writerow(asdict(card))
