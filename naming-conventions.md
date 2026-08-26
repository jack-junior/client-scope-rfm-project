# Notes — Python Naming Conventions

**Track:** Data Science & Machine Learning
**Topic:** Naming conventions for variables, functions, classes, and more (based on PEP 8)

---

## 1. Why Naming Conventions Matter

Consistent naming makes code easier to read, debug, and collaborate on. Python's official style guide, **PEP 8**, defines the conventions most Python code (and libraries like pandas, scikit-learn, etc.) follows.

---

## 2. Variables

**Convention:** `snake_case` — lowercase words separated by underscores.

```python
student_name = "Othniel"
total_score = 87
learning_rate = 0.01
```

- Use descriptive names, not single letters (except in short loops or math contexts, e.g., `i`, `x`, `y`).
- Avoid ambiguous names like `data2` or `temp` when a clearer name is possible (`cleaned_data`, `raw_temperature`).

```python
# Not great
d = 42

# Better
days_remaining = 42
```

---

## 3. Functions

**Convention:** `snake_case`, and names should usually be a **verb or verb phrase** describing what the function does.

```python
def calculate_average(scores):
    return sum(scores) / len(scores)

def load_dataset(path):
    ...

def is_valid_email(email):   # boolean-returning functions often start with is_/has_/can_
    ...
```

### Application

- `train_model()`, `clean_text()`, `fetch_data()` — clear, action-based names used constantly in ML pipelines.

---

## 4. Classes

**Convention:** `PascalCase` (a.k.a. `CapWords`) — each word capitalized, no underscores.

```python
class StudentRecord:
    def __init__(self, name, track):
        self.name = name
        self.track = track


class LinearRegressionModel:
    ...
```

### Application

- Model classes (`RandomForestClassifier`, `NeuralNetwork`), data classes (`Dataset`, `Pipeline`), and any custom object type.

---

## 5. Constants

**Convention:** `UPPER_SNAKE_CASE` — all uppercase, words separated by underscores. Used for values that shouldn't change during execution.

```python
MAX_EPOCHS = 100
DEFAULT_LEARNING_RATE = 0.001
DATABASE_URL = "postgresql://localhost:5432/taiss2026"
```

---

## 6. Modules & Packages

**Convention:** short, all-lowercase names, underscores only if it improves readability. Avoid hyphens (not importable) and camelCase.

```python
# Good file names
data_utils.py
model_training.py
airflow_dags.py

# Avoid
DataUtils.py
data-utils.py
```

---

## 7. Private / Internal Names

Python has no true "private" variables, but conventions signal intent:

```python
class Model:
    def __init__(self):
        self._internal_state = None      # single underscore: "internal use" convention
        self.__strict_private = None     # double underscore: name-mangled, avoid external access

    def _helper_method(self):            # internal helper, not part of the public API
        ...
```

- `_single_leading_underscore` → "internal use," not enforced but respected by convention.
- `__double_leading_underscore` → triggers name mangling, rarely needed outside library internals.
- `__dunder__` (double underscore both sides) → reserved for Python's built-in special methods (`__init__`, `__str__`, `__len__`). Don't invent your own dunder names.

---

## 8. Booleans

Prefix with `is_`, `has_`, `can_`, or `should_` so the variable/function reads like a yes/no question.

```python
is_active = True
has_missing_values = df.isnull().values.any()
can_deploy = tests_passed and model_score > 0.8
```

---

## 9. Summary Table

| Element | Convention | Example |
|---|---|---|
| Variable | `snake_case` | `total_score` |
| Function | `snake_case`, verb-based | `calculate_average()` |
| Class | `PascalCase` | `StudentRecord` |
| Constant | `UPPER_SNAKE_CASE` | `MAX_EPOCHS` |
| Module/file | lowercase, `snake_case` if needed | `data_utils.py` |
| Internal/private | leading underscore(s) | `_helper()`, `__private` |
| Boolean | `is_`/`has_`/`can_` prefix | `is_valid`, `has_data` |

---

## 10. Quick Rules of Thumb

- Be descriptive, not clever — `customer_age` beats `ca`.
- Match the convention to the *type* of thing (variable vs. class vs. constant), not personal preference.
- Consistency across a project matters more than any single "correct" choice — follow the codebase you're contributing to.
- Run a linter (e.g., `flake8` or `pylint`) to catch naming issues automatically.

---

## 11. Practice Ideas

- Refactor a messy script (e.g., variables named `x1`, `df2`, `func`) into properly named equivalents.
- Write a small `Dataset` class and a `load_data()` / `clean_data()` function pair following these conventions.
- Run `flake8` on an existing exercise file and fix any naming warnings it flags.


## 12. Exceptions

- PEP 8's snake_case recommendation applies to Python modules (.py files), because hyphens aren't valid in Python identifiers — import naming-conventions would break, since Python reads the hyphen as a minus sign. That constraint doesn't exist for Markdown files; they're never imported, so there's no syntax reason to avoid hyphens.

- For documentation files specifically, kebab-case (word-word.md) is the more common convention across the Python/open-source ecosystem — used by tools like Sphinx, MkDocs, and most GitHub wikis/docs folders. It's also slightly more readable in URLs and rendered file trees (GitHub, docs sites) since hyphens render as spaces more naturally than underscores.