import logging
from typing import Callable, Dict

from .parser import IMoleculeParser, MoleculeParser
from .validators import ValidationError

__version__ = "0.1.0"


logger = logging.getLogger(__name__)


def create_molecule_parser() -> MoleculeParser:
    """
    Return a `MoleculeParser` instance.

    We use a factory here mainly to avoid stale state of validators
    (`MoleculeParser`'s validators are instantiated on import).
    """
    return MoleculeParser()


def parse_molecule(
    formula: str,
    parser_factory: Callable[..., IMoleculeParser] = create_molecule_parser,
) -> Dict[str, int]:
    """
    Parse a chemical `formula` and return a `dict` mapping each atom to its
    count of occurrences.

    :param formula: chemical formula (e.g. "H2O")
    :param parser_factory: callable returning a molecule parser
    :returns: `dict` mapping atoms to their occurrence count
    :raises SyntaxError: for invalid input (bad characters, mismatched parenthesis)

    >>> from molecule_parser import parse_molecule
    >>> parse_molecule("Mg(OH)2")
    {'Mg': 1, 'O': 2, 'H': 2}
    """
    parser = create_molecule_parser()

    logger.info(f"Validating formula {repr(formula)}...")
    try:
        parser.validate(formula)
    except ValidationError as err:
        raise SyntaxError(f"{err}") from err
    logger.info(f"Successfully validated formula {repr(formula)}")

    logger.info(f"Parsing formula {repr(formula)}...")
    molecule = parser.parse(formula)
    logger.info(f"Successfully parsed formula {repr(formula)}")

    return molecule
