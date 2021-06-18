from typing import Dict

from .parser import MoleculeParser
from .validators import ValidationError

__version__ = "0.1.0"


def parse_molecule(formula: str) -> Dict[str, int]:
    parser = MoleculeParser()

    try:
        parser.validate(formula)
    except ValidationError as err:
        raise SyntaxError(f"{err}") from err

    return parser.parse(formula)
