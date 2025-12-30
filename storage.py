# Shared in-memory storage for tasks

TASKS = []
NEXT_ID = 1

def reset_storage():
    """Helper for testing to reset state between runs."""
    global TASKS, NEXT_ID
    TASKS = []
    NEXT_ID = 1
