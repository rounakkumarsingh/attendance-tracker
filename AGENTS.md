# AGENTS.md

This document provides instructions for AI agents working on this codebase.

## Build, Lint, and Test Commands

### Installation

To set up the development environment, create a virtual environment and install the dependencies from `requirements.txt`:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

### Running the Application

The application is a command-line tool. You can run it using the `attendance` command:

```bash
attendance --help
```

### Testing

The project uses the standard Python `unittest` framework.

**Run all tests:**

```bash
python -m unittest discover tests
```

**Run a single test file:**

```bash
python -m unittest tests/test_logic.py
```

**Run a single test class:**

```bash
python -m unittest tests.test_logic.TestLogic
```

**Run a single test method:**

```bash
python -m unittest tests.test_logic.TestLogic.test_calculate_attendance_percentage
```

### Linting

There is no linter configured for this project. Please adhere to the code style guidelines below.

## Code Style Guidelines

### Formatting

-   **Indentation:** Use 4 spaces for indentation.
-   **Line Length:** Keep lines under 120 characters.
-   **Whitespace:** Use whitespace to improve readability.

### Naming Conventions

-   **Variables:** Use `snake_case` for variable names (e.g., `attendance_data`).
-   **Functions:** Use `snake_case` for function names (e.g., `calculate_attendance_percentage`).
-   **Classes:** Use `PascalCase` for class names (e.g., `TestLogic`).
-   **Constants:** Use `UPPER_SNAKE_CASE` for constants (e.g., `DATA_DIR`).

### Imports

-   **Order:** Order imports as follows:
    1.  Standard library imports (e.g., `json`, `datetime`).
    2.  Third-party library imports (e.g., `click`).
    3.  Local application imports (e.g., `from . import data_manager`).
-   **Style:** Use `import <module>` or `from <module> import <name>`.

### Types

This project does not use type hints. Maintain this style and do not add type hints.

### Docstrings

-   Use docstrings for all public modules, functions, classes, and methods.
-   The docstring should explain the purpose of the code.

### Error Handling

-   Use `try...except` blocks to handle exceptions where appropriate.
-   For example, when converting a string to a date, catch the `ValueError` and provide a helpful error message to the user.

### Comments

-   Use comments to explain complex or non-obvious code.
-   Avoid obvious comments that restate the code.

## Project Structure

-   `attendance_tracker/`: The main application package.
    -   `main.py`: The CLI entry point.
    -   `logic.py`: Contains the business logic.
    -   `data_manager.py`: Handles reading and writing data.
-   `tests/`: Contains the unit tests.
-   `setup.py`: The project setup script.
-   `requirements.txt`: The project dependencies.

## Data Storage

The application stores its data in the user's home directory under `~/.attendance-tracker`. The data is stored in JSON files:

-   `timetable.json`: The user's timetable.
-   `attendance.json`: The user's attendance records.

## General Principles

-   Keep functions small and focused on a single task.
-   Write clear and readable code.
-   Follow the existing code style.
-   Add tests for new features and bug fixes.
