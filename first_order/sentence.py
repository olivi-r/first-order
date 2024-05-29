from __future__ import annotations
import enum

from first_order.logic import Logic


class Connective(enum.Enum):
    CONJUNCTION = "&"
    DISJUNCTION = "|"
    IMPLIES = ">>"


class Sentence(Logic):
    def __init__(
        self,
        lhs: Logic,
        rhs: Logic,
        operator: Connective,
        inverted: bool = False,
    ) -> None:
        self.lhs = lhs
        self.rhs = rhs
        self.operator = operator
        self.inverted = inverted

    def __and__(self, other):
        if isinstance(other, Logic):
            return Sentence(self, other, Connective.CONJUNCTION)

        return NotImplemented

    def __invert__(self):
        self.inverted = not self.inverted
        return self

    def __or__(self, other):
        if isinstance(other, Logic):
            return Sentence(self, other, Connective.DISJUNCTION)

        return NotImplemented

    def __repr__(self):
        if self.inverted:
            return f"~({self.lhs} {self.operator.value} {self.rhs})"

        return f"({self.lhs} {self.operator.value} {self.rhs})"

    def __rshift__(self, other):
        if isinstance(other, Logic):
            return Sentence(self, other, Connective.IMPLIES)

        return NotImplemented

    def copy(self) -> Sentence:
        return Sentence(self.lhs.copy(), self.rhs.copy(), self.operator, self.inverted)

    def eliminate_implications(self) -> Sentence:
        lhs = self.lhs.eliminate_implications()
        rhs = self.rhs.eliminate_implications()
        operator = self.operator

        if operator == Connective.IMPLIES:
            lhs = ~lhs
            operator = Connective.DISJUNCTION

        return self.__class__(lhs, rhs, operator, self.inverted)

    def get_unbound_terms(self) -> set:
        return self.lhs.get_unbound_terms() | self.rhs.get_unbound_terms()

    def move_negations_inwards(self) -> Sentence:
        lhs = self.lhs.copy()
        rhs = self.rhs.copy()
        operator = self.operator

        if self.inverted:
            lhs.inverted = not lhs.inverted
            rhs.inverted = not rhs.inverted

            if operator == Connective.CONJUNCTION:
                operator = Connective.DISJUNCTION

            elif operator == Connective.DISJUNCTION:
                operator = Connective.CONJUNCTION

        return Sentence(
            lhs.move_negations_inwards(), rhs.move_negations_inwards(), operator
        )

    def resolve(self, interpretation: dict) -> bool:
        lhs = self.lhs.resolve(interpretation)
        rhs = self.rhs.resolve(interpretation)

        if self.operator == Connective.CONJUNCTION:
            result = lhs and rhs

        elif self.operator == Connective.DISJUNCTION:
            result = lhs or rhs

        elif self.operator == Connective.IMPLIES:
            result = not lhs or rhs

        if self.inverted:
            return not result

        return result
