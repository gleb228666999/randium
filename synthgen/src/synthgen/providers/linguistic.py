"""
Linguistic & Content Data Provider.

Generates linguistic content including:
- Words and sentences
- Paragraphs
- Product/book/company names
- Reviews
- Tags
- SEO metadata
"""

from __future__ import annotations

from typing import Any

from synthgen.core.base import BaseProvider
from synthgen.core.seed_manager import SeedManager


LOREM_WORDS = [
    "lorem", "ipsum", "dolor", "sit", "amet", "consectetur", "adipiscing", "elit",
    "sed", "do", "eiusmod", "tempor", "incididunt", "ut", "labore", "et", "dolore",
    "magna", "aliqua", "enim", "ad", "minim", "veniam", "quis", "nostrud",
    "exercitation", "ullamco", "laboris", "nisi", "aliquip", "ex", "ea", "commodo",
    "consequat", "duis", "aute", "irure", "in", "reprehenderit", "voluptate",
    "velit", "esse", "cillum", "fugiat", "nulla", "pariatur", "excepteur", "sint",
    "occaecat", "cupidatat", "non", "proident", "sunt", "culpa", "qui", "officia",
    "deserunt", "mollit", "anim", "id", "est", "laborum"
]

PRODUCT_ADJECTIVES = [
    "Premium", "Smart", "Ultra", "Pro", "Max", "Mini", "Lite", "Plus",
    "Advanced", "Classic", "Modern", "Eco", "Digital", "Wireless", "Portable"
]

PRODUCT_NOUNS = [
    "Widget", "Gadget", "Device", "Tool", "System", "Hub", "Station", "Kit",
    "Pack", "Set", "Bundle", "Box", "Mate", "Pod", "Stick", "Cam", "Watch"
]

BOOK_GENRES = [
    "Fiction", "Mystery", "Thriller", "Romance", "Sci-Fi", "Fantasy",
    "Biography", "History", "Self-Help", "Business", "Science", "Technology"
]

REVIEW_TEMPLATES = [
    "This {product} is absolutely {positive}! I would {recommend} it to anyone.",
    "Great value for the price. The {feature} works {positive}.",
    "I've been using this for {time} now and it's been {positive}.",
    "Not bad, but could be better. The {feature} is just okay.",
    "Exceeded my expectations! The {feature} is {positive}.",
]

POSITIVE_WORDS = ["amazing", "fantastic", "excellent", "great", "wonderful", "superb", "outstanding"]
NEGATIVE_WORDS = ["disappointing", "terrible", "awful", "poor", "bad", "mediocre", "subpar"]


class LinguisticProvider(BaseProvider):
    """Provider for linguistic and content data."""

    def __init__(self, seed_manager: SeedManager | None = None) -> None:
        super().__init__(seed_manager)
        self._sm = seed_manager

    def _get_sm(self) -> SeedManager:
        if self._sm is None:
            raise RuntimeError("SeedManager not initialized")
        return self._sm

    def word(self) -> str:
        """Generate a random word."""
        sm = self._get_sm()
        return sm.random_choice(LOREM_WORDS)

    def sentence(self, word_count: int = 10) -> str:
        """Generate a random sentence."""
        sm = self._get_sm()
        words = [self.word() for _ in range(word_count)]
        sentence = " ".join(words)
        return sentence.capitalize() + "."

    def paragraph(self, sentence_count: int = 3) -> str:
        """Generate a random paragraph."""
        sm = self._get_sm()
        sentences = [self_sentence(sm.random_int(8, 15)) for _ in range(sentence_count)]
        return " ".join(sentences)

    def product_name(self) -> str:
        """Generate a product name."""
        sm = self._get_sm()
        adj = sm.random_choice(PRODUCT_ADJECTIVES)
        noun = sm.random_choice(PRODUCT_NOUNS)
        model = f"{sm.random_int(100, 999)}"
        return f"{adj} {noun} {model}"

    def book_title(self) -> str:
        """Generate a book title."""
        sm = self._get_sm()
        templates = [
            "The {adj} {noun}",
            "{noun} of {place}",
            "How to {verb}",
            "A {adj} Journey",
        ]
        template = sm.random_choice(templates)
        return template.format(
            adj=self.word().capitalize(),
            noun=self.word().capitalize(),
            place=sm.random_choice(["Time", "Dreams", "Shadows", "Light"]),
            verb=sm.random_choice(["Learn", "Master", "Understand", "Achieve"]),
        )

    def review(self, product_name: str | None = None, rating: int | None = None) -> dict[str, Any]:
        """Generate a product review."""
        sm = self._get_sm()
        product = product_name or self.product_name()
        rating = rating or sm.random_int(1, 5)
        
        positive = sm.random_choice(POSITIVE_WORDS)
        feature = sm.random_choice(["quality", "design", "performance", "battery life", "interface"])
        recommend = sm.random_choice(["definitely recommend", "highly recommend", "recommend"])
        time_period = sm.random_choice(["a week", "a month", "several months", "over a year"])
        
        template = sm.random_choice(REVIEW_TEMPLATES)
        text = template.format(
            product=product,
            positive=positive if rating >= 4 else sm.random_choice(NEGATIVE_WORDS),
            recommend=recommend if rating >= 4 else "think twice before buying",
            feature=feature,
            time=time_period,
        )
        
        return {
            "product": product,
            "rating": rating,
            "title": f"{'Great' if rating >= 4 else 'Mixed'} experience with {product}",
            "text": text,
            "verified_purchase": sm.random_bool(0.8),
        }

    def tags(self, count: int = 5) -> list[str]:
        """Generate random tags."""
        sm = self._get_sm()
        tag_words = ["tech", "news", "tutorial", "guide", "tips", "review", "analysis", "update"]
        return [sm.random_choice(tag_words) for _ in range(count)]

    def seo_metadata(self) -> dict[str, str]:
        """Generate SEO metadata."""
        sm = self._get_sm()
        keywords = ", ".join(self.tags(sm.random_int(5, 10)))
        description = self.sentence(sm.random_int(15, 25))
        return {
            "title": f"{self.word().capitalize()} - {self.word().capitalize()} Solutions",
            "description": description,
            "keywords": keywords,
            "og_title": f"Discover {self.word().capitalize()} Today",
            "og_description": description[:100] + "...",
        }

    def generate(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        """Generate complete linguistic profile."""
        return {
            "word": self.word(),
            "sentence": self.sentence(),
            "paragraph": self.paragraph(),
            "product_name": self.product_name(),
            "book_title": self.book_title(),
            "review": self.review(),
            "tags": self.tags(),
            "seo": self.seo_metadata(),
        }


def _sentence(sm: SeedManager, word_count: int = 10) -> str:
    """Helper to generate sentence with provided seed manager."""
    words = [sm.random_choice(LOREM_WORDS) for _ in range(word_count)]
    sentence = " ".join(words)
    return sentence.capitalize() + "."
