import pytest
from fix_parser import FixParser

def test_parse_basic_new_order_single():
    parser = FixParser()
    raw = "8=FIX.4.2|35=D|55=AAPL|54=1|38=100|40=2|10=128"
    msg = parser.parse(raw)

    # Raw tags
    assert msg["8"] == "FIX.4.2"
    assert msg["35"] == "D"
    assert msg["55"] == "AAPL"
    assert msg["54"] == "1"
    assert msg["38"] == "100"
    assert msg["40"] == "2"

    # Human readable keys
    assert msg["MsgType"] == "D"
    assert msg["Symbol"] == "AAPL"
    assert msg["Side"] == "1"
    assert msg["OrderQty"] == "100"
    assert msg["OrdType"] == "2"

def test_parse_uses_custom_delimiter():
    parser = FixParser()
    raw = "8=FIX.4.2\x0135=Q\x0155=MSFT\x01132=101.5\x01133=102.0\x01"
    msg = parser.parse(raw, delimiter="\x01")  # <-- key change

    assert msg["35"] == "Q"
    assert msg["55"] == "MSFT"
    assert msg["132"] == "101.5"
    assert msg["133"] == "102.0"

def test_missing_msgtype_raises():
    parser = FixParser()
    raw = "8=FIX.4.2|55=AAPL|38=100|40=2|10=128"
    with pytest.raises(ValueError) as excinfo:
        parser.parse(raw)
    assert "Missing required tag 35" in str(excinfo.value)

def test_missing_required_fields_for_known_msgtype_raises():
    parser = FixParser()
    # Missing 38 (OrderQty)
    raw = "8=FIX.4.2|35=D|55=AAPL|54=1|40=2|10=128"
    with pytest.raises(ValueError) as excinfo:
        parser.parse(raw)
    assert "Missing required tags for MsgType=D" in str(excinfo.value)
    assert "38" in str(excinfo.value)

def test_unknown_msgtype_is_not_strictly_validated():
    parser = FixParser()
    # MsgType=Z is unknown, but parser should not raise validation error
    raw = "8=FIX.4.2|35=Z|55=AAPL|54=1|38=100|40=2|10=128"
    msg = parser.parse(raw)
    assert msg["35"] == "Z"
    # No exception means unknown message types are accepted
