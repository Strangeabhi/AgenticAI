# General Coding Style Guide

Rule ID: GEN-STYLE-001  
Scope: all-languages

- Use clear, descriptive names for variables, functions, classes, and modules.
- Names should reflect intent, not implementation details.
- Avoid abbreviations unless they are widely understood in the language ecosystem.

Rule ID: GEN-STYLE-002  
Scope: all-languages

- Keep functions **small and focused** on a single responsibility.
- If a function is doing more than one conceptual task, consider extracting helpers.

Rule ID: GEN-STYLE-003  
Scope: all-languages

- Prefer early returns to deeply nested conditionals when it improves readability.
- Avoid more than three nesting levels of `if`, `for`, and `while` in normal application code.

Rule ID: GEN-STYLE-004  
Scope: all-languages

- Always handle exceptional or error paths explicitly (return values, error objects, or exceptions).
- Do not silently ignore errors.

Rule ID: GEN-STYLE-005  
Scope: all-languages

- Write comments to explain **why** code exists or non-obvious decisions.
- Do not add comments that simply restate what the code clearly does.

