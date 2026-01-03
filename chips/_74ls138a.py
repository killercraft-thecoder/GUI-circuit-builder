# 74ls138a.py
from core.component import Component
from core.pin import PinDirection


class LS138A(Component):
    """74LS138A — TTL 3-to-8 decoder (active LOW outputs)."""

    def __init__(self):
        super().__init__("74LS138A")

        for i in range(3):
            self.add_pin(f"A{i}", PinDirection.INPUT)

        self.add_pin("G1", PinDirection.INPUT)
        self.add_pin("G2A", PinDirection.INPUT)
        self.add_pin("G2B", PinDirection.INPUT)

        for i in range(8):
            self.add_pin(f"Y{i}", PinDirection.OUTPUT)

    def update(self, tick):
        g1 = self.pins["G1"].read()
        g2a = self.pins["G2A"].read()
        g2b = self.pins["G2B"].read()

        enabled = (g1 == 1 and g2a == 0 and g2b == 0)

        if not enabled:
            for i in range(8):
                self.pins[f"Y{i}"].write(1)
            return

        sel = (
            ((self.pins["A2"].read() or 0) << 2) |
            ((self.pins["A1"].read() or 0) << 1) |
            (self.pins["A0"].read() or 0)
        )

        for i in range(8):
            self.pins[f"Y{i}"].write(0 if i == sel else 1)