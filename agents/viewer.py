# Task Viewer Agent - Logic for viewing tasks
from agents import Response
import storage

def list_tasks() -> Response:
    """Retrieve all tasks."""
    return Response(success=True, message="Tasks retrieved", data=storage.TASKS)

def format_list() -> Response:
    """Format the task list for console display."""
    tasks = storage.TASKS
    if not tasks:
        return Response(success=True, message="Standard view", data="No tasks found")

    lines = ["Current Todo List:", "-" * 20]
    for task in tasks:
        status = "[X]" if task["completed"] else "[ ]"
        lines.append(f"ID: {task['id']} {status} {task['title']}")
        if task["description"]:
            lines.append(f"   Desc: {task['description']}")

    return Response(success=True, message="Formatted view", data="\n".join(lines))
