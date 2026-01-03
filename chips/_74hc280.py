# 74hc280.py
from core.component import Component
from core.pin import PinDirection


class HC280(Component):
    """74HC280 — 9-bit parity generator/checker."""

    def __init__(self):
        super().__init__("74HC280")

        # Inputs A0..A8 (9 bits total)
        for i in range(9):
            self.add_pin(f"A{i}", PinDirection.INPUT)

        # Outputs: even and odd parity
        self.add_pin("EVEN", PinDirection.OUTPUT)
        self.add_pin("ODD", PinDirection.OUTPUT)

    def update(self, tick):
        total = 0
        for i in range(9):
            if self.pins[f"A{i}"].read():
                total ^= 1  # XOR accumulation

        # total == 1 means odd number of 1s
        odd = total
        even = 0 if odd else 1

        self.pins["ODD"].write(odd)
        self.pins["EVEN"].write(even)