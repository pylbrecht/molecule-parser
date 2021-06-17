import re
from collections import defaultdict
from typing import Dict


def parse_molecule(formula: str) -> Dict[str, int]:
    parser = MoleculeParser()
    return parser.parse(formula)


class MoleculeParser:
    ATOM_PATTERN = re.compile(r"(?P<name>[A-Z][a-z]?)(?P<index>\d+)?")
    LDELIM_PATTERN = re.compile(r"\(|\[|\{")
    RDELIM_PATTERN = re.compile(r"(\)|\]|\})(?P<index>\d+)?")

    def __init__(self):
        self._stack = [defaultdict(int)]

    def parse(self, formular: str) -> Dict[str, int]:
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

        if tail:
            return self.parse(tail)

        return self._stack.pop()
