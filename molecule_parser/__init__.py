from typing import Callable, Dict

from .parser import IParser, MoleculeParser
from .validators import ValidationError

__version__ = "0.1.0"


def create_molecule_parser() -> MoleculeParser:
    return MoleculeParser()


def parse_molecule(
    formula: str, parser_factory: Callable[..., IParser] = create_molecule_parser
) -> Dict[str, int]:
    parser = create_molecule_parser()
    try:
        parser.validate(formula)
    except ValidationError as err:
        raise SyntaxError(f"{err}") from err

    return parser.parse(formula)
