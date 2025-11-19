import json
import os
from importlib import reload

import logger
import main

def test_main_creates_expected_events_json(tmp_path, monkeypatch, capsys):
    # Run main.main() in a temporary working directory so events.json
    # does not clash with anything else.
    cwd = os.getcwd()
    try:
        os.chdir(tmp_path)

        # Reset Logger singleton and ensure it will write into tmp_path/events.json
        logger.Logger._instance = None

        # Reload main to ensure it imports the fresh Logger singleton state
        reload(main)

        # Call main() and capture stdout to ensure it runs without error
        main.main()
        captured = capsys.readouterr()
        assert "Scenario 1" in captured.out
        assert "Scenario 2" in captured.out

        events_path = tmp_path / "events.json"
        assert events_path.exists(), "events.json should be created by main.main()"

        events = json.loads(events_path.read_text())
        # Expect four events as per the scripted scenarios
        assert len(events) == 4

        # 1: OrderCreated for AAPL
        e1 = events[0]
        assert e1["event"] == "OrderCreated"
        assert e1["data"]["55"] == "AAPL"
        assert e1["data"]["38"] == "500"

        # 2: OrderFilled for AAPL
        e2 = events[1]
        assert e2["event"] == "OrderFilled"
        assert e2["data"]["symbol"] == "AAPL"
        assert e2["data"]["qty"] == 500

        # 3: OrderCreated for TSLA
        e3 = events[2]
        assert e3["event"] == "OrderCreated"
        assert e3["data"]["55"] == "TSLA"
        assert e3["data"]["38"] == "20000"

        # 4: OrderRejected for TSLA due to risk limit
        e4 = events[3]
        assert e4["event"] == "OrderRejected"
        assert e4["data"]["symbol"] == "TSLA"
        assert "exceeds max_order_size" in e4["data"]["reason"]
    finally:
        os.chdir(cwd)