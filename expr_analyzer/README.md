# Arithmetic Expression Analyzer

Python 3.10+ project using only the standard library. It tokenizes, parses, evaluates,
and explains arithmetic expressions with integers, decimals, parentheses, unary signs,
and operators `+ - * / % ^`.

## Run

From the workspace root:

```powershell
python -m expr_analyzer.main " (3 + 4) * 2 - 8 / 4 ^ 2 "
python -m expr_analyzer.main -f expression.txt
python -m unittest discover -s expr_analyzer/tests -v
python -m expr_analyzer.gui
```

## Grammar

```text
expr    -> term (('+' | '-') term)*
term    -> power (('*' | '/' | '%') power)*
power   -> unary ('^' power)?
unary   -> ('-' | '+') unary | primary
primary -> NUMBER | '(' expr ')'
```

## Sample inputs and outputs

| Input | Output |
|---|---:|
| `1+2` | `3` |
| `2+3*4` | `14` |
| `(2+3)*4` | `20` |
| `10-4-3` | `3` |
| `100/10/5` | `2` |
| `2^3^2` | `512` |
| `-3+5` | `2` |
| `1.5*2` | `3` |
| `10%3` | `1` |
| `(3 + 4) * 2 - 8 / 4 ^ 2` | `13.5` |
