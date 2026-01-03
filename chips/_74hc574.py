# 74hc574.py
from core.component import Component
from core.pin import PinDirection


class HC574(Component):
    """74HC574 — Octal D-type flip-flop with tri-state outputs."""

    def __init__(self):
        super().__init__("74HC574")

        self.add_pin("CLK", PinDirection.INPUT)
        self.add_pin("OE", PinDirection.INPUT)   # active LOW

        for i in range(8):
            self.add_pin(f"D{i}", PinDirection.INPUT)
            self.add_pin(f"Q{i}", PinDirection.OUTPUT)

        self.state["reg"] = 0
        self.state["last_clk"] = 0

    def update(self, tick):
        clk = self.pins["CLK"].read() or 0
        oe_n = self.pins["OE"].read()

        # Rising edge capture
        if self.state["last_clk"] == 0 and clk == 1:
            val = 0
            for i in range(8):
                if self.pins[f"D{i}"].read():
                    val |= (1 << i)
            self.state["reg"] = val

        self.state["last_clk"] = clk

        # Drive outputs
        for i in range(8):
            if oe_n == 0:
                bit = (self.state["reg"] >> i) & 1
                self.pins[f"Q{i}"].write(bit)
            else:
                self.pins[f"Q{i}"].write(None)