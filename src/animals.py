"""Animal hierarchy: ABC → Mammal/Bird → concrete species."""

from abc import ABC, abstractmethod


class Animal(ABC):
    """Abstract base class for all zoo animals."""

    HABITAT_TYPE: str = "generic"   # overridden by each species

    def __init__(self, name: str, species: str, age: int):
        self._name = name
        self._species = species
        self._age = age
        self._health: float = 100.0      # 0–100
        self._hunger: float = 0.0        # 0–100 (100 = starving)
        self._happiness: float = 80.0    # 0–100
        self._alive: bool = True

    # --- Properties ---
    @property
    def name(self): return self._name

    @property
    def species(self): return self._species

    @property
    def health(self): return self._health

    @property
    def hunger(self): return self._hunger

    @property
    def happiness(self): return self._happiness

    @property
    def alive(self): return self._alive

    # --- Abstract methods ---
    @abstractmethod
    def make_sound(self) -> str:
        """Return the animal's characteristic sound."""
        pass

    @abstractmethod
    def eat(self, food_type: str) -> None:
        """Consume food and reduce hunger."""
        pass

    @abstractmethod
    def preferred_food(self) -> str:
        """Return the food type this animal requires."""
        pass

    # --- Concrete shared behaviour ---
    def daily_update(self) -> None:
        """Called each game day: increases hunger, updates health and happiness."""
        self._hunger = min(100.0, self._hunger + 15.0)
        if self._hunger > 70:
            self._health = max(0.0, self._health - 10.0)
            self._happiness = max(0.0, self._happiness - 10.0)
        if self._health <= 0:
            self._alive = False

    def can_breed(self) -> bool:
        """Return True if the animal is healthy and happy enough to breed."""
        return self._health >= 70 and self._happiness >= 70 and self._alive

    def __str__(self):
        status = "✓" if self._alive else "✗"
        return (f"[{status}] {self._name} ({self._species}) | "
                f"HP:{self._health:.0f} Hunger:{self._hunger:.0f} 😊:{self._happiness:.0f}")


# ---------------------------------------------------------------------------
# Mid-level classes
# ---------------------------------------------------------------------------

class Mammal(Animal):
    """Shared behaviour for all mammal species."""

    def __init__(self, name: str, species: str, age: int, is_marsupial: bool = False):
        super().__init__(name, species, age)
        self._is_marsupial = is_marsupial

    def eat(self, food_type: str) -> None:
        """Eat preferred food for full relief, or any food for partial relief."""
        if food_type == self.preferred_food():
            self._hunger = max(0.0, self._hunger - 40.0)
            self._happiness = min(100.0, self._happiness + 5.0)
        else:
            self._hunger = max(0.0, self._hunger - 15.0)


class Bird(Animal):
    """Shared behaviour for all bird species."""

    def __init__(self, name: str, species: str, age: int, can_fly: bool = True):
        super().__init__(name, species, age)
        self._can_fly = can_fly

    def eat(self, food_type: str) -> None:
        """Eat preferred food for full relief, or any food for partial relief."""
        if food_type == self.preferred_food():
            self._hunger = max(0.0, self._hunger - 35.0)
            self._happiness = min(100.0, self._happiness + 5.0)
        else:
            self._hunger = max(0.0, self._hunger - 10.0)


# ---------------------------------------------------------------------------
# Concrete species — each declares its own HABITAT_TYPE
# ---------------------------------------------------------------------------

class Koala(Mammal):
    HABITAT_TYPE = "forest"

    def __init__(self, name: str, age: int = 2):
        super().__init__(name, "Koala", age, is_marsupial=True)

    def make_sound(self) -> str:
        return "*low bellow*"

    def preferred_food(self) -> str:
        return "eucalyptus"


class Kangaroo(Mammal):
    HABITAT_TYPE = "grassland"

    def __init__(self, name: str, age: int = 2):
        super().__init__(name, "Kangaroo", age, is_marsupial=True)

    def make_sound(self) -> str:
        return "*thump thump*"

    def preferred_food(self) -> str:
        return "grass"


class Wombat(Mammal):
    HABITAT_TYPE = "burrow"

    def __init__(self, name: str, age: int = 2):
        super().__init__(name, "Wombat", age, is_marsupial=True)

    def make_sound(self) -> str:
        return "*grunt*"

    def preferred_food(self) -> str:
        return "roots"


class Platypus(Mammal):
    HABITAT_TYPE = "wetland"

    def __init__(self, name: str, age: int = 2):
        super().__init__(name, "Platypus", age, is_marsupial=False)

    def make_sound(self) -> str:
        return "*soft growl*"

    def preferred_food(self) -> str:
        return "shrimp"


class Emu(Bird):
    HABITAT_TYPE = "savanna"

    def __init__(self, name: str, age: int = 2):
        super().__init__(name, "Emu", age, can_fly=False)

    def make_sound(self) -> str:
        return "*boom boom*"

    def preferred_food(self) -> str:
        return "seeds"


class WedgeTailedEagle(Bird):
    HABITAT_TYPE = "aviary"

    def __init__(self, name: str, age: int = 2):
        super().__init__(name, "Wedge-Tailed Eagle", age, can_fly=True)

    def make_sound(self) -> str:
        return "*screech*"

    def preferred_food(self) -> str:
        return "meat"


# ---------------------------------------------------------------------------
# Animal Factory
# ---------------------------------------------------------------------------

class AnimalFactory:
    """Factory for creating Animal instances by species name."""

    _registry = {
        "koala":               Koala,
        "kangaroo":            Kangaroo,
        "wombat":              Wombat,
        "platypus":            Platypus,
        "emu":                 Emu,
        "wedge-tailed eagle":  WedgeTailedEagle,
    }

    @staticmethod
    def create(species: str, name: str, age: int = 2) -> Animal:
        """
        Create and return an Animal of the given species.

        Args:
            species: lowercase species name (e.g. 'koala')
            name: the animal's individual name
            age: age in years

        Returns:
            Animal instance

        Raises:
            ValueError: if species is not recognised
        """
        cls = AnimalFactory._registry.get(species.lower())
        if cls is None:
            raise ValueError(f"Unknown species: '{species}'")
        return cls(name, age)

    @staticmethod
    def get_habitat(species: str) -> str:
        """
        Return the required HABITAT_TYPE for a given species.

        Args:
            species: lowercase species name

        Returns:
            habitat type string

        Raises:
            ValueError: if species is not recognised
        """
        cls = AnimalFactory._registry.get(species.lower())
        if cls is None:
            raise ValueError(f"Unknown species: '{species}'")
        return cls.HABITAT_TYPE