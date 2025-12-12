# 74hc4060.py
from core.component import Component
from core.pin import PinDirection

class HC4060(Component):
    """74HC4060 — Oscillator + 14-stage counter (digital-only model)."""

    def __init__(self):
        super().__init__("74HC4060")

        # External clock input (digital model)
        self.add_pin("CLK", PinDirection.INPUT)
        self.add_pin("RESET", PinDirection.INPUT)  # active HIGH

        # Outputs Q4–Q13 (10 outputs)
        for i in range(4, 14):
            self.add_pin(f"Q{i}", PinDirection.OUTPUT)

        self.state["count"] = 0
        self.state["last_clk"] = 0

    def update(self, tick):
        clk = self.pins["CLK"].read() or 0
        rst = self.pins["RESET"].read() or 0

        if rst == 1:
            self.state["count"] = 0
        else:
            if self.state["last_clk"] == 0 and clk == 1:
                self.state["count"] = (self.state["count"] + 1) & 0x3FFF

        self.state["last_clk"] = clk

        for i in range(4, 14):
            bit = (self.state["count"] >> i) & 1
            self.pins[f"Q{i}"].write(bit)