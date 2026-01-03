# 74hc182.py
from core.component import Component
from core.pin import PinDirection


class HC182(Component):
    """74HC182 — Carry lookahead generator for 4-bit adders."""

    def __init__(self):
        super().__init__("74HC182")

        # Group propagate and generate from a 4-bit adder
        self.add_pin("P0", PinDirection.INPUT)
        self.add_pin("P1", PinDirection.INPUT)
        self.add_pin("P2", PinDirection.INPUT)
        self.add_pin("P3", PinDirection.INPUT)

        self.add_pin("G0", PinDirection.INPUT)
        self.add_pin("G1", PinDirection.INPUT)
        self.add_pin("G2", PinDirection.INPUT)
        self.add_pin("G3", PinDirection.INPUT)

        # Carry in / outputs / group signals
        self.add_pin("CIN", PinDirection.INPUT)

        self.add_pin("C1", PinDirection.OUTPUT)
        self.add_pin("C2", PinDirection.OUTPUT)
        self.add_pin("C3", PinDirection.OUTPUT)
        self.add_pin("C4", PinDirection.OUTPUT)

        self.add_pin("GP", PinDirection.OUTPUT)   # Group propagate
        self.add_pin("GG", PinDirection.OUTPUT)   # Group generate

    def update(self, tick):
        p = [1 if self.pins[f"P{i}"].read() else 0 for i in range(4)]
        g = [1 if self.pins[f"G{i}"].read() else 0 for i in range(4)]
        cin = 1 if self.pins["CIN"].read() else 0

        # Standard carry lookahead equations
        c1 = g[0] | (p[0] & cin)
        c2 = g[1] | (p[1] & g[0]) | (p[1] & p[0] & cin)
        c3 = (
            g[2]
            | (p[2] & g[1])
            | (p[2] & p[1] & g[0])
            | (p[2] & p[1] & p[0] & cin)
        )
        c4 = (
            g[3]
            | (p[3] & g[2])
            | (p[3] & p[2] & g[1])
            | (p[3] & p[2] & p[1] & g[0])
            | (p[3] & p[2] & p[1] & p[0] & cin)
        )

        gp = p[3] & p[2] & p[1] & p[0]
        gg = (
            g[3]
            | (p[3] & g[2])
            | (p[3] & p[2] & g[1])
            | (p[3] & p[2] & p[1] & g[0])
        )

        self.pins["C1"].write(1 if c1 else 0)
        self.pins["C2"].write(1 if c2 else 0)
        self.pins["C3"].write(1 if c3 else 0)
        self.pins["C4"].write(1 if c4 else 0)
        self.pins["GP"].write(1 if gp else 0)
        self.pins["GG"].write(1 if gg else 0)