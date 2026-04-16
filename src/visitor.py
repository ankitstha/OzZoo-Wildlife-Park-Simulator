import random


class Visitor:
    ADMISSION_FEE: float = 25.0

    def __init__(self):
        self._satisfaction: float = 70.0
        self._total_donated: float = 0.0

    @property
    def satisfaction(self) -> float:
        return self._satisfaction

    @property
    def total_donated(self) -> float:
        return self._total_donated

    def visit_enclosure(self, appeal_score: float) -> None:
        delta = (appeal_score - 50.0) * 0.2
        self._satisfaction = max(0.0, min(100.0, self._satisfaction + delta))

    def maybe_donate(self) -> float:
        if self._satisfaction >= 85.0:
            donation = round(random.uniform(5.0, 50.0), 2)
            self._total_donated += donation
            return donation
        return 0.0

    def __str__(self) -> str:
        return (
            f"Visitor | Satisfaction: {self._satisfaction:.0f} "
            f"| Total Donated: ${self._total_donated:.2f}"
        )