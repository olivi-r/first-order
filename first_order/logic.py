import abc
import itertools


class Logic(abc.ABC):
    @abc.abstractmethod
    def __and__(self, other):
        pass

    @abc.abstractmethod
    def __invert__(self):
        pass

    @abc.abstractmethod
    def __or__(self, other):
        pass

    @abc.abstractmethod
    def __rshift__(self, other):
        pass

    @abc.abstractmethod
    def copy(self):
        pass

    @abc.abstractmethod
    def eliminate_implications(self):
        pass

    @abc.abstractmethod
    def get_unbound_terms(self):
        pass

    @abc.abstractmethod
    def move_negations_inwards(self):
        pass

    @abc.abstractmethod
    def resolve(self, interpretation):
        pass

    def __matmul__(self, other):
        if isinstance(other, dict):
            return self.resolve(other)

        return NotImplemented

    def is_satisfiable(self) -> bool:
        unbound_terms = list(self.get_unbound_terms())
        interpretations = itertools.product([True, False], repeat=len(unbound_terms))
        for interpretation in interpretations:
            if self.resolve(dict(zip(unbound_terms, interpretation))):
                return True

        return False

    def is_valid(self) -> bool:
        unbound_terms = list(self.get_unbound_terms())
        interpretations = itertools.product([True, False], repeat=len(unbound_terms))
        for interpretation in interpretations:
            if not self.resolve(dict(zip(unbound_terms, interpretation))):
                return False

        return True
