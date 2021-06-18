from abc import ABC, abstractmethod


class ValidationError(Exception):
    """
    Raised by a class implementing `IValidator` in case
    the validation fails.
    """


class IValidator(ABC):
    @abstractmethod
    def __call__(self, value: str):
        pass


class DelimiterValidator(IValidator):
    """
    Validation of delimiters
    """

    def __init__(self):
        self._delim_pairs = {
            "(": ")",
            "[": "]",
            "{": "}",
        }

    def __call__(self, value: str):
        """
        Check `value` for mismatched delimiters.

        Internally we use a stack to verify that all delimiters have matching
        counterparts. If we find an opening delimiter, we push it onto the
        stack. When we encounter a closing delimiter, a matching opening
        delimiter should be on top of the stack. If there is no matching
        delimiter on top of the stack, validation fails.

        After processing `value` is complete, an empty stack indicates that
        `value` is valid. If the stack is not empty, `value` is invalid.

        :param value: value being validated
        :raises ValidationError: if validation fails
        """
        stack = []

        for char in value:
            if not self._is_delim(char):
                continue

            if self._is_open_delim(char):
                stack.append(char)
                continue

            try:
                ldelim = stack.pop()
                assert self._is_delim_pair(ldelim, char)
            except (LookupError, AssertionError) as err:
                raise ValidationError("delimiter mismatch") from err

        if stack:
            raise ValidationError("delimiter mismatch")

    def _is_delim_pair(self, ldelim: str, rdelim: str) -> bool:
        return self._delim_pairs[ldelim] == rdelim

    def _is_delim(self, char: str) -> bool:
        return char in "([{}])"

    def _is_open_delim(self, char: str) -> bool:
        return char in self._delim_pairs.keys()
