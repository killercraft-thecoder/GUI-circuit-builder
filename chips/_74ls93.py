# 74ls93.py
from core.component import Component
from core.pin import PinDirection


class LS93(Component):
    """74LS93 — 4-bit ripple counter."""

    def __init__(self):
        super().__init__("74LS93")

        self.add_pin("CLK", PinDirection.INPUT)
        self.add_pin("CLR1", PinDirection.INPUT)  # active HIGH
        self.add_pin("CLR2", PinDirection.INPUT)  # active HIGH

        for i in range(4):
            self.add_pin(f"Q{i}", PinDirection.OUTPUT)

        self.state["count"] = 0
        self.state["last_clk"] = 0

    def update(self, tick):
        clk = self.pins["CLK"].read() or 0
        clr1 = self.pins["CLR1"].read() or 0
        clr2 = self.pins["CLR2"].read() or 0

        if clr1 == 1 and clr2 == 1:
            self.state["count"] = 0

        elif self.state["last_clk"] == 0 and clk == 1:
            self.state["count"] = (self.state["count"] + 1) & 0xF

        self.state["last_clk"] = clk

        for i in range(4):
            self.pins[f"Q{i}"].write((self.state["count"] >> i) & 1)