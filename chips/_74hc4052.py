# 74hc4052.py
from core.component import Component
from core.pin import PinDirection


class HC4052(Component):
    """74HC4052 — Dual 4-channel analog multiplexer."""

    def __init__(self):
        super().__init__("74HC4052")

        # Select lines
        self.add_pin("S0", PinDirection.INPUT)
        self.add_pin("S1", PinDirection.INPUT)

        # Enable (active LOW)
        self.add_pin("EN", PinDirection.INPUT)

        # Two banks: X0..X3 and Y0..Y3
        for i in range(4):
            self.add_pin(f"X{i}", PinDirection.INPUT)
            self.add_pin(f"Y{i}", PinDirection.INPUT)

        self.add_pin("A", PinDirection.OUTPUT)
        self.add_pin("B", PinDirection.OUTPUT)

    def update(self, tick):
        en = self.pins["EN"].read()

        if en == 1:
            self.pins["A"].write(None)
            self.pins["B"].write(None)
            return

        sel = ((self.pins["S1"].read() or 0) << 1) | \
              (self.pins["S0"].read() or 0)

        self.pins["A"].write(self.pins[f"X{sel}"].read())
        self.pins["B"].write(self.pins[f"Y{sel}"].read())