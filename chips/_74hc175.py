# 74hc175.py
from core.component import Component
from core.pin import PinDirection

class HC175(Component):
    """74HC175 — Quad D flip-flop."""

    def __init__(self):
        super().__init__("74HC175")

        self.add_pin("CLK", PinDirection.INPUT)
        self.add_pin("CLR", PinDirection.INPUT)  # active LOW

        for i in range(4):
            self.add_pin(f"D{i}", PinDirection.INPUT)
            self.add_pin(f"Q{i}", PinDirection.OUTPUT)
            self.add_pin(f"nQ{i}", PinDirection.OUTPUT)
            self.state[f"Q{i}"] = 0

        self.state["last_clk"] = 0

    def update(self, tick):
        clk = self.pins["CLK"].read() or 0
        clr = self.pins["CLR"].read() or 1

        if clr == 0:
            for i in range(4):
                self.state[f"Q{i}"] = 0
        else:
            if self.state["last_clk"] == 0 and clk == 1:
                for i in range(4):
                    d = self.pins[f"D{i}"].read() or 0
                    self.state[f"Q{i}"] = d

        self.state["last_clk"] = clk

        for i in range(4):
            q = self.state[f"Q{i}"]
            self.pins[f"Q{i}"].write(q)
            self.pins[f"nQ{i}"].write(1 - q)