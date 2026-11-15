# Arithmetic Expression Analyzer

Python 3.10+ project using only the standard library. It tokenizes, parses, evaluates,
and explains arithmetic expressions with integers, decimals, parentheses, unary signs,
and operators `+ - * / % ^`.

The repository also includes a static browser version in `index.html`, suitable for
deployment to Netlify.

## Run

From the workspace root:

```powershell
python -m expr_analyzer.main " (3 + 4) * 2 - 8 / 4 ^ 2 "
python -m expr_analyzer.main -f expression.txt
python -m unittest discover -s expr_analyzer/tests -v
python -m expr_analyzer.gui
```

## Deploy to Netlify

Create a new Netlify site, choose **Import an existing project**, select this GitHub
repository, leave the build command empty, and set the publish directory to `.`.
Netlify will publish the browser version at the generated site URL.

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
