# _74hc01.py
from core.component import Component
from core.pin import PinDirection


class HC01(Component):
    """74HC01 — Quad 2-input NAND with open-collector outputs."""

    def __init__(self):
        super().__init__("74HC01")

        for n in range(1, 5):
            self.add_pin(f"{n}A", PinDirection.INPUT)
            self.add_pin(f"{n}B", PinDirection.INPUT)
            self.add_pin(f"{n}Y", PinDirection.OUTPUT)

    def _nand_oc(self, a, b):
        a = a or 0
        b = b or 0
        # NAND truth
        out = 0 if (a == 1 and b == 1) else 1
        # Open collector: 1 becomes high-Z
        return 0 if out == 0 else None

    def update(self, tick):
        for n in range(1, 5):
            a = self.pins[f"{n}A"].read()
            b = self.pins[f"{n}B"].read()
            self.pins[f"{n}Y"].write(self._nand_oc(a, b))