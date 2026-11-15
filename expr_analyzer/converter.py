"""Notation and three-address-code conversions."""

from .ast_tree import Binary, Num, Node, Unary


def _number(value: int | float) -> str:
    return str(value)


def infix(node: Node) -> str:
    if isinstance(node, Num):
        return _number(node.value)
    if isinstance(node, Unary):
        return f"({node.operator}{infix(node.operand)})"
    return f"({infix(node.left)} {node.operator} {infix(node.right)})"


def postfix(node: Node) -> str:
    if isinstance(node, Num):
        return _number(node.value)
    if isinstance(node, Unary):
        return f"{postfix(node.operand)} {node.operator}u"
    return f"{postfix(node.left)} {postfix(node.right)} {node.operator}"


def prefix(node: Node) -> str:
    if isinstance(node, Num):
        return _number(node.value)
    if isinstance(node, Unary):
        return f"{node.operator}u {prefix(node.operand)}"
    return f"{node.operator} {prefix(node.left)} {prefix(node.right)}"


def three_address(node: Node) -> list[str]:
    lines: list[str] = []
    counter = 0

    def visit(current: Node) -> str:
        nonlocal counter
        if isinstance(current, Num):
            return _number(current.value)
        if isinstance(current, Unary):
            operand = visit(current.operand)
            counter += 1
            name = f"t{counter}"
            lines.append(f"{name} = {current.operator}{operand}")
            return name
        left, right = visit(current.left), visit(current.right)
        counter += 1
        name = f"t{counter}"
        lines.append(f"{name} = {left} {current.operator} {right}")
        return name

    result = visit(node)
    lines.append(f"result = {result}")
    return lines
