# JavaScript / TypeScript Style Guide

Rule ID: JS-NAMING-001  
Scope: javascript,typescript

- Use `camelCase` for variables and functions.
- Use `PascalCase` for React components, classes, and types.

Rule ID: JS-ASYNC-001  
Scope: javascript,typescript

- Prefer `async`/`await` over raw promise chaining when it improves readability.
- Always handle rejected promises using `try`/`catch` or `.catch(...)`.

Rule ID: JS-ERROR-001  
Scope: javascript,typescript

- Do not swallow errors in empty `catch` blocks.
- At minimum, log or rethrow the error to preserve observability.

Rule ID: JS-MODULE-001  
Scope: javascript,typescript

- Use ES modules (`import` / `export`) consistently.
- Avoid mixing CommonJS (`require`, `module.exports`) and ES modules in the same module unless absolutely necessary.

