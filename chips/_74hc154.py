# 74hc154.py
from core.component import Component
from core.pin import PinDirection


class HC154(Component):
    """74HC154 — 4-to-16 decoder with active LOW outputs."""

    def __init__(self):
        super().__init__("74HC154")

        # Select lines
        self.add_pin("A0", PinDirection.INPUT)
        self.add_pin("A1", PinDirection.INPUT)
        self.add_pin("A2", PinDirection.INPUT)
        self.add_pin("A3", PinDirection.INPUT)

        # Enables (active LOW)
        self.add_pin("G1", PinDirection.INPUT)
        self.add_pin("G2", PinDirection.INPUT)

        # Outputs Y0..Y15
        for i in range(16):
            self.add_pin(f"Y{i}", PinDirection.OUTPUT)

    def update(self, tick):
        g1 = self.pins["G1"].read()
        g2 = self.pins["G2"].read()

        enabled = (g1 == 0 and g2 == 0)

        if not enabled:
            for i in range(16):
                self.pins[f"Y{i}"].write(1)
            return

        sel = (
            ((self.pins["A3"].read() or 0) << 3) |
            ((self.pins["A2"].read() or 0) << 2) |
            ((self.pins["A1"].read() or 0) << 1) |
            (self.pins["A0"].read() or 0)
        )

        for i in range(16):
            self.pins[f"Y{i}"].write(0 if i == sel else 1)