# 74ls251.py
from core.component import Component
from core.pin import PinDirection


class LS251(Component):
    """74LS251 — 8-to-1 multiplexer with tri-state output."""

    def __init__(self):
        super().__init__("74LS251")

        for i in range(8):
            self.add_pin(f"D{i}", PinDirection.INPUT)

        self.add_pin("S0", PinDirection.INPUT)
        self.add_pin("S1", PinDirection.INPUT)
        self.add_pin("S2", PinDirection.INPUT)

        self.add_pin("OE", PinDirection.INPUT)  # active LOW
        self.add_pin("Y", PinDirection.OUTPUT)

    def update(self, tick):
        oe_n = self.pins["OE"].read()

        if oe_n == 1:
            self.pins["Y"].write(None)
            return

        sel = (
            ((self.pins["S2"].read() or 0) << 2) |
            ((self.pins["S1"].read() or 0) << 1) |
            (self.pins["S0"].read() or 0)
        )

        val = 1 if self.pins[f"D{sel}"].read() else 0
        self.pins["Y"].write(val)