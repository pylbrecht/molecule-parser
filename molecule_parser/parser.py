import re
from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Dict

from .validators import DelimiterValidator, ValidationError


def parse_molecule(formula: str) -> Dict[str, int]:
    parser = MoleculeParser()

    try:
        parser.validate(formula)
    except ValidationError as err:
        raise SyntaxError(f"{err}") from err

    return parser.parse(formula)


class IParser(ABC):
    @abstractmethod
    def validate(self, input_: str):
        pass

    @abstractmethod
    def parse(self, input_: str):
        pass


class MoleculeParser(IParser):
    ATOM_PATTERN = re.compile(r"(?P<name>[A-Z][a-z]?)(?P<index>\d+)?")
    LDELIM_PATTERN = re.compile(r"\(|\[|\{")
    RDELIM_PATTERN = re.compile(r"(\)|\]|\})(?P<index>\d+)?")

    validators = [DelimiterValidator()]

    def __init__(self):
        self._stack = [defaultdict(int)]

    def validate(self, formula: str):
        for validator in self.validators:
            validator(formula)

    def parse(self, formular: str) -> Dict[str, int]:
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
            self._stack.append(defaultdict(int))
            tail = formular[ldelim.end() :]

        elif rdelim:
            index = int(rdelim.group("index") or 1)

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
