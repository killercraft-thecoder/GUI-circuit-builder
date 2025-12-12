# 74hc85.py
from core.component import Component
from core.pin import PinDirection

class HC85(Component):
    """74HC85 — 4-bit magnitude comparator."""

    def __init__(self):
        super().__init__("74HC85")

        # A0–A3, B0–B3
        for i in range(4):
            self.add_pin(f"A{i}", PinDirection.INPUT)
            self.add_pin(f"B{i}", PinDirection.INPUT)

        # Cascade inputs
        self.add_pin("LTin", PinDirection.INPUT)
        self.add_pin("EQin", PinDirection.INPUT)
        self.add_pin("GTin", PinDirection.INPUT)

        # Outputs
        self.add_pin("LT", PinDirection.OUTPUT)
        self.add_pin("EQ", PinDirection.OUTPUT)
        self.add_pin("GT", PinDirection.OUTPUT)

    def update(self, tick):
        a = 0
        b = 0
        for i in range(4):
            ai = self.pins[f"A{i}"].read() or 0
            bi = self.pins[f"B{i}"].read() or 0
            a |= ai << i
            b |= bi << i

        lt = a < b
        eq = a == b
        gt = a > b

        # Cascade logic
        if eq:
            lt = self.pins["LTin"].read() or 0
            gt = self.pins["GTin"].read() or 0
            eq = self.pins["EQin"].read() or 0

        self.pins["LT"].write(1 if lt else 0)
        self.pins["EQ"].write(1 if eq else 0)
        self.pins["GT"].write(1 if gt else 0)