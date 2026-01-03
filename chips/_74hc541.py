# 74hc541.py
from core.component import Component
from core.pin import PinDirection


class HC541(Component):
    """74HC541 — Octal buffer/line driver with 3-state outputs.

    - Inputs:  A0..A7
    - Outputs: Y0..Y7
    - Enables: OE1, OE2 (both active LOW)
    """

    def __init__(self):
        super().__init__("74HC541")

        self.add_pin("OE1", PinDirection.INPUT)  # active LOW
        self.add_pin("OE2", PinDirection.INPUT)

        for i in range(8):
            self.add_pin(f"A{i}", PinDirection.INPUT)
            self.add_pin(f"Y{i}", PinDirection.OUTPUT)

    def update(self, tick):
        oe1 = self.pins["OE1"].read()
        oe2 = self.pins["OE2"].read()

        # Group 1: A0..A3
        for i in range(4):
            if oe1 == 0:
                val = self.pins[f"A{i}"].read()
                self.pins[f"Y{i}"].write(1 if val else 0)
            else:
                self.pins[f"Y{i}"].write(None)

        # Group 2: A4..A7
        for i in range(4, 8):
            if oe2 == 0:
                val = self.pins[f"A{i}"].read()
                self.pins[f"Y{i}"].write(1 if val else 0)
            else:
                self.pins[f"Y{i}"].write(None)