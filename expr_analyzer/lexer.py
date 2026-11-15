"""Lexical analysis for arithmetic expressions."""

from dataclasses import dataclass


class ExprError(Exception):
    """A user-facing expression error with an optional source position."""

    def __init__(self, message: str, position: int | None = None):
        self.message = message
        self.position = position
        suffix = f" at position {position}" if position is not None else ""
        super().__init__(message + suffix)


@dataclass(frozen=True)
class Token:
    lexeme: str
    type: str
    position: int


def tokenize(text: str) -> list[Token]:
    """Convert source text to tokens, rejecting invalid characters/numbers."""
    if not text.strip():
        raise ExprError("empty expression")

    tokens: list[Token] = []
    i = 0
    while i < len(text):
        char = text[i]
        if char.isspace():
            i += 1
            continue
        if char.isdigit() or char == ".":
            start = i
            dots = 0
            digits = 0
            while i < len(text) and (text[i].isdigit() or text[i] == "."):
                dots += text[i] == "."
                digits += text[i].isdigit()
                i += 1
            lexeme = text[start:i]
            if dots > 1 or digits == 0 or lexeme == ".":
                raise ExprError(f"malformed number '{lexeme}'", start)
            tokens.append(Token(lexeme, "NUMBER", start))
            continue
        if char in "+-*/%^":
            tokens.append(Token(char, "OPERATOR", i))
            i += 1
            continue
        if char in "()":
            tokens.append(Token(char, "LPAREN" if char == "(" else "RPAREN", i))
            i += 1
            continue
        raise ExprError(f"invalid character '{char}'", i)
    tokens.append(Token("", "EOF", len(text)))
    return tokens
