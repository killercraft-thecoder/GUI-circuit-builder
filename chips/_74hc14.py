# 74hc14.py
from core.component import Component
from core.pin import PinDirection

class HC14(Component):
    """74HC14 — Hex Schmitt-trigger inverter."""

    def __init__(self):
        super().__init__("74HC14")

        for i in range(6):
            self.add_pin(f"A{i}", PinDirection.INPUT)
            self.add_pin(f"Y{i}", PinDirection.OUTPUT)

    def update(self, tick):
        # Digital-only model: behaves like a normal inverter
        for i in range(6):
            a = self.pins[f"A{i}"].read()
            if a in (0, 1):
                self.pins[f"Y{i}"].write(1 - a)