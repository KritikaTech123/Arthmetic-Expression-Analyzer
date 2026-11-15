# Arithmetic Expression Analyzer

A compiler-design mini project that analyzes an arithmetic expression in stages, the way the front end of a compiler does: **lexical analysis → syntax analysis → syntax tree → intermediate code → evaluation**.

Written in pure Python (standard library only). No installation of packages is needed.

---

## Table of Contents
1. [Features](#features)
2. [Requirements](#requirements)
3. [Project Structure](#project-structure)
4. [How to Run](#how-to-run)
5. [Grammar](#grammar)
6. [How It Works](#how-it-works)
7. [Sample Run](#sample-run)
8. [Error Handling](#error-handling)
9. [Test Cases](#test-cases)
10. [Design Decisions](#design-decisions)
11. [Limitations and Future Scope](#limitations-and-future-scope)

---

## Features

| Stage | What the program does |
|---|---|
| Lexical analysis | Splits the input into tokens (number, operator, bracket) and prints a table of lexeme, token type and position |
| Syntax analysis | Recursive-descent parser that checks the expression against a grammar with correct precedence and associativity |
| Syntax tree | Builds an abstract syntax tree (AST) and prints it as a text tree |
| Conversions | Shows infix, postfix and prefix forms |
| Intermediate code | Generates three-address code with temporaries (t1, t2, ...) |
| Statistics | Counts operands and operators and reports the tree height |
| Evaluation | Computes the result with numbered step-by-step working |
| Error reporting | Clear messages with the character position, never a Python traceback |

Supported: integers, decimals, spaces, nested brackets, unary minus and plus, and the operators `+  -  *  /  %  ^`.

## Requirements

- Python 3.8 or later
- Tkinter (only for the optional GUI; it ships with most Python installers)

## Project Structure

```
expr_analyzer/
├── lexer.py          Tokenizer and the ExprError exception
├── parser.py         Recursive-descent parser (builds the AST)
├── ast_tree.py       AST node classes, tree printing, height and statistics
├── converter.py      Infix / postfix / prefix conversion and three-address code
├── evaluator.py      Evaluation with steps, division-by-zero and overflow checks
├── analyzer.py       Pipeline that runs every stage and formats the report
├── main.py           Command-line interface
├── gui.py            Optional Tkinter window
├── tests/
│   └── test_analyzer.py    33 unit tests
└── README.md
```

## How to Run

Open a terminal in the `expr_analyzer` folder.

**Interactive mode** (type expressions one after another, `exit` to quit):
```
python main.py
```

**Single expression:**
```
python main.py "(3 + 4) * 2 - 8 / 4 ^ 2"
```

**Many expressions from a file** (one expression per line):
```
python main.py -f inputs.txt
```

**Graphical window (optional):**
```
python gui.py
```

**Run the tests:**
```
python -m unittest discover -s tests -v
```

On some systems use `python3` instead of `python`.

## Grammar

Productions are listed from lowest to highest precedence. Left recursion has been removed so that a recursive-descent parser can be used; repetition `( ... )*` is implemented with loops, which keeps `+ - * / %` **left associative**.

```
expr     ->  term   ( ('+' | '-') term )*
term     ->  power  ( ('*' | '/' | '%') power )*
power    ->  unary  ( '^' power )?          (right associative)
unary    ->  ('-' | '+') unary  |  primary
primary  ->  NUMBER  |  '(' expr ')'
NUMBER   ->  digit+ ( '.' digit+ )?
```

| Operator | Precedence | Associativity |
|---|---|---|
| `( )` | highest | – |
| unary `-` `+` | 4 | right |
| `^` | 3 | right |
| `*` `/` `%` | 2 | left |
| `+` `-` | 1 (lowest) | left |

## How It Works

1. **Lexer (`lexer.py`)** scans the string once from left to right. Digits and `.` form a NUMBER token; each operator or bracket becomes its own token; spaces are skipped; anything else raises an error with its position. An EOF token marks the end.
2. **Parser (`parser.py`)** has one method per grammar rule (`expr`, `term`, `power`, `unary`, `primary`). It consumes tokens and builds `Num`, `Unary` and `Binary` nodes. Precedence comes from the order of the methods; associativity comes from loops (left) or recursion (right).
3. **AST (`ast_tree.py`)** stores the structure of the expression. Brackets are not stored because the tree shape already carries the grouping.
4. **Converter (`converter.py`)** walks the tree: post-order gives postfix, pre-order gives prefix, in-order with minimal brackets gives infix, and a post-order walk that allocates a temporary per operator gives three-address code.
5. **Evaluator (`evaluator.py`)** evaluates the tree bottom-up, records each operation as a step, and raises a clean error for division by zero, modulo by zero and overflow.
6. **Analyzer (`analyzer.py`)** runs all of the above, catches `ExprError` and builds the printable report.

## Sample Run

Input:
```
python main.py "(3 + 4) * 2 - 8 / 4 ^ 2"
```

Output (abridged):
```
[1] LEXICAL ANALYSIS
Lexeme    Type      Position
(         LPAREN    0
3         NUMBER    1
+         PLUS      3
...
[2] SYNTAX TREE (AST)
-
├── *
│   ├── +
│   │   ├── 3
│   │   └── 4
│   └── 2
└── /
    ├── 8
    └── ^
        ├── 4
        └── 2

[3] CONVERSIONS
Infix   : (3 + 4) * 2 - 8 / 4 ^ 2
Postfix : 3 4 + 2 * 8 4 2 ^ / -
Prefix  : - * + 3 4 2 / 8 ^ 4 2

[4] THREE-ADDRESS CODE
t1 = 3 + 4
t2 = t1 * 2
t3 = 4 ^ 2
t4 = 8 / t3
t5 = t2 - t4
result = t5

[5] STATISTICS
Operands: 6  Binary ops: 5  Unary ops: 0  Tree height: 4

[6] EVALUATION STEPS
Step 1: 3 + 4 = 7
Step 2: 7 * 2 = 14
Step 3: 4 ^ 2 = 16
Step 4: 8 / 16 = 0.5
Step 5: 14 - 0.5 = 13.5

RESULT = 13.5
```

Error example:
```
python main.py "2 * * 3"
ERROR: Missing operand before '*' (at position 4)
```

## Error Handling

| Input | Message |
|---|---|
| `2 $ 3` | Invalid character '$' (at position 2) |
| `1.2.3` | Malformed number '1.2.3' (at position 0) |
| `(2+3` | Unbalanced parentheses: missing ')' |
| `2+3)` | Unbalanced parentheses: unexpected ')' |
| `2 * * 3` | Missing operand before '*' |
| `2 +` | Missing operand: expression ends unexpectedly |
| `2 * ()` | Empty parentheses '()' |
| `2 3` | Unexpected token '3' |
| *(blank)* | Empty expression |
| `5/0` | Division by zero |
| `5%0` | Modulo by zero |
| `9^9^9` | Overflow in exponentiation |

## Test Cases

| Input | Expected result | What it checks |
|---|---|---|
| `1+2` | 3 | basic addition |
| `2+3*4` | 14 | precedence |
| `(2+3)*4` | 20 | brackets override precedence |
| `((1+2)*(3+4))-5` | 16 | nested brackets |
| `10-4-3` | 3 | left associativity of `-` |
| `100/10/5` | 2 | left associativity of `/` |
| `2^3^2` | 512 | right associativity of `^` |
| `-3+5` | 2 | unary minus |
| `--4` | 4 | double unary minus |
| `1.5*2` | 3 | decimals |
| `10%3` | 1 | modulo |
| `(3 + 4) * 2 - 8 / 4 ^ 2` | 13.5 | mixed operators |
| `(3+4)*2` | postfix `3 4 + 2 *`, prefix `* + 3 4 2` | conversions |
| `1+2*3` | `t1 = 2 * 3`, `t2 = 1 + t1` | three-address code |

The suite in `tests/test_analyzer.py` has 33 tests covering the valid cases above, every error in the error table, the conversions and the statistics.

## Design Decisions

- **Recursive descent** was chosen because each grammar rule maps to one function, which is easy to read, debug and explain.
- **AST first, everything else from the tree.** Postfix, prefix, infix, three-address code and evaluation are all simple walks of the same tree, so there is one source of truth.
- **One exception type (`ExprError`)** carries a message and a position, so the interface never needs to handle raw Python errors.
- **Unary minus binds tighter than `^`**, so `-2^2` is `(-2)^2 = 4`. To use the mathematical convention `-(2^2) = -4`, make `power` call `unary` only for the exponent and let `unary` wrap `power` instead of `primary`.

## Limitations and Future Scope

- No variables, functions (`sin`, `sqrt`) or constants (`pi`) yet.
- Numbers are floating point, so very long decimals can show rounding differences.
- Possible extensions: variables with an assignment statement, a function table, a Pratt/shunting-yard parser for comparison, a graphical drawing of the AST (Graphviz), a DFA diagram generator for the lexer, and optimisation passes such as constant folding.
