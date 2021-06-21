import logging
import re
from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Dict

from .validators import DelimiterValidator

logger = logging.getLogger(__name__)


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
            logger.debug(f"Validating {repr(formula)} with {validate}...")
            validate(formula)

    def parse(self, formula: str) -> Dict[str, int]:
        """
        Parse `formula` and return a `dict` mapping atoms to their count of
        occurrences.

        :param formula: chemical formula
        :returns: a `dict` mapping atoms to their occurrence count
        :raises SyntaxError: for bad characters in `formula`
        """
        if not formula:
            logger.debug("Nothing to parse, returning {}")
            return {}

        tail = None

        atom = self.ATOM_PATTERN.match(formula)
        ldelim = self.LDELIM_PATTERN.match(formula)
        rdelim = self.RDELIM_PATTERN.match(formula)

        if atom:
            logger.debug(f"Found atom token {repr(atom.group())}")
            name = atom.group("name")
            index = int(atom.group("index") or 1)

            molecule = self._stack.pop()
            molecule[name] = index
            self._stack.append(molecule)

            tail = formula[atom.end() :]

        elif ldelim:
            logger.debug(f"Found ldelim token {repr(ldelim.group())}")
            # enter new context
            self._stack.append(defaultdict(int))
            tail = formula[ldelim.end() :]

        elif rdelim:
            logger.debug(f"Found rdelim token {repr(rdelim.group())}")
            index = int(rdelim.group("index") or 1)

            # merge outer and inner context
            for name, value in self._stack.pop().items():
                molecule = self._stack.pop()
                molecule[name] += value * index
                self._stack.append(molecule)

            tail = formula[rdelim.end() :]

        else:
            logger.debug(f"Found bad character {repr(formula[0])}")
            raise SyntaxError(f"bad character {repr(formula[0])}")

        if tail:
            logger.debug(f"Calling with remainder {repr(tail)}")
            return self.parse(tail)

        return self._stack.pop()
