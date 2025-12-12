# 74hc157.py
from core.component import Component
from core.pin import PinDirection

class HC157(Component):
    """74HC157 — Quad 2-to-1 multiplexer."""

    def __init__(self):
        super().__init__("74HC157")

        # Select + Enable
        self.add_pin("SEL", PinDirection.INPUT)
        self.add_pin("EN", PinDirection.INPUT)  # active LOW

        # Inputs A0–A3, B0–B3, outputs Y0–Y3
        for i in range(4):
            self.add_pin(f"A{i}", PinDirection.INPUT)
            self.add_pin(f"B{i}", PinDirection.INPUT)
            self.add_pin(f"Y{i}", PinDirection.OUTPUT)

    def update(self, tick):
        sel = self.pins["SEL"].read() or 0
        en = self.pins["EN"].read() or 0

        for i in range(4):
            if en == 1:
                self.pins[f"Y{i}"].write(1)  # disabled → HIGH
                continue

            if sel == 0:
                val = self.pins[f"A{i}"].read()
            else:
                val = self.pins[f"B{i}"].read()

            self.pins[f"Y{i}"].write(val)