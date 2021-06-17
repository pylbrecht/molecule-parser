from collections import Counter
from typing import Dict

from sly import Parser

from molecule_parser.lexer import MoleculeLexer


def parse_molecule(formula: str) -> Dict[str, int]:
    raise NotImplementedError


class MoleculeParser(Parser):
    """
    atom        : atom ATOM
                | atom NUMBER
                | ATOM
    """

    tokens = MoleculeLexer.tokens

    def __init__(self):
        self.atoms = Counter()

    @_("atom ATOM")
    def atom(self, parser):
        self.atoms[parser.ATOM] = 1

    @_("atom NUMBER")
    def atom(self, parser):
        self.atoms[parser.atom] = int(parser.NUMBER)
        return parser.atom

    @_("ATOM")
    def atom(self, parser):
        self.atoms[parser.ATOM] = 1
        return parser.ATOM
