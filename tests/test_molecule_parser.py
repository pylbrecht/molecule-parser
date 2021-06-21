import logging

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


@pytest.mark.parametrize(
    "invalid_input,error_msg",
    [
        ("-", "bad character '-'"),
        ("(NO", "delimiter mismatch"),
        ("NO)", "delimiter mismatch"),
        ("123456", "bad character '1'"),
    ],
    ids=[
        "bad character",
        "mismatched closed parenthesis",
        "mismatched open parenthesis",
        "only numbers",
    ],
)
def test_raise_exception_for_invalid_syntax(invalid_input, error_msg):
    with pytest.raises(SyntaxError, match=error_msg):
        parse_molecule(invalid_input)


def test_info_logging_for_happy_path(caplog):
    formula = "H2O"
    with caplog.at_level(logging.INFO):
        parse_molecule(formula)

    assert f"Validating formula {repr(formula)}..." in caplog.text
    assert f"Successfully validated formula {repr(formula)}" in caplog.text
    assert f"Parsing formula {repr(formula)}..." in caplog.text
    assert f"Successfully parsed formula {repr(formula)}" in caplog.text


def test_error_logging_for_failed_validation(caplog):
    invalid_formula = "(H2O"
    with caplog.at_level(logging.ERROR), pytest.raises(SyntaxError):
        parse_molecule(invalid_formula)

    assert (
        f"Validation failed for formula {repr(invalid_formula)}: delimiter mismatch"
        in caplog.text
    )


def test_debug_logging_for_empty_formula(caplog):
    empty_formula = ""
    with caplog.at_level(logging.DEBUG):
        parse_molecule(empty_formula)

    assert "Nothing to parse, returning {}" in caplog.text


def test_debug_logging_for_happy_path(caplog):
    with caplog.at_level(logging.DEBUG):
        parse_molecule("Mg(OH)2")

    assert "Found atom token 'Mg'" in caplog.text
    assert "Calling with remainder '(OH)2'" in caplog.text
    assert "Found ldelim token '('" in caplog.text
    assert "Calling with remainder 'OH)2'" in caplog.text
    assert "Found atom token 'O'" in caplog.text
    assert "Found atom token 'H'" in caplog.text
    assert "Calling with remainder ')2'" in caplog.text
    assert "Found rdelim token ')2'" in caplog.text


def test_debug_logging_for_bad_character(caplog):
    bad_character = "$"
    with caplog.at_level(logging.DEBUG), pytest.raises(SyntaxError):
        parse_molecule(bad_character)

    assert f"Found bad character {repr(bad_character)}" in caplog.text


def test_debug_logging_for_failed_validation(caplog):
    invalid_formula = "NO)3"
    with caplog.at_level(logging.DEBUG), pytest.raises(SyntaxError):
        parse_molecule(invalid_formula)

    assert (
        f"Validating {repr(invalid_formula)} with DelimiterValidator..." in caplog.text
    )
