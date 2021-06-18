import pytest

from molecule_parser import __version__, parse_molecule


def test_version():
    assert __version__ == "0.1.0"


@pytest.mark.parametrize(
    "formula,result",
    [
        ("H2O", {"H": 2, "O": 1}),
        ("Mg(OH)2", {"Mg": 1, "O": 2, "H": 2}),
        ("K4[ON(SO3)2]2", {"K": 4, "O": 14, "N": 2, "S": 4}),
        ("{[()]}", {}),
        ("", {}),
    ],
    ids=[
        "water",
        "magnesium_hydroxide",
        "fremy_salt",
        "only delimiters",
        "empty string",
    ],
)
def test_parse_molecule(formula, result):
    assert parse_molecule(formula) == result
