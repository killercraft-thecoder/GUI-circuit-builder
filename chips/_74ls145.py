# 74ls145.py
from core.component import Component
from core.pin import PinDirection


class LS145(Component):
    """74LS145 — BCD to decimal (1-of-10) decoder, active LOW outputs."""

    def __init__(self):
        super().__init__("74LS145")

        for i in range(4):
            self.add_pin(f"A{i}", PinDirection.INPUT)

        for i in range(10):
            self.add_pin(f"Y{i}", PinDirection.OUTPUT)

    def update(self, tick):
        val = 0
        for i in range(4):
            if self.pins[f"A{i}"].read():
                val |= (1 << i)

        for i in range(10):
            self.pins[f"Y{i}"].write(0 if i == val else 1)