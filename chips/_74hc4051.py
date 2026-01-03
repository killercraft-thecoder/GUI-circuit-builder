# 74hc4051.py
from core.component import Component
from core.pin import PinDirection


class HC4051(Component):
    """74HC4051 — 8-channel analog multiplexer/demultiplexer."""

    def __init__(self):
        super().__init__("74HC4051")

        # Select lines
        self.add_pin("S0", PinDirection.INPUT)
        self.add_pin("S1", PinDirection.INPUT)
        self.add_pin("S2", PinDirection.INPUT)

        # Enable (active LOW)
        self.add_pin("EN", PinDirection.INPUT)

        # Channels X0..X7 and common I/O
        for i in range(8):
            self.add_pin(f"X{i}", PinDirection.INPUT)

        self.add_pin("Y", PinDirection.OUTPUT)

    def update(self, tick):
        en = self.pins["EN"].read()

        if en == 1:
            self.pins["Y"].write(None)
            return

        sel = ((self.pins["S2"].read() or 0) << 2) | \
              ((self.pins["S1"].read() or 0) << 1) | \
              (self.pins["S0"].read() or 0)

        val = self.pins[f"X{sel}"].read()
        self.pins["Y"].write(val)