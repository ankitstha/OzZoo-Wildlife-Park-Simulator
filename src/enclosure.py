"""Enclosure and Food inventory classes."""

from abc import ABC, abstractmethod
from exception import EnclosureFullError, IncompatibleSpeciesError, InsufficientFoodError


# ---------------------------------------------------------------------------
# ICleanable interface (ABC with only abstract methods)
# ---------------------------------------------------------------------------

class ICleanable(ABC):
    """Interface contract: any class that can be cleaned."""

    @abstractmethod
    def clean(self) -> None:
        """Clean the object, restoring cleanliness to 100."""
        pass

    @abstractmethod
    def get_cleanliness(self) -> float:
        """Return current cleanliness level (0–100)."""
        pass


# ---------------------------------------------------------------------------
# Enclosure
# ---------------------------------------------------------------------------

class Enclosure(ICleanable):
    """Represents a zoo enclosure that houses animals of one species type."""

    def __init__(self, name: str, habitat_type: str, capacity: int):
        """
        Args:
            name: display name of the enclosure
            habitat_type: e.g. 'forest', 'grassland', 'wetland', 'aviary'
            capacity: maximum number of animals
        """
        self._name = name
        self._habitat_type = habitat_type
        self._capacity = capacity
        self._animals: list = []
        self._cleanliness: float = 100.0
        self._allowed_species: str | None = None  # set on first animal added

    @property
    def name(self): return self._name

    @property
    def animals(self): return list(self._animals)

    @property
    def is_full(self): return len(self._animals) >= self._capacity

    def add_animal(self, animal) -> None:
        if self.is_full:
            raise EnclosureFullError(self._name)

        # ✅ NEW: habitat check
        if animal.HABITAT_TYPE != self._habitat_type:
            raise IncompatibleSpeciesError(
                animal.species, self._habitat_type
            )

        # existing species rule
        if self._allowed_species and animal.species != self._allowed_species:
            raise IncompatibleSpeciesError(animal.species, self._allowed_species)

        if not self._allowed_species:
            self._allowed_species = animal.species

        self._animals.append(animal)

    def remove_dead_animals(self) -> list:
        """Remove and return any dead animals."""
        dead = [a for a in self._animals if not a.alive]
        self._animals = [a for a in self._animals if a.alive]
        return dead

    def daily_update(self) -> None:
        """Decrease cleanliness each day based on animal count."""
        self._cleanliness = max(0.0, self._cleanliness - (5.0 * len(self._animals)))

    def clean(self) -> None:
        self._cleanliness = 100.0

    def get_cleanliness(self) -> float:
        return self._cleanliness

    def visitor_appeal(self) -> float:
        """Return a 0–100 score representing how appealing this enclosure is."""
        if not self._animals:
            return 0.0
        avg_health = sum(a.health for a in self._animals) / len(self._animals)
        return (avg_health * 0.6) + (self._cleanliness * 0.4)

    def __str__(self):
        return (f"[{self._name}] {len(self._animals)}/{self._capacity} animals | "
                f"Cleanliness: {self._cleanliness:.0f}%")


# ---------------------------------------------------------------------------
# Food inventory
# ---------------------------------------------------------------------------

class FoodInventory:
    """Manages stock of all food types required by the zoo's animals."""

    def __init__(self):
        self._stock: dict[str, float] = {
            "eucalyptus": 50.0,
            "grass": 50.0,
            "roots": 50.0,
            "shrimp": 30.0,
            "seeds": 50.0,
            "meat": 30.0,
        }
        # Cost per unit for purchasing
        self._prices: dict[str, float] = {
            "eucalyptus": 5.0,
            "grass": 2.0,
            "roots": 2.0,
            "shrimp": 8.0,
            "seeds": 3.0,
            "meat": 10.0,
        }

    def restock(self, food_type: str, amount: float) -> float:
        """
        Add food to inventory and return the total cost.

        Raises:
            KeyError: if food_type is unknown
        """
        if food_type not in self._stock:
            raise KeyError(f"Unknown food type: '{food_type}'")
        cost = self._prices[food_type] * amount
        self._stock[food_type] += amount
        return cost

    def consume(self, food_type: str, amount: float = 1.0) -> None:
        """
        Deduct food from inventory.

        Raises:
            InsufficientFoodError: if stock is too low
        """
        if self._stock.get(food_type, 0) < amount:
            raise InsufficientFoodError(food_type)
        self._stock[food_type] -= amount

    def get_stock(self, food_type: str) -> float:
        return self._stock.get(food_type, 0.0)

    def status(self) -> dict:
        return dict(self._stock)