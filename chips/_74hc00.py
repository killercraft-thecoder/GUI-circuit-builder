# 74hc00.py
from core.component import Component
from core.pin import PinDirection


class HC00(Component):
    """
    74HC00 — Quad 2-input NAND gates.
    """

    def __init__(self):
        super().__init__("74HC00")

        for g in range(4):
            self.add_pin(f"A{g}", PinDirection.INPUT)
            self.add_pin(f"B{g}", PinDirection.INPUT)
            self.add_pin(f"Y{g}", PinDirection.OUTPUT)

    def update(self, tick):
        for g in range(4):
            a = self.pins[f"A{g}"].read()
            b = self.pins[f"B{g}"].read()
            if a in (0, 1) and b in (0, 1):
                self.pins[f"Y{g}"].write(0 if (a & b) else 1)