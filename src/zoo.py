"""Singleton Zoo class + daily game loop logic."""

from __future__ import annotations
from exception import InsufficientFundsError, AnimalNotFoundError, InsufficientFoodError
from enclosure import Enclosure, FoodInventory
from visitor import Visitor
from animals import Animal, AnimalFactory
import random


class Zoo:
    """
    Singleton class representing OzZoo.
    Only one instance can exist at runtime.
    """

    _instance: Zoo | None = None

    def __new__(cls) -> Zoo:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialised = False
        return cls._instance

    def __init__(self):
        if self._initialised:
            return
        self._initialised = True

        self._funds: float = 25000.0
        self._day: int = 0
        self._enclosures: list[Enclosure] = []
        self._food: FoodInventory = FoodInventory()
        self._game_over: bool = False
        self._game_over_reason: str = ""

    # --- Properties ---
    @property
    def funds(self): return self._funds

    @property
    def day(self): return self._day

    @property
    def game_over(self): return self._game_over

    @property
    def enclosures(self): return list(self._enclosures)

    # --- Finance ---
    def spend(self, amount: float, reason: str = "") -> None:
        """
        Deduct funds.

        Raises:
            InsufficientFundsError: if balance is too low
        """
        if amount > self._funds:
            raise InsufficientFundsError(amount, self._funds)
        self._funds -= amount

    def earn(self, amount: float) -> None:
        """Add income to zoo funds."""
        self._funds += amount

    def buy_food(self, food_type: str, amount: float) -> None:
        """Purchase food and deduct cost from funds."""
        cost = self._food.restock(food_type, amount)
        self.spend(cost, reason=f"Buy {amount}x {food_type}")

    # --- Enclosures & animals ---
    def add_enclosure(self, enclosure: Enclosure) -> None:
        self._enclosures.append(enclosure)

    def all_animals(self) -> list[Animal]:
        animals = []
        for enc in self._enclosures:
            animals.extend(enc.animals)
        return animals

    def buy_animal(self, species: str, name: str, enclosure: Enclosure, cost: float = 500.0) -> Animal:
        """Purchase a new animal and place it in an enclosure."""
        self.spend(cost, reason=f"Buy {species} '{name}'")
        animal = AnimalFactory.create(species, name)
        enclosure.add_animal(animal)
        return animal

    def feed_animal(self, animal_name: str) -> str:
            from exception import AnimalNotFoundError, InsufficientFoodError
            target = None
            for animal in self.all_animals():
                if animal.name.lower() == animal_name.lower():
                    target = animal
                break

            if target is None:
                from exception import AnimalNotFoundError
                raise AnimalNotFoundError(animal_name)

            # Try to feed it
            food = target.preferred_food()
            self._food.consume(food)          # raises InsufficientFoodError if empty
            target.eat(food)
            return f"🍽 {target.name} the {target.species} ate {food} — hunger now {target.hunger:.0f}"
        
    def vet_animal(self, animal_name: str) -> str:
        target = next(
            (a for a in self.all_animals() if a.name.lower() == animal_name.lower()),
            None
        )
        if target is None:
            raise AnimalNotFoundError(animal_name)

        self.spend(150.0, "Vet fee")
        target._health = min(100.0, target._health + 30.0)
        target._happiness = min(100.0, target._happiness + 10.0)
        return f"{target.name} was treated — HP now {target._health:.0f}"
            
    # --- Daily tick ---
    def advance_day(self) -> dict:
        """
        Simulate one full game day.
        Returns:
            A dict of events/messages that occurred this day.
        """
        self._day += 1
        log = []

        # 1. Animal hunger & health updates
        for animal in self.all_animals():
            animal.daily_update()
            try:
                self._food.consume(animal.preferred_food())
            except Exception:
                log.append(f"⚠ No {animal.preferred_food()} for {animal.name}!")

        # 2. Feed animals that are still alive
        for enc in self._enclosures:
            enc.daily_update()

        # 3. Remove dead animals
        for enc in self._enclosures:
            dead = enc.remove_dead_animals()
            for d in dead:
                log.append(f"💀 {d.name} the {d.species} has died.")

        # 4. Visitor simulation
        visitor_count = random.randint(10, 40)
        daily_income = visitor_count * Visitor.ADMISSION_FEE
        total_donations = 0.0
        for _ in range(visitor_count):
            v = Visitor()
            for enc in self._enclosures:
                v.visit_enclosure(enc.visitor_appeal())
            total_donations += v.maybe_donate()
        self.earn(daily_income + total_donations)
        log.append(f"🎟 {visitor_count} visitors arrived — earned ${daily_income + total_donations:.2f}")

        # 5. Daily expenses (staff, utilities)
        daily_costs = 200.0
        try:
            self.spend(daily_costs, "Daily operating costs")
        except InsufficientFundsError:
            self._game_over = True
            self._game_over_reason = "Ran out of funds!"

        # 6. Breeding check
        for enc in self._enclosures:
            animals = enc.animals
            breeders = [a for a in animals if a.can_breed()]
            if len(breeders) >= 2 and random.random() < 0.1:
                parent = breeders[0]
                baby_name = f"Baby{parent.species}{self._day}"
                try:
                    new_animal = AnimalFactory.create(parent.species, baby_name, age=0)
                    enc.add_animal(new_animal)
                    log.append(f"🍼 New {parent.species} born: {baby_name}!")
                except Exception:
                    pass  # enclosure full

        # 7. Random special events
        event = self._random_event()
        if event:
            log.append(event)

        # 8. Check game-over conditions
        if not self.all_animals():
            self._game_over = True
            self._game_over_reason = "All animals have died!"

        return {"day": self._day, "funds": self._funds, "log": log}

    def _random_event(self) -> str | None:
        """Trigger a random special event with low probability."""
        events = [
            ("🌡 Heatwave! All enclosure cleanliness drops by 20.", self._heatwave),
            ("🎉 Zoo anniversary! Visitor count bonus today.", self._bonus_visitors),
        ]
        if random.random() < 0.15:
            msg, fn = random.choice(events)
            fn()
            return msg
        return None

    def _heatwave(self):
        for enc in self._enclosures:
            enc._cleanliness = max(0.0, enc._cleanliness - 20.0)

    def _bonus_visitors(self):
        bonus = random.randint(5, 15) * Visitor.ADMISSION_FEE
        self.earn(bonus)