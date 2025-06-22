import pytest
import os

@pytest.fixture(scope="session", autouse=True)
def cleanup_test_db():
    yield
    if os.path.exists("test_trendpulse.db"):
        os.remove("test_trendpulse.db")