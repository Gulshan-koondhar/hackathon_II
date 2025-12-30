# Task Analytics Agent - Logic for calculating statistics
from agents import Response
import storage

def get_summary() -> Response:
    """Calculate total, completed, and pending counts."""
    tasks = storage.TASKS
    total = len(tasks)
    completed = sum(1 for t in tasks if t["completed"])
    pending = total - completed
    percentage = (completed / total * 100) if total > 0 else 0.0

    data = {
        "total": total,
        "completed": completed,
        "pending": pending,
        "percentage": round(percentage, 2)
    }

    return Response(
        success=True,
        message="Analytics calculated successfully",
        data=data
    )
