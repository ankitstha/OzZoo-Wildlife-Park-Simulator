"""Custom exception classes for OzZoo simulation."""


class InsufficientFundsError(Exception):
    """Raised when a purchase exceeds available zoo funds."""
    def __init__(self, amount: float, balance: float):
        super().__init__(f"Cannot spend ${amount:.2f} — only ${balance:.2f} available.")


class EnclosureFullError(Exception):
    """Raised when adding an animal to a full enclosure."""
    def __init__(self, enclosure_name: str):
        super().__init__(f"Enclosure '{enclosure_name}' is at full capacity.")


class IncompatibleSpeciesError(Exception):
    """Raised when incompatible species are placed in the same enclosure."""
    def __init__(self, species1: str, species2: str):
        super().__init__(f"Cannot house {species1} with {species2}.")


class InsufficientFoodError(Exception):
    """Raised when there is not enough food to feed an animal."""
    def __init__(self, food_type: str):
        super().__init__(f"Not enough '{food_type}' in inventory.")


class AnimalNotFoundError(Exception):
    """Raised when an animal ID cannot be located."""
    def __init__(self, animal_id: str):
        super().__init__(f"No animal found with ID '{animal_id}'.")