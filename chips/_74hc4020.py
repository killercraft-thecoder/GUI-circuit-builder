# 74hc4020.py
from core.component import Component
from core.pin import PinDirection


class HC4020(Component):
    """74HC4020 — 14-stage ripple counter."""

    def __init__(self):
        super().__init__("74HC4020")

        self.add_pin("CLK", PinDirection.INPUT)
        self.add_pin("CLR", PinDirection.INPUT)  # active HIGH

        # Outputs Q1..Q14 (Q0 does not exist)
        for i in range(1, 15):
            self.add_pin(f"Q{i}", PinDirection.OUTPUT)

        self.state["count"] = 0
        self.state["last_clk"] = 0

    def update(self, tick):
        clk = self.pins["CLK"].read() or 0
        clr = self.pins["CLR"].read() or 0

        if clr == 1:
            self.state["count"] = 0

        elif self.state["last_clk"] == 0 and clk == 1:
            self.state["count"] = (self.state["count"] + 1) & 0x3FFF  # 14 bits

        self.state["last_clk"] = clk

        for i in range(1, 15):
            self.pins[f"Q{i}"].write((self.state["count"] >> i) & 1)