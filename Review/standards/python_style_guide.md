# Python Style Guide

Rule ID: PY-NAMING-001  
Scope: python

- Follow PEP 8 naming conventions:
  - `snake_case` for functions and variables.
  - `PascalCase` for classes.
  - `SCREAMING_SNAKE_CASE` for constants.

Rule ID: PY-NAMING-002  
Scope: python

- Avoid single-letter variable names except for well-known idioms (`i`, `j`, `k` in small loops).
- Prefer meaningful, descriptive names that communicate intent.

Rule ID: PY-STRUCTURE-001  
Scope: python

- Group imports in three blocks separated by blank lines:
  - Standard library
  - Third-party
  - Local application imports
- Keep imports sorted within their block.

Rule ID: PY-ERROR-001  
Scope: python

- Do not use bare `except:` clauses.
- Catch specific exception types or use `except Exception:` only when re-raising or logging.

