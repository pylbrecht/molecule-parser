from collections import defaultdict
from typing import Dict

from sly import Parser

from molecule_parser.lexer import MoleculeLexer


def parse_molecule(formula: str) -> Dict[str, int]:
    lexer = MoleculeLexer()
    tokens = lexer.tokenize(formula)
    parser = MoleculeParser()
    parser.parse(tokens)
    return dict(parser.atoms)


class MoleculeParser(Parser):
    """
    atom_group  : DELIM atom RDELIM
                | LDELIM atom RDELIM NUMBER
                | atom

    atom        : atom ATOM
                | atom NUMBER
                | ATOM
    """

    tokens = MoleculeLexer.tokens

    def __init__(self):
        self.atoms = defaultdict(int)

    @_("LDELIM atom RDELIM")
    def atom_group(self, parser):
        return parser.atom

    @_("LDELIM atom RDELIM NUMBER")
    def atom_group(self, parser):
        for atom in parser.atom:
            self.atoms[atom] *= int(parser.NUMBER)
        return parser.atom, parser.NUMBER

    @_("atom")
    def atom_group(self, parser):
        return parser.atom

    @_("atom ATOM")
    def atom(self, parser):
        self.atoms[parser.ATOM] = 1
        return parser.atom, parser.ATOM

    @_("atom NUMBER")
    def atom(self, parser):
        *_, atom = parser.atom
        self.atoms[atom] *= int(parser.NUMBER)
        return parser.atom, parser.NUMBER

    @_("ATOM")
    def atom(self, parser):
        self.atoms[parser.ATOM] = 1
        return parser.ATOM
