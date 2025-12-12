# 74hc245.py
from core.component import Component
from core.pin import PinDirection

class HC245(Component):
    """74HC245 — 8-bit bidirectional bus transceiver."""

    def __init__(self):
        super().__init__("74HC245")

        # A0–A7 and B0–B7
        for i in range(8):
            self.add_pin(f"A{i}", PinDirection.TRISTATE)
            self.add_pin(f"B{i}", PinDirection.TRISTATE)

        # Direction + Output Enable
        self.add_pin("DIR", PinDirection.INPUT)
        self.add_pin("OE", PinDirection.INPUT)

    def update(self, tick):
        oe = self.pins["OE"].read() or 0
        dir = self.pins["DIR"].read() or 0

        # High-Z when OE = 1
        if oe == 1:
            for i in range(8):
                self.pins[f"A{i}"].write(None)
                self.pins[f"B{i}"].write(None)
            return

        # A → B
        if dir == 1:
            for i in range(8):
                val = self.pins[f"A{i}"].read()
                self.pins[f"B{i}"].write(val)

        # B → A
        else:
            for i in range(8):
                val = self.pins[f"B{i}"].read()
                self.pins[f"A{i}"].write(val)