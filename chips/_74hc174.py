# 74hc174.py
from core.component import Component
from core.pin import PinDirection


class HC174(Component):
    """74HC174 — Hex D-type flip-flop with common clock and reset.

    - Six D inputs (D0..D5).
    - Six Q outputs (Q0..Q5).
    - Common clock (CLK), rising-edge triggered.
    - Asynchronous reset (CLR), active LOW.
    """

    def __init__(self):
        super().__init__("74HC174")

        self.add_pin("CLK", PinDirection.INPUT)
        self.add_pin("CLR", PinDirection.INPUT)  # active LOW

        for i in range(6):
            self.add_pin(f"D{i}", PinDirection.INPUT)
            self.add_pin(f"Q{i}", PinDirection.OUTPUT)

        self.state["q"] = [0] * 6
        self.state["last_clk"] = 0

    def update(self, tick):
        clk = self.pins["CLK"].read() or 0
        clr_n = self.pins["CLR"].read()

        # Asynchronous clear (active LOW)
        if clr_n == 0:
            self.state["q"] = [0] * 6
        else:
            # Rising-edge triggered
            if self.state["last_clk"] == 0 and clk == 1:
                new_q = []
                for i in range(6):
                    d = self.pins[f"D{i}"].read() or 0
                    new_q.append(1 if d else 0)
                self.state["q"] = new_q

        self.state["last_clk"] = clk

        # Drive outputs
        for i in range(6):
            self.pins[f"Q{i}"].write(self.state["q"][i])