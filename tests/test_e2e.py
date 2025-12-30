# End-to-End Tests for Scenario Validations
from agents.manager import add_task
from agents.viewer import format_list
import storage

def test_add_and_list_flow():
    """Scenario: Add task and verify it appears in list."""
    # 1. Start empty
    assert len(storage.TASKS) == 0

    # 2. Add task
    add_task("Buy bread", "Whole grain")

    # 3. Verify in list
    resp = format_list()
    assert "Buy bread" in resp.data
    assert "Whole grain" in resp.data
    assert "ID: 1" in resp.data
    assert "[ ]" in resp.data  # Incomplete by default
