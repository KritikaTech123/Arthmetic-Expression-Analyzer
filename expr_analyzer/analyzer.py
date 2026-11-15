"""End-to-end expression analysis and report formatting."""

from .ast_tree import statistics, tree_print
from .converter import infix, postfix, prefix, three_address
from .evaluator import evaluate
from .lexer import ExprError, Token, tokenize
from .parser import parse


def analyze(text: str) -> str:
    tokens = tokenize(text)
    tree = parse(tokens)
    value, steps = evaluate(tree)
    stats = statistics(tree)
    token_rows = "\n".join(
        f"{token.position:<8} {token.type:<10} {token.lexeme or '<EOF>'}" for token in tokens
    )
    tac = "\n".join(three_address(tree))
    return "\n".join([
        "TOKEN TABLE",
        "Position Type       Lexeme",
        token_rows,
        "",
        "SYNTAX TREE",
        tree_print(tree),
        "",
        f"INFIX:   {infix(tree)}",
        f"POSTFIX: {postfix(tree)}",
        f"PREFIX:  {prefix(tree)}",
        "",
        "THREE-ADDRESS CODE",
        tac,
        "",
        "STATISTICS",
        f"Operands: {stats['operands']}",
        f"Operators: {stats['operators']}",
        f"Tree height: {stats['height']}",
        "",
        "EVALUATION STEPS",
        *steps,
        "",
        f"RESULT: {value:g}" if isinstance(value, float) else f"RESULT: {value}",
    ])


def analyze_safe(text: str) -> str:
    try:
        return analyze(text)
    except ExprError as error:
        return f"Error: {error}"
