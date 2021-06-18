from abc import ABC, abstractmethod


class ValidationError(Exception):
    pass


class IValidator(ABC):
    @abstractmethod
    def __call__(self, value: str):
        pass


class DelimiterValidator(IValidator):
    def __init__(self):
        self._delim_pairs = {
            "(": ")",
            "[": "]",
            "{": "}",
        }

    def __call__(self, value: str):
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
