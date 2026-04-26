"""Gaming & Entertainment Data Provider."""

from __future__ import annotations
from typing import Any
from synthgen.core.base import BaseProvider
from synthgen.core.seed_manager import SeedManager


RACES = ["Human", "Elf", "Dwarf", "Orc", "Halfling", "Dragonborn", "Tiefling", "Gnome"]
CLASSES = ["Warrior", "Mage", "Rogue", "Cleric", "Ranger", "Paladin", "Barbarian", "Bard", "Druid", "Monk"]
RARITIES = ["Common", "Uncommon", "Rare", "Epic", "Legendary", "Mythic"]
ITEM_TYPES = ["Weapon", "Armor", "Potion", "Ring", "Amulet", "Scroll", "Gem", "Material"]


class GamingProvider(BaseProvider):
    """Provider for gaming and entertainment data."""

    def __init__(self, seed_manager: SeedManager | None = None) -> None:
        super().__init__(seed_manager)
        self._sm = seed_manager

    def _get_sm(self) -> SeedManager:
        if self._sm is None:
            raise RuntimeError("SeedManager not initialized")
        return self._sm

    def dice_roll(self, sides: int = 6, count: int = 1) -> list[int]:
        """Roll dice."""
        sm = self._get_sm()
        return [sm.random_int(1, sides) for _ in range(count)]

    def card_draw(self, deck_count: int = 1) -> list[str]:
        """Draw cards from a standard deck."""
        sm = self._get_sm()
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        deck = [f"{rank} of {suit}" for suit in suits for rank in ranks]
        return sm.random_sample(deck, min(deck_count, len(deck)))

    def npc_stats(self) -> dict[str, Any]:
        """Generate NPC stats."""
        sm = self._get_sm()
        return {
            "strength": sm.random_int(1, 20),
            "dexterity": sm.random_int(1, 20),
            "constitution": sm.random_int(1, 20),
            "intelligence": sm.random_int(1, 20),
            "wisdom": sm.random_int(1, 20),
            "charisma": sm.random_int(1, 20),
        }

    def character(self) -> dict[str, Any]:
        """Generate a game character."""
        sm = self._get_sm()
        name_parts = ["Shadow", "Storm", "Iron", "Fire", "Frost", "Swift", "Mighty", "Dark"]
        suffixes = ["walker", "blade", "heart", "forge", "wind", "strike", "bane", "guard"]
        name = sm.random_choice(name_parts) + sm.random_choice(suffixes)
        
        return {
            "name": name,
            "race": sm.random_choice(RACES),
            "class": sm.random_choice(CLASSES),
            "level": sm.random_int(1, 50),
            "stats": self.npc_stats(),
            "gold": sm.random_int(0, 10000),
        }

    def loot_item(self) -> dict[str, Any]:
        """Generate a loot item."""
        sm = self._get_sm()
        prefixes = ["Rusty", "Polished", "Enchanted", "Cursed", "Ancient", "Glowing"]
        name = sm.random_choice(prefixes) + " " + sm.random_choice(ITEM_TYPES).lower()
        
        rarity_weights = [50, 30, 15, 4, 0.9, 0.1]
        rarity = sm.random_choice(RARITIES)  # Simplified
        
        return {
            "name": name,
            "type": sm.random_choice(ITEM_TYPES),
            "rarity": rarity,
            "value": sm.random_int(1, 1000) * (RARITIES.index(rarity) + 1),
            "magical": sm.random_bool(0.3),
        }

    def generate(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        """Generate complete gaming profile."""
        return {
            "dice_roll": self.dice_roll(sides=20, count=3),
            "cards": self.card_draw(5),
            "character": self.character(),
            "loot": self.loot_item(),
        }
