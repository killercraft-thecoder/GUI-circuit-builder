# 74hc150.py
from core.component import Component
from core.pin import PinDirection


class HC150(Component):
    """74HC150 — 16-to-1 multiplexer (active LOW output)."""

    def __init__(self):
        super().__init__("74HC150")

        # Select lines
        self.add_pin("S0", PinDirection.INPUT)
        self.add_pin("S1", PinDirection.INPUT)
        self.add_pin("S2", PinDirection.INPUT)
        self.add_pin("S3", PinDirection.INPUT)

        # Inputs D0..D15
        for i in range(16):
            self.add_pin(f"D{i}", PinDirection.INPUT)

        # Output (active LOW)
        self.add_pin("Y", PinDirection.OUTPUT)

    def update(self, tick):
        sel = (
            ((self.pins["S3"].read() or 0) << 3) |
            ((self.pins["S2"].read() or 0) << 2) |
            ((self.pins["S1"].read() or 0) << 1) |
            (self.pins["S0"].read() or 0)
        )

        val = 1 if self.pins[f"D{sel}"].read() else 0

        # Output is inverted
        self.pins["Y"].write(0 if val else 1)