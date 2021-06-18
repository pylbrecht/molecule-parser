import re
from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Dict

from .validators import DelimiterValidator


class IMoleculeParser(ABC):
    @abstractmethod
    def validate(self, input_: str):
        pass

    @abstractmethod
    def parse(self, input_: str) -> Dict[str, int]:
        pass


class MoleculeParser(IMoleculeParser):
    """
    Parser for chemical formulas.

    The parser implements a recursive, stack based algorithm parsing the
    formula from left to right.

    Make sure to validate input before parsing by calling `validate(input)`.
    """

    ATOM_PATTERN = re.compile(r"(?P<name>[A-Z][a-z]?)(?P<index>\d+)?")
    LDELIM_PATTERN = re.compile(r"\(|\[|\{")
    RDELIM_PATTERN = re.compile(r"(\)|\]|\})(?P<index>\d+)?")

    validators = [DelimiterValidator()]

    def __init__(self):
        self._stack = [defaultdict(int)]

    def validate(self, formula: str):
        """
        Validate `formula` with all available validators.

        :param formula: a chemical formula
        :raises ValidationError: if `formula` is not valid
        """
        for validate in self.validators:
            validate(formula)

    def parse(self, formular: str) -> Dict[str, int]:
        """
        Parse `formula` and return a `dict` mapping atoms to their count of
        occurrences.

        :param formula: chemical formula
        :returns: a `dict` mapping atoms to their occurrence count
        :raises SyntaxError: for bad characters in `formula`
        """
        if not formular:
            return {}

        tail = None

        atom = self.ATOM_PATTERN.match(formular)
        ldelim = self.LDELIM_PATTERN.match(formular)
        rdelim = self.RDELIM_PATTERN.match(formular)

        if atom:
            name = atom.group("name")
            index = int(atom.group("index") or 1)

            molecule = self._stack.pop()
            molecule[name] = index
            self._stack.append(molecule)

            tail = formular[atom.end() :]

        elif ldelim:
            # enter new context
            self._stack.append(defaultdict(int))
            tail = formular[ldelim.end() :]

        elif rdelim:
            index = int(rdelim.group("index") or 1)

            # merge outer and inner context
            for name, value in self._stack.pop().items():
                molecule = self._stack.pop()
                molecule[name] += value * index
                self._stack.append(molecule)

            tail = formular[rdelim.end() :]

        else:
            raise SyntaxError(f"bad character {repr(formular[0])}")

        if tail:
            return self.parse(tail)

        return self._stack.pop()
