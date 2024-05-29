from __future__ import annotations
import enum

from first_order.common import Methods
from first_order.logic import Logic
from first_order.term import Term


class Quantifier(enum.Enum):
    FORALL = "∀"
    EXISTS = "∃"


class QuantifiedSentence(Methods, Logic):
    def __init__(
        self,
        quantifier: Quantifier,
        term: Term,
        sentence: Logic,
        inverted: bool = False,
    ) -> None:
        self.quantifier = quantifier
        self.term = term
        self.sentence = sentence
        self.inverted = inverted

    def __invert__(self):
        self.inverted = not self.inverted
        return self

    def __repr__(self):
        if self.inverted:
            return f"~({self.quantifier.value} {self.term}: {self.sentence})"

        return f"({self.quantifier.value} {self.term}: {self.sentence})"

    def copy(self) -> QuantifiedSentence:
        return QuantifiedSentence(
            self.quantifier, self.term.copy(), self.sentence.copy(), self.inverted
        )

    def eliminate_implications(self) -> QuantifiedSentence:
        return QuantifiedSentence(
            self.quantifier,
            self.term,
            self.sentence.eliminate_implications(),
            self.inverted,
        )

    def get_unbound_terms(self) -> set:
        return self.sentence.get_unbound_terms() - {self.term.name}

    def move_negations_inwards(self) -> QuantifiedSentence:
        quantifier = self.quantifier
        sentence = self.sentence.copy()

        if self.inverted:
            sentence.inverted = not sentence.inverted

            if quantifier == Quantifier.FORALL:
                quantifier = Quantifier.EXISTS

            elif quantifier == Quantifier.EXISTS:
                quantifier = Quantifier.FORALL

        return QuantifiedSentence(
            quantifier, self.term, sentence.move_negations_inwards()
        )

    def resolve(self, interpretation: dict) -> bool:
        if self.quantifier == Quantifier.FORALL:
            for value in [True, False]:
                interpretation[self.term.name] = value
                if not self.sentence.resolve(interpretation):
                    result = False
                    break

            else:
                result = True

            if self.inverted:
                return not result

            return result

        elif self.quantifier == Quantifier.EXISTS:
            for value in [True, False]:
                interpretation[self.term.name] = value
                if self.sentence.resolve(interpretation):
                    result = True
                    break

            else:
                result = False

            if self.inverted:
                return not result

            return result


def ForAll(term: Term, sentence: Logic):
    return QuantifiedSentence(Quantifier.FORALL, term, sentence)


def Exists(term: Term, sentence: Logic):
    return QuantifiedSentence(Quantifier.EXISTS, term, sentence)
