# 28c16.py
from core.component import Component
from core.pin import PinDirection


class AT28C16(Component):
    """
    Simplified 2K × 8 EEPROM.
    Address: 11 bits (A0–A10)
    Data: 8 bits (D0–D7)
    Control: CE, OE, WE
    """

    def __init__(self):
        super().__init__("28C16")

        # Address pins
        for i in range(11):
            self.add_pin(f"A{i}", PinDirection.INPUT)

        # Data pins (bidirectional)
        for i in range(8):
            self.add_pin(f"D{i}", PinDirection.TRISTATE)

        # Control pins
        self.add_pin("CE", PinDirection.INPUT)
        self.add_pin("OE", PinDirection.INPUT)
        self.add_pin("WE", PinDirection.INPUT)

        # Internal memory
        self.state["mem"] = [0] * 2048

    def update(self, tick):
        ce = self.pins["CE"].read()
        oe = self.pins["OE"].read()
        we = self.pins["WE"].read()

        # Build address
        addr = 0
        for i in range(11):
            bit = self.pins[f"A{i}"].read()
            if bit not in (0, 1):
                return
            addr |= (bit << i)

        # Write cycle
        if ce == 0 and we == 0:
            val = 0
            for i in range(8):
                bit = self.pins[f"D{i}"].read()
                if bit not in (0, 1):
                    return
                val |= (bit << i)
            self.state["mem"][addr] = val
            return

        # Read cycle
        if ce == 0 and oe == 0 and we == 1:
            val = self.state["mem"][addr]
            for i in range(8):
                self.pins[f"D{i}"].write((val >> i) & 1)
        else:
            # High-Z data bus
            for i in range(8):
                self.pins[f"D{i}"].write(None)