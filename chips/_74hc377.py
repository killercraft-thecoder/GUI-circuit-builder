# _74hc377.py
from core.component import Component
from core.pin import PinDirection


class HC377(Component):
    """74HC377 — Octal D flip-flop with enable."""

    def __init__(self):
        super().__init__("74HC377")

        self.state["Q"] = [0] * 8
        self.state["last_clk"] = 0

        self.add_pin("CLK", PinDirection.INPUT)
        self.add_pin("EN", PinDirection.INPUT)

        for i in range(8):
            self.add_pin(f"D{i}", PinDirection.INPUT)
            self.add_pin(f"Q{i}", PinDirection.OUTPUT)

    def update(self, tick):
        clk = self.pins["CLK"].read() or 0
        en = self.pins["EN"].read() or 0

        # Rising edge
        if self.state["last_clk"] == 0 and clk == 1:
            if en == 1:
                for i in range(8):
                    self.state["Q"][i] = 1 if (self.pins[f"D{i}"].read() or 0) == 1 else 0

        self.state["last_clk"] = clk

        for i in range(8):
            self.pins[f"Q{i}"].write(self.state["Q"][i])