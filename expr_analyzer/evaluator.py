"""AST evaluation with an auditable sequence of steps."""

import math
from .ast_tree import Binary, Num, Node, Unary
from .lexer import ExprError


def _format(value: int | float) -> str:
    if isinstance(value, int) and value.bit_length() > 1024:
        raise ExprError("overflow")
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value)


def evaluate(node: Node) -> tuple[int | float, list[str]]:
    steps: list[str] = []
    step_number = 0

    def visit(current: Node) -> int | float:
        nonlocal step_number
        if isinstance(current, Num):
            return current.value
        if isinstance(current, Unary):
            value = visit(current.operand)
            result = -value if current.operator == "-" else value
            step_number += 1
            steps.append(f"{step_number}. {current.operator}{_format(value)} = {_format(result)}")
            return result
        left, right = visit(current.left), visit(current.right)
        if current.operator in ("/", "%") and right == 0:
            raise ExprError("division by zero" if current.operator == "/" else "modulo by zero")
        try:
            result = {
                "+": lambda: left + right,
                "-": lambda: left - right,
                "*": lambda: left * right,
                "/": lambda: left / right,
                "%": lambda: left % right,
                "^": lambda: left ** right,
            }[current.operator]()
        except (OverflowError, ZeroDivisionError) as error:
            raise ExprError("overflow") from error
        if isinstance(result, int) and result.bit_length() > 1024:
            raise ExprError("overflow")
        if isinstance(result, float) and not math.isfinite(result):
            raise ExprError("overflow")
        step_number += 1
        steps.append(
            f"{step_number}. {_format(left)} {current.operator} {_format(right)} = {_format(result)}"
        )
        return result

    return visit(node), steps
