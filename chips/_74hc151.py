# 74hc151.py
from core.component import Component
from core.pin import PinDirection


class HC151(Component):
    """74HC151 — 8-to-1 multiplexer."""

    def __init__(self):
        super().__init__("74HC151")

        # Select lines
        self.add_pin("S0", PinDirection.INPUT)
        self.add_pin("S1", PinDirection.INPUT)
        self.add_pin("S2", PinDirection.INPUT)

        # Inputs D0..D7
        for i in range(8):
            self.add_pin(f"D{i}", PinDirection.INPUT)

        # Output
        self.add_pin("Y", PinDirection.OUTPUT)

    def update(self, tick):
        sel = (
            ((self.pins["S2"].read() or 0) << 2) |
            ((self.pins["S1"].read() or 0) << 1) |
            (self.pins["S0"].read() or 0)
        )

        val = 1 if self.pins[f"D{sel}"].read() else 0
        self.pins["Y"].write(val)