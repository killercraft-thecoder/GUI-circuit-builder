# _74hc4069.py
from core.component import Component
from core.pin import PinDirection


class HC4069(Component):
    """74HC4069 — Hex inverter (unbuffered)."""

    def __init__(self):
        super().__init__("74HC4069")

        for n in range(1, 7):
            self.add_pin(f"A{n}", PinDirection.INPUT)
            self.add_pin(f"Y{n}", PinDirection.OUTPUT)

    def update(self, tick):
        for n in range(1, 7):
            a = self.pins[f"A{n}"].read() or 0
            self.pins[f"Y{n}"].write(0 if a == 1 else 1)