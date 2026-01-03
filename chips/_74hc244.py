# 74hc244.py
from core.component import Component
from core.pin import PinDirection


class HC244(Component):
    """74HC244 — Octal buffer/line driver with 3-state outputs.

    - Inputs:  A0..A7
    - Outputs: Y0..Y7 (non-inverting)
    - Enables: OE1, OE2 (both active LOW)
    - When OE* is HIGH for a group, outputs are high-impedance (None).
    """

    def __init__(self):
        super().__init__("74HC244")

        # Enables (active LOW)
        self.add_pin("OE1", PinDirection.INPUT)
        self.add_pin("OE2", PinDirection.INPUT)

        # A0..A7 inputs, Y0..Y7 outputs
        for i in range(8):
            self.add_pin(f"A{i}", PinDirection.INPUT)
            self.add_pin(f"Y{i}", PinDirection.OUTPUT)

    def update(self, tick):
        oe1 = self.pins["OE1"].read()
        oe2 = self.pins["OE2"].read()

        # Group 1: A0..A3 -> Y0..Y3, controlled by OE1
        for i in range(4):
            if oe1 == 0:
                val = self.pins[f"A{i}"].read()
                self.pins[f"Y{i}"].write(1 if val else 0)
            else:
                # High-impedance when disabled
                self.pins[f"Y{i}"].write(None)

        # Group 2: A4..A7 -> Y4..Y7, controlled by OE2
        for i in range(4, 8):
            if oe2 == 0:
                val = self.pins[f"A{i}"].read()
                self.pins[f"Y{i}"].write(1 if val else 0)
            else:
                self.pins[f"Y{i}"].write(None)