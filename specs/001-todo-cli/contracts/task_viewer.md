# Contract: TaskViewerAgent

Logic for retrieving and formatting task data.

## Skills

### `list_tasks() -> Response`
- **Logic**: Retrieve all tasks from storage.
- **Success**: Returns list of tasks (empty if none).
- **Data**: `List[Dict]`

### `format_list() -> Response`
- **Logic**: Create a human-readable string representation of the tasks.
- **Success**: Returns formatted string (e.g., table or bullets).
- **Data**: `str`
