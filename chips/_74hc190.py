# 74hc190.py
from core.component import Component
from core.pin import PinDirection


class HC190(Component):
    """74HC190 — Up/Down decade counter (0–9)."""

    def __init__(self):
        super().__init__("74HC190")

        self.add_pin("CLK", PinDirection.INPUT)
        self.add_pin("UD", PinDirection.INPUT)    # 1=up, 0=down
        self.add_pin("LOAD", PinDirection.INPUT)  # active LOW

        for i in range(4):
            self.add_pin(f"D{i}", PinDirection.INPUT)
            self.add_pin(f"Q{i}", PinDirection.OUTPUT)

        self.state["count"] = 0
        self.state["last_clk"] = 0

    def update(self, tick):
        clk = self.pins["CLK"].read() or 0
        ud = self.pins["UD"].read() or 0
        load_n = self.pins["LOAD"].read()

        # Parallel load
        if load_n == 0:
            val = 0
            for i in range(4):
                if self.pins[f"D{i}"].read():
                    val |= (1 << i)
            self.state["count"] = val % 10

        # Rising-edge count
        elif self.state["last_clk"] == 0 and clk == 1:
            if ud == 1:
                self.state["count"] += 1
                if self.state["count"] >= 10:
                    self.state["count"] = 0
            else:
                self.state["count"] -= 1
                if self.state["count"] < 0:
                    self.state["count"] = 9

        self.state["last_clk"] = clk

        # Outputs
        for i in range(4):
            self.pins[f"Q{i}"].write((self.state["count"] >> i) & 1)