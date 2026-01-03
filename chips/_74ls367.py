# 74ls367.py
from core.component import Component
from core.pin import PinDirection


class LS367(Component):
    """74LS367 — Hex buffer/driver with tri-state outputs."""

    def __init__(self):
        super().__init__("74LS367")

        # Two groups with separate enables
        self.add_pin("OE1", PinDirection.INPUT)  # active LOW
        self.add_pin("OE2", PinDirection.INPUT)  # active LOW

        for i in range(6):
            self.add_pin(f"A{i}", PinDirection.INPUT)
            self.add_pin(f"Y{i}", PinDirection.OUTPUT)

    def update(self, tick):
        oe1 = self.pins["OE1"].read()
        oe2 = self.pins["OE2"].read()

        for i in range(6):
            group = 1 if i < 3 else 2
            oe = oe1 if group == 1 else oe2

            if oe == 1:
                self.pins[f"Y{i}"].write(None)
            else:
                val = 1 if self.pins[f"A{i}"].read() else 0
                self.pins[f"Y{i}"].write(val)