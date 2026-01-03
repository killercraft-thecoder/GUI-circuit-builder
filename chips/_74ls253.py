# 74ls253.py
from core.component import Component
from core.pin import PinDirection


class LS253(Component):
    """74LS253 — Dual 4-to-1 multiplexer with tri-state outputs."""

    def __init__(self):
        super().__init__("74LS253")

        # Two muxes: A and B
        for mux in ("A", "B"):
            for i in range(4):
                self.add_pin(f"D{mux}{i}", PinDirection.INPUT)
            self.add_pin(f"Y{mux}", PinDirection.OUTPUT)

        self.add_pin("S0", PinDirection.INPUT)
        self.add_pin("S1", PinDirection.INPUT)
        self.add_pin("OE", PinDirection.INPUT)  # active LOW

    def update(self, tick):
        oe_n = self.pins["OE"].read()

        if oe_n == 1:
            self.pins["YA"].write(None)
            self.pins["YB"].write(None)
            return

        sel = (
            ((self.pins["S1"].read() or 0) << 1) |
            (self.pins["S0"].read() or 0)
        )

        for mux in ("A", "B"):
            val = 1 if self.pins[f"D{mux}{sel}"].read() else 0
            self.pins[f"Y{mux}"].write(val)