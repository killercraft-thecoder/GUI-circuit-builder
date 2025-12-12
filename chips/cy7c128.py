# CY7C128.py
from core.component import Component
from core.pin import PinDirection


class CY7C128(Component):
    """
    CY7C128 — 128K × 8 static RAM.
    Address: A0–A16
    Data: D0–D7 (tri-state)
    Control: CE, OE, WE
    """

    def __init__(self):
        super().__init__("CY7C128")

        # Address pins (17 bits → 128K)
        for i in range(17):
            self.add_pin(f"A{i}", PinDirection.INPUT)

        # Data pins
        for i in range(8):
            self.add_pin(f"D{i}", PinDirection.TRISTATE)

        # Control
        self.add_pin("CE", PinDirection.INPUT)
        self.add_pin("OE", PinDirection.INPUT)
        self.add_pin("WE", PinDirection.INPUT)

        # Memory array
        self.state["mem"] = [0] * 131072  # 128K x 8

    def update(self, tick):
        ce = self.pins["CE"].read() or 0
        oe = self.pins["OE"].read() or 0
        we = self.pins["WE"].read() or 0

        # Build address
        addr = 0
        for i in range(17):
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
            # High-Z
            for i in range(8):
                self.pins[f"D{i}"].write(None)