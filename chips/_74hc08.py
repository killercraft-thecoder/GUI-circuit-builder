# 74hc08.py
from core.component import Component
from core.pin import PinDirection


class HC08(Component):
    """
    74HC08 — Quad 2-input AND gates.
    """

    def __init__(self):
        super().__init__("74HC08")

        for g in range(4):
            self.add_pin(f"A{g}", PinDirection.INPUT)
            self.add_pin(f"B{g}", PinDirection.INPUT)
            self.add_pin(f"Y{g}", PinDirection.OUTPUT)

    def update(self, tick):
        for g in range(4):
            a = self.pins[f"A{g}"].read()
            b = self.pins[f"B{g}"].read()
            if a in (0, 1) and b in (0, 1):
                self.pins[f"Y{g}"].write(a & b)