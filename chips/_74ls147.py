# 74ls147.py
from core.component import Component
from core.pin import PinDirection


class LS147(Component):
    """74LS147 — 10-to-4 priority encoder (active LOW)."""

    def __init__(self):
        super().__init__("74LS147")

        for i in range(10):
            self.add_pin(f"I{i}", PinDirection.INPUT)

        for i in range(4):
            self.add_pin(f"A{i}", PinDirection.OUTPUT)

    def update(self, tick):
        code = 0b1111  # default inactive

        for i in range(10):
            if self.pins[f"I{i}"].read() == 0:
                code = (~i) & 0xF
                break

        for bit in range(4):
            self.pins[f"A{bit}"].write((code >> bit) & 1)