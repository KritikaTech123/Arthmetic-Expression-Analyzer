"""Recursive-descent parser for the arithmetic grammar."""

from dataclasses import dataclass
from .ast_tree import Binary, Num, Unary, Node
from .lexer import ExprError, Token


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.index = 0

    @property
    def current(self) -> Token:
        return self.tokens[self.index]

    def advance(self) -> Token:
        token = self.current
        self.index += 1
        return token

    def parse(self) -> Node:
        node = self.expr()
        if self.current.type != "EOF":
            if self.current.type == "RPAREN":
                raise ExprError("extra closing bracket", self.current.position)
            raise ExprError("two operands in a row or missing operator", self.current.position)
        return node

    def expr(self) -> Node:
        node = self.term()
        while self.current.lexeme in ("+", "-"):
            operator = self.advance().lexeme
            node = Binary(operator, node, self.term())
        return node

    def term(self) -> Node:
        node = self.power()
        while self.current.lexeme in ("*", "/", "%"):
            operator = self.advance().lexeme
            if self.current.lexeme in ("*", "/", "%", "+", "-", "^", ")") or self.current.type == "EOF":
                raise ExprError("missing operand", self.current.position)
            node = Binary(operator, node, self.power())
        return node

    def power(self) -> Node:
        node = self.unary()
        if self.current.lexeme == "^":
            self.advance()
            if self.current.type == "EOF" or self.current.lexeme == ")":
                raise ExprError("missing operand", self.current.position)
            node = Binary("^", node, self.power())
        return node

    def unary(self) -> Node:
        if self.current.lexeme in ("-", "+"):
            return Unary(self.advance().lexeme, self.unary())
        return self.primary()

    def primary(self) -> Node:
        token = self.current
        if token.type == "NUMBER":
            self.advance()
            return Num(float(token.lexeme) if "." in token.lexeme else int(token.lexeme))
        if token.type == "LPAREN":
            self.advance()
            if self.current.type == "RPAREN":
                raise ExprError("empty parentheses", self.current.position)
            node = self.expr()
            if self.current.type != "RPAREN":
                raise ExprError("missing closing bracket", self.current.position)
            self.advance()
            return node
        if token.type == "RPAREN":
            raise ExprError("extra closing bracket", token.position)
        raise ExprError("missing operand", token.position)


def parse(tokens: list[Token]) -> Node:
    return Parser(tokens).parse()
