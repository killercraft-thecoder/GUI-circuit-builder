# _74hc20.py
from core.component import Component
from core.pin import PinDirection


class HC20(Component):
    """74HC20 — Dual 4-input NAND gate."""

    def __init__(self):
        super().__init__("74HC20")

        # Gate 1
        self.add_pin("1A", PinDirection.INPUT)
        self.add_pin("1B", PinDirection.INPUT)
        self.add_pin("1C", PinDirection.INPUT)
        self.add_pin("1D", PinDirection.INPUT)
        self.add_pin("1Y", PinDirection.OUTPUT)

        # Gate 2
        self.add_pin("2A", PinDirection.INPUT)
        self.add_pin("2B", PinDirection.INPUT)
        self.add_pin("2C", PinDirection.INPUT)
        self.add_pin("2D", PinDirection.INPUT)
        self.add_pin("2Y", PinDirection.OUTPUT)

    def _nand4(self, a, b, c, d):
        a = a or 0
        b = b or 0
        c = c or 0
        d = d or 0
        return 0 if (a == 1 and b == 1 and c == 1 and d == 1) else 1

    def update(self, tick):
        # Gate 1
        y1 = self._nand4(
            self.pins["1A"].read(),
            self.pins["1B"].read(),
            self.pins["1C"].read(),
            self.pins["1D"].read(),
        )
        self.pins["1Y"].write(y1)

        # Gate 2
        y2 = self._nand4(
            self.pins["2A"].read(),
            self.pins["2B"].read(),
            self.pins["2C"].read(),
            self.pins["2D"].read(),
        )
        self.pins["2Y"].write(y2)