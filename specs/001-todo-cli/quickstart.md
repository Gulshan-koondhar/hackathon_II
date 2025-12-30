# Quickstart: 001-todo-cli (Phase 1)

Minimal In-Memory Todo CLI.

## Installation

1. Ensure Python 3.13+ is installed.
2. Clone this repository.

## Usage

Run the application:
```bash
python src/main.py
```

## Commands
The application uses a menu-driven interface:
1. **Add Task**: Prompts for title and optional description.
2. **List Tasks**: Shows all current tasks with ID and status.
3. **Update Task**: Prompts for ID and new details.
4. **Delete Task**: Prompts for ID to remove.
5. **Toggle Complete**: Prompts for ID to switch status.
6. **Show Stats**: Displays completion analytics.
7. **Exit**: Closes the application (all data will be lost).

## Development

Run tests:
```bash
pytest
```
