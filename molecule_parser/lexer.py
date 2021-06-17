from sly import Lexer


class MoleculeLexer(Lexer):
    tokens = {ATOM, NUMBER, LDELIM, RDELIM}

    ATOM = r"[A-Z][a-z]?"
    NUMBER = r"\d+"
    LDELIM = r"\(|\[|\{"
    RDELIM = r"\)|\]|\}"
