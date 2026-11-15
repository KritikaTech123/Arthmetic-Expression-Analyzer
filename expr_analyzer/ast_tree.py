"""AST node types and tree/statistics utilities."""

from dataclasses import dataclass
from typing import Union


@dataclass(frozen=True)
class Num:
    value: int | float


@dataclass(frozen=True)
class Unary:
    operator: str
    operand: "Node"


@dataclass(frozen=True)
class Binary:
    operator: str
    left: "Node"
    right: "Node"


Node = Union[Num, Unary, Binary]


def label(node: Node) -> str:
    if isinstance(node, Num):
        return str(node.value)
    return node.operator


def tree_lines(node: Node) -> list[str]:
    lines = [label(node)]

    def walk(current: Node, prefix: str, is_last: bool) -> None:
        children = ([current.operand] if isinstance(current, Unary)
                    else [current.left, current.right] if isinstance(current, Binary)
                    else [])
        for index, child in enumerate(children):
            last = index == len(children) - 1
            lines.append(prefix + ("└── " if last else "├── ") + label(child))
            walk(child, prefix + ("    " if last else "│   "), last)

    walk(node, "", True)
    return lines


def tree_print(node: Node) -> str:
    return "\n".join(tree_lines(node))


def height(node: Node) -> int:
    if isinstance(node, Num):
        return 1
    children = [node.operand] if isinstance(node, Unary) else [node.left, node.right]
    return 1 + max(height(child) for child in children)


def statistics(node: Node) -> dict[str, int]:
    if isinstance(node, Num):
        return {"operands": 1, "operators": 0, "height": 1}
    children = [node.operand] if isinstance(node, Unary) else [node.left, node.right]
    values = [statistics(child) for child in children]
    return {
        "operands": sum(item["operands"] for item in values),
        "operators": 1 + sum(item["operators"] for item in values),
        "height": height(node),
    }
