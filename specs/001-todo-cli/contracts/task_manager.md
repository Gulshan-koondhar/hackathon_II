# Contract: TaskManagerAgent

Logic for mutation of the todo list.

## Skills

### `add_task(title: str, description: str = "") -> Response`
- **Logic**: Validate title, create Task dict, increment ID, append to storage.
- **Success**: Task created.
- **Error**: Validation failure (empty title, exceeds length).

### `update_task(task_id: int, title: str = None, description: str = None) -> Response`
- **Logic**: Find task by ID, validate new title if provided, update fields.
- **Success**: Task updated.
- **Error**: Task not found, validation failure.

### `toggle_task(task_id: int) -> Response`
- **Logic**: Find task by ID, invert `completed` boolean.
- **Success**: Status toggled.
- **Error**: Task not found.

### `delete_task(task_id: int) -> Response`
- **Logic**: Find and remove task from list.
- **Success**: Task deleted.
- **Error**: Task not found.
