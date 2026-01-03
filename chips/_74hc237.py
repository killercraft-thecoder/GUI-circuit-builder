# 74hc237.py
from core.component import Component
from core.pin import PinDirection


class HC237(Component):
    """74HC237 — 3-to-8 decoder with address latch."""

    def __init__(self):
        super().__init__("74HC237")

        # Address inputs
        self.add_pin("A0", PinDirection.INPUT)
        self.add_pin("A1", PinDirection.INPUT)
        self.add_pin("A2", PinDirection.INPUT)

        # Latch enable (active HIGH)
        self.add_pin("LE", PinDirection.INPUT)

        # Enables
        self.add_pin("G1", PinDirection.INPUT)
        self.add_pin("G2A", PinDirection.INPUT)
        self.add_pin("G2B", PinDirection.INPUT)

        for i in range(8):
            self.add_pin(f"Y{i}", PinDirection.OUTPUT)

        self.state["latched"] = 0

    def update(self, tick):
        le = self.pins["LE"].read() or 0

        # Latch address when LE = 1
        if le == 1:
            sel = (
                ((self.pins["A2"].read() or 0) << 2) |
                ((self.pins["A1"].read() or 0) << 1) |
                (self.pins["A0"].read() or 0)
            )
            self.state["latched"] = sel

        g1 = self.pins["G1"].read()
        g2a = self.pins["G2A"].read()
        g2b = self.pins["G2B"].read()

        enabled = (g1 == 1 and g2a == 0 and g2b == 0)

        if not enabled:
            for i in range(8):
                self.pins[f"Y{i}"].write(0)
            return

        sel = self.state["latched"]

        for i in range(8):
            self.pins[f"Y{i}"].write(1 if i == sel else 0)