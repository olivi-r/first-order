from first_order.logic import Logic
from first_order.sentence import Connective, Sentence


class Methods:
    def __and__(self, other):
        if isinstance(other, Logic):
            return Sentence(self, other, Connective.CONJUNCTION)

        return NotImplemented

    def __or__(self, other):
        if isinstance(other, Logic):
            return Sentence(self, other, Connective.DISJUNCTION)

        return NotImplemented

    def __rshift__(self, other):
        if isinstance(other, Logic):
            return Sentence(self, other, Connective.IMPLIES)

        return NotImplemented
