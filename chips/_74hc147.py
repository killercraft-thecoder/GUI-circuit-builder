# _74hc147.py
from core.component import Component
from core.pin import PinDirection


class HC147(Component):
    """74HC147 — 10-to-4 priority encoder (active-LOW inputs, active-LOW outputs)."""

    def __init__(self):
        super().__init__("74HC147")

        for i in range(10):
            self.add_pin(f"I{i}", PinDirection.INPUT)

        for i in range(4):
            self.add_pin(f"A{i}", PinDirection.OUTPUT)

    def update(self, tick):
        # Inputs are active LOW
        active = [i for i in range(10) if (self.pins[f"I{i}"].read() or 1) == 0]

        if not active:
            code = 15  # no input active → outputs HIGH
        else:
            code = max(active)  # highest priority

        # Output is active LOW
        for i in range(4):
            bit = (code >> i) & 1
            self.pins[f"A{i}"].write(0 if bit == 1 else 1)