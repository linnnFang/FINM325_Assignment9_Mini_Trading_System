import json
import os
from logger import Logger

def test_logger_is_singleton(tmp_path):
    # First instance with custom path
    log1_path = tmp_path / "events1.json"
    log1 = Logger(path=str(log1_path))
    log1.log("TestEvent1", {"a": 1})

    # Second instance with a different path argument should return same object
    log2_path = tmp_path / "events2.json"
    log2 = Logger(path=str(log2_path))

    assert log1 is log2
    # The path should be the one from the first construction
    assert log1.path == str(log1_path)
    assert log2.path == str(log1_path)

    # Events are shared
    assert len(log2.events) == 1
    assert log2.events[0]["event"] == "TestEvent1"

def test_logger_save_writes_json(tmp_path):
    events_path = tmp_path / "events.json"
    # Reset singleton between tests by clearing the class attribute
    from logger import Logger as LoggerClass
    LoggerClass._instance = None

    log = Logger(path=str(events_path))
    log.log("OrderCreated", {"symbol": "AAPL", "qty": 100})
    log.log("OrderFilled", {"symbol": "AAPL", "qty": 100})
    log.save()

    assert events_path.exists()
    data = json.loads(events_path.read_text())
    assert len(data) == 2
    assert data[0]["event"] == "OrderCreated"
    assert data[1]["event"] == "OrderFilled"
    # basic structure sanity
    assert "timestamp" in data[0]
    assert data[0]["data"]["symbol"] == "AAPL"