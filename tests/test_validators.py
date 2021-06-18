import pytest

from molecule_parser.validators import DelimiterValidator, ValidationError


@pytest.mark.parametrize(
    "input_value",
    [
        "(",
        ")",
        "{",
        "}",
        "[",
        "]",
        "NO)3",
        "{NO)3",
    ],
)
def test_delimiter_validator(input_value):
    validate = DelimiterValidator()
    with pytest.raises(ValidationError, match="delimiter mismatch"):
        validate(input_value)
