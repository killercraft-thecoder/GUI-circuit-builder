# 74ls148.py
from core.component import Component
from core.pin import PinDirection


class LS148(Component):
    """74LS148 — 8-to-3 priority encoder (active LOW)."""

    def __init__(self):
        super().__init__("74LS148")

        for i in range(8):
            self.add_pin(f"I{i}", PinDirection.INPUT)

        for i in range(3):
            self.add_pin(f"A{i}", PinDirection.OUTPUT)

        self.add_pin("GS", PinDirection.OUTPUT)
        self.add_pin("EO", PinDirection.OUTPUT)

    def update(self, tick):
        code = 0b111
        any_active = False

        for i in range(8):
            if self.pins[f"I{i}"].read() == 0:
                code = (~i) & 0b111
                any_active = True
                break

        for bit in range(3):
            self.pins[f"A{bit}"].write((code >> bit) & 1)

        self.pins["GS"].write(0 if any_active else 1)
        self.pins["EO"].write(0 if any_active else 1)