# _74hc05.py
from core.component import Component
from core.pin import PinDirection


class HC05(Component):
    """74HC05 — Hex inverter with open-drain outputs."""

    def __init__(self):
        super().__init__("74HC05")

        for n in range(1, 7):
            self.add_pin(f"A{n}", PinDirection.INPUT)
            self.add_pin(f"Y{n}", PinDirection.OUTPUT)

    def update(self, tick):
        for n in range(1, 7):
            a = self.pins[f"A{n}"].read() or 0
            # Inverter: out = NOT a
            out = 0 if a == 1 else 1
            # Open drain: 1 becomes high-Z
            self.pins[f"Y{n}"].write(0 if out == 0 else None)