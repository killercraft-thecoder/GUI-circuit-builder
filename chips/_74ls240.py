# 74ls240.py
from core.component import Component
from core.pin import PinDirection


class LS240(Component):
    """74LS240 — Octal inverting buffer/driver."""

    def __init__(self):
        super().__init__("74LS240")

        self.add_pin("OE1", PinDirection.INPUT)  # active LOW
        self.add_pin("OE2", PinDirection.INPUT)  # active LOW

        for i in range(8):
            self.add_pin(f"A{i}", PinDirection.INPUT)
            self.add_pin(f"Y{i}", PinDirection.OUTPUT)

    def update(self, tick):
        oe1 = self.pins["OE1"].read()
        oe2 = self.pins["OE2"].read()

        for i in range(8):
            group = 1 if i < 4 else 2
            oe = oe1 if group == 1 else oe2

            if oe == 1:
                self.pins[f"Y{i}"].write(None)
            else:
                val = self.pins[f"A{i}"].read()
                self.pins[f"Y{i}"].write(0 if val else 1)