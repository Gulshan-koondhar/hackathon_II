# Task Manager Agent - Logic for modifying tasks
from agents import Response, MAX_TITLE_LENGTH, MAX_DESCRIPTION_LENGTH
import storage

def add_task(title: str, description: str = "") -> Response:
    """Add a new task to in-memory storage."""
    # Validation
    title = title.strip() if title else ""
    if not title:
        return Response(success=False, message="Task title cannot be empty")

    if len(title) > MAX_TITLE_LENGTH:
        return Response(success=False, message=f"Task title exceeds {MAX_TITLE_LENGTH} characters")

    # Optional description check - although FRs imply it's optional, we still validate length
    if description and len(description) > MAX_DESCRIPTION_LENGTH:
        return Response(success=False, message=f"Task description exceeds {MAX_DESCRIPTION_LENGTH} characters")

    # Creation
    task = {
        "id": storage.NEXT_ID,
        "title": title,
        "description": description,
        "completed": False
    }

    storage.TASKS.append(task)
    storage.NEXT_ID += 1

    return Response(success=True, message="Task added successfully", data=task)

def toggle_task(task_id: int) -> Response:
    """Toggle completion status of a task by ID."""
    for task in storage.TASKS:
        if task["id"] == task_id:
            task["completed"] = not task["completed"]
            status = "completed" if task["completed"] else "incomplete"
            return Response(success=True, message=f"Task {task_id} marked as {status}", data=task)

    return Response(success=False, message=f"Task with ID {task_id} not found")

def update_task(task_id: int, title: str = None, description: str = None) -> Response:
    """Update task title or description by ID."""
    for task in storage.TASKS:
        if task["id"] == task_id:
            if title is not None:
                title = title.strip()
                if not title:
                    return Response(success=False, message="Task title cannot be empty")
                if len(title) > MAX_TITLE_LENGTH:
                    return Response(success=False, message=f"Task title exceeds {MAX_TITLE_LENGTH} characters")
                task["title"] = title

            if description is not None:
                if len(description) > MAX_DESCRIPTION_LENGTH:
                    return Response(success=False, message=f"Task description exceeds {MAX_DESCRIPTION_LENGTH} characters")
                task["description"] = description

            return Response(success=True, message=f"Task {task_id} updated successfully", data=task)

    return Response(success=False, message=f"Task with ID {task_id} not found")

def delete_task(task_id: int) -> Response:
    """Delete task by ID."""
    for i, task in enumerate(storage.TASKS):
        if task["id"] == task_id:
            storage.TASKS.pop(i)
            return Response(success=True, message=f"Task {task_id} deleted successfully")

    return Response(success=False, message=f"Task with ID {task_id} not found")
