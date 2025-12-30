import pytest
from storage import reset_storage

@pytest.fixture(autouse=True)
def clean_storage():
    reset_storage()
    yield
