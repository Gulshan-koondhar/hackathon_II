# Tests for TaskViewerAgent (List)
from agents.viewer import list_tasks, format_list
import storage
from agents.manager import add_task

def test_list_tasks_empty():
    resp = list_tasks()
    assert resp.success is True
    assert resp.data == []

def test_list_tasks_populated():
    add_task("T1")
    add_task("T2")
    resp = list_tasks()
    assert len(resp.data) == 2
    assert resp.data[0]["id"] == 1
    assert resp.data[1]["id"] == 2

def test_format_list_empty():
    resp = format_list()
    assert "No tasks found" in resp.data

def test_format_list_populated():
    add_task("Buy milk")
    resp = format_list()
    assert "Buy milk" in resp.data
    assert "ID: 1" in resp.data
