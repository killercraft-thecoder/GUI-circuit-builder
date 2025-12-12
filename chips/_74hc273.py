# 74hc273.py
from core.component import Component
from core.pin import PinDirection

class HC273(Component):
    """74HC273 — 8-bit register with clear."""

    def __init__(self):
        super().__init__("74HC273")

        self.add_pin("CLK", PinDirection.INPUT)
        self.add_pin("CLR", PinDirection.INPUT)  # active LOW

        for i in range(8):
            self.add_pin(f"D{i}", PinDirection.INPUT)
            self.add_pin(f"Q{i}", PinDirection.OUTPUT)
            self.state[f"Q{i}"] = 0

        self.state["last_clk"] = 0

    def update(self, tick):
        clk = self.pins["CLK"].read() or 0
        clr = self.pins["CLR"].read() or 1

        if clr == 0:
            for i in range(8):
                self.state[f"Q{i}"] = 0
        else:
            if self.state["last_clk"] == 0 and clk == 1:
                for i in range(8):
                    d = self.pins[f"D{i}"].read() or 0
                    self.state[f"Q{i}"] = d

        self.state["last_clk"] = clk

        for i in range(8):
            q = self.state[f"Q{i}"]
            self.pins[f"Q{i}"].write(q)