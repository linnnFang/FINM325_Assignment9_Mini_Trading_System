# fix_parser.py

class FixParser:
    
    REQUIRED_FIELDS_BY_MSGTYPE = {
        "D": ["55", "54", "38", "40"],  # New Order Single: Symbol, Side, Qty, OrdType
        "Q": ["55", "132", "133"],      # Quote: Symbol, BidPx, OfferPx
    }

    HUMAN_READABLE_TAGS = {
        "35": "MsgType",
        "55": "Symbol",
        "54": "Side",
        "38": "OrderQty",
        "40": "OrdType",
        "44": "Price",
        "132": "BidPx",
        "133": "OfferPx",
    }

    def parse(self, raw_msg: str, delimiter: str = "|") -> dict:
        """
        Parse a FIX message string into a dictionary.

        Parameters:
        - raw_msg: FIX string (tags separated by delimiter)
        - delimiter: default "|", can be changed to "\x01" for real FIX

        Returns:
        - dict with parsed FIX fields (both raw and human-readable)
        """
        # Split message into key=value pairs
        fields = raw_msg.split(delimiter)

        # Build dictionary
        fix_dict = {}
        for field in fields:
            if "=" not in field:
                continue
            tag, value = field.split("=", 1)
            fix_dict[tag] = value

            # Optionally add human-readable names
            if tag in self.HUMAN_READABLE_TAGS:
                fix_dict[self.HUMAN_READABLE_TAGS[tag]] = value

        # Validate required fields based on MsgType
        self._validate(fix_dict)

        return fix_dict

    def _validate(self, fix_dict):
        if "35" not in fix_dict:
            raise ValueError("Missing required tag 35 (MsgType)")

        msg_type = fix_dict["35"]

        if msg_type not in self.REQUIRED_FIELDS_BY_MSGTYPE:
            # Unknown message types are allowed but not validated strictly
            return

        missing = [
            tag for tag in self.REQUIRED_FIELDS_BY_MSGTYPE[msg_type]
            if tag not in fix_dict
        ]

        if missing:
            raise ValueError(f"Missing required tags for MsgType={msg_type}: {missing}")

if __name__ == "__main__":
    msg = "8=FIX.4.2|35=D|55=AAPL|54=1|38=100|40=2|44=150.25|10=128"
    print(FixParser().parse(msg))
