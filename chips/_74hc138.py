# 74hc138.py
from core.component import Component
from core.pin import PinDirection

class HC138(Component):
    """74HC138 — 3-to-8 decoder with enables."""

    def __init__(self):
        super().__init__("74HC138")

        # Inputs
        self.add_pin("A0", PinDirection.INPUT)
        self.add_pin("A1", PinDirection.INPUT)
        self.add_pin("A2", PinDirection.INPUT)

        # Enables
        self.add_pin("G1", PinDirection.INPUT)
        self.add_pin("G2A", PinDirection.INPUT)
        self.add_pin("G2B", PinDirection.INPUT)

        # Outputs Y0–Y7
        for i in range(8):
            self.add_pin(f"Y{i}", PinDirection.OUTPUT)

    def update(self, tick):
        g1 = self.pins["G1"].read() or 0
        g2a = self.pins["G2A"].read() or 0
        g2b = self.pins["G2B"].read() or 0

        # Disabled → all HIGH
        if not (g1 == 1 and g2a == 0 and g2b == 0):
            for i in range(8):
                self.pins[f"Y{i}"].write(1)
            return

        # Decode
        a0 = self.pins["A0"].read() or 0
        a1 = self.pins["A1"].read() or 0
        a2 = self.pins["A2"].read() or 0
        index = (a2 << 2) | (a1 << 1) | a0

        for i in range(8):
            self.pins[f"Y{i}"].write(0 if i == index else 1)