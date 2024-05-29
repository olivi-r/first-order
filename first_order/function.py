from __future__ import annotations

from first_order.common import Methods
from first_order.logic import Logic
from first_order.term import Term


class Function(Methods, Logic):
    def __init__(self, name: str, *args: Term, inverted: bool = False) -> None:
        self.name = name
        self.args = args
        self.inverted = inverted

    def __invert__(self):
        self.inverted = not self.inverted
        return self

    def __repr__(self):
        return f"{self.name}({', '.join(map(str, self.args))})"

    def copy(self) -> Function:
        return self.__class__(self.name, *self.args, inverted=self.inverted)

    def eliminate_implications(self) -> Function:
        return self.copy()

    def get_unbound_terms(self) -> set:
        return set(self.args)

    def move_negations_inwards(self) -> Function:
        return self.copy()

    def resolve(self, interpretation: dict) -> bool:
        return interpretation[self.name](
            *[arg.resolve(interpretation) for arg in self.args]
        )
