"""Visitor class — models a zoo guest's experience."""

import random


class Visitor:
    """Represents a single zoo visitor."""

    ADMISSION_FEE = 25.0

    def __init__(self):
        self._satisfaction: float = 70.0   # starts neutral-positive
        self._donated: float = 0.0

    @property
    def satisfaction(self): return self._satisfaction

    def visit_enclosure(self, appeal_score: float) -> None:
        """
        Update satisfaction based on enclosure appeal.

        Args:
            appeal_score: 0–100 score from Enclosure.visitor_appeal()
        """
        delta = (appeal_score - 50) * 0.2   # ±10 max per enclosure
        self._satisfaction = max(0.0, min(100.0, self._satisfaction + delta))

    def maybe_donate(self) -> float:
        """Return a donation amount if the visitor is very happy, else 0."""
        if self._satisfaction >= 85:
            self._donated = round(random.uniform(5, 50), 2)
            return self._donated
        return 0.0

    def __str__(self):
        return f"Visitor | Satisfaction: {self._satisfaction:.0f} | Donated: ${self._donated:.2f}"