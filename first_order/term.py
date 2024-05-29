from __future__ import annotations

from first_order.common import Methods
from first_order.logic import Logic


class Term(Methods, Logic):
    def __init__(self, name: str, inverted: bool = False) -> None:
        self.name = name
        self.inverted = inverted

    def __invert__(self):
        return Term(self.name, inverted=not self.inverted)

    def __repr__(self):
        if self.inverted:
            return f"~{self.name}"

        return self.name

    def copy(self) -> Term:
        return Term(self.name, self.inverted)

    def eliminate_implications(self) -> Term:
        return self.copy()

    def get_unbound_terms(self) -> set:
        return {self.name}

    def move_negations_inwards(self) -> Term:
        return self.copy()

    def resolve(self, interpretation: dict) -> bool:
        if self.inverted:
            return not interpretation[self.name]

        return interpretation[self.name]
