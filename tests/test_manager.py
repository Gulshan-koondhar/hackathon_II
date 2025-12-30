# Tests for TaskManagerAgent (Add)
from agents.manager import add_task, toggle_task, update_task, delete_task, Response
import storage

def test_add_task_success():
    resp = add_task("Buy groceries", "Milk, Eggs, Bread")
    assert resp.success is True
    assert resp.message == "Task added successfully"
    assert resp.data["id"] == 1
    assert resp.data["title"] == "Buy groceries"
    assert len(storage.TASKS) == 1

def test_add_task_empty_title():
    resp = add_task("   ")
    assert resp.success is False
    assert "cannot be empty" in resp.message
    assert len(storage.TASKS) == 0

def test_add_task_long_title():
    resp = add_task("A" * 201)
    assert resp.success is False
    assert "exceeds" in resp.message

def test_toggle_task_success():
    add_task("Toggle me")
    resp = toggle_task(1)
    assert resp.success is True
    assert storage.TASKS[0]["completed"] is True

    # Toggle back
    toggle_task(1)
    assert storage.TASKS[0]["completed"] is False

def test_update_task_success():
    add_task("Old title")
    resp = update_task(1, title="New title")
    assert resp.success is True
    assert storage.TASKS[0]["title"] == "New title"

def test_delete_task_success():
    add_task("Delete me")
    resp = delete_task(1)
    assert resp.success is True
    assert len(storage.TASKS) == 0
