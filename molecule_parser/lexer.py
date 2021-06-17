from sly import Lexer


class MoleculeLexer(Lexer):
    tokens = {ATOM, NUMBER}

    ATOM = r"[A-Z][a-z]?"
    NUMBER = r"\d+"
