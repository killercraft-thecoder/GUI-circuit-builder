# 74hc4017.py
from core.component import Component
from core.pin import PinDirection


class HC4017(Component):
    """74HC4017 — Decade counter with 10 decoded outputs."""

    def __init__(self):
        super().__init__("74HC4017")

        self.add_pin("CLK", PinDirection.INPUT)
        self.add_pin("RESET", PinDirection.INPUT)  # active HIGH

        for i in range(10):
            self.add_pin(f"Q{i}", PinDirection.OUTPUT)

        self.state["count"] = 0
        self.state["last_clk"] = 0

    def update(self, tick):
        clk = self.pins["CLK"].read() or 0
        rst = self.pins["RESET"].read() or 0

        if rst == 1:
            self.state["count"] = 0

        elif self.state["last_clk"] == 0 and clk == 1:
            self.state["count"] = (self.state["count"] + 1) % 10

        self.state["last_clk"] = clk

        for i in range(10):
            self.pins[f"Q{i}"].write(1 if i == self.state["count"] else 0)