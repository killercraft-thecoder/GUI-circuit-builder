# _74hc11.py
from core.component import Component
from core.pin import PinDirection


class HC11(Component):
    """74HC11 — Triple 3-input AND gate."""

    def __init__(self):
        super().__init__("74HC11")

        # Gate 1
        self.add_pin("1A", PinDirection.INPUT)
        self.add_pin("1B", PinDirection.INPUT)
        self.add_pin("1C", PinDirection.INPUT)
        self.add_pin("1Y", PinDirection.OUTPUT)

        # Gate 2
        self.add_pin("2A", PinDirection.INPUT)
        self.add_pin("2B", PinDirection.INPUT)
        self.add_pin("2C", PinDirection.INPUT)
        self.add_pin("2Y", PinDirection.OUTPUT)

        # Gate 3
        self.add_pin("3A", PinDirection.INPUT)
        self.add_pin("3B", PinDirection.INPUT)
        self.add_pin("3C", PinDirection.INPUT)
        self.add_pin("3Y", PinDirection.OUTPUT)

    def _and3(self, a, b, c):
        a = a or 0
        b = b or 0
        c = c or 0
        return 1 if (a == 1 and b == 1 and c == 1) else 0

    def update(self, tick):
        # Gate 1
        y1 = self._and3(
            self.pins["1A"].read(),
            self.pins["1B"].read(),
            self.pins["1C"].read(),
        )
        self.pins["1Y"].write(y1)

        # Gate 2
        y2 = self._and3(
            self.pins["2A"].read(),
            self.pins["2B"].read(),
            self.pins["2C"].read(),
        )
        self.pins["2Y"].write(y2)

        # Gate 3
        y3 = self._and3(
            self.pins["3A"].read(),
            self.pins["3B"].read(),
            self.pins["3C"].read(),
        )
        self.pins["3Y"].write(y3)