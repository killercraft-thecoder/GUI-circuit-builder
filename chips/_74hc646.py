# 74hc646.py
from core.component import Component
from core.pin import PinDirection


class HC646(Component):
    """74HC646 — Bidirectional 8-bit shift register with tri-state outputs."""

    def __init__(self):
        super().__init__("74HC646")

        # Control pins
        self.add_pin("CLK", PinDirection.INPUT)
        self.add_pin("PL", PinDirection.INPUT)   # active LOW
        self.add_pin("OE", PinDirection.INPUT)   # active LOW
        self.add_pin("DIR", PinDirection.INPUT)  # 1 = left, 0 = right

        # Serial inputs
        self.add_pin("SL", PinDirection.INPUT)
        self.add_pin("SR", PinDirection.INPUT)

        # Parallel inputs/outputs
        for i in range(8):
            self.add_pin(f"D{i}", PinDirection.INPUT)
            self.add_pin(f"Q{i}", PinDirection.OUTPUT)

        self.state["reg"] = 0
        self.state["last_clk"] = 0

    def update(self, tick):
        clk = self.pins["CLK"].read() or 0
        pl_n = self.pins["PL"].read()
        oe_n = self.pins["OE"].read()
        dir = self.pins["DIR"].read() or 0
        sl = self.pins["SL"].read() or 0
        sr = self.pins["SR"].read() or 0

        # Parallel load
        if pl_n == 0:
            val = 0
            for i in range(8):
                if self.pins[f"D{i}"].read():
                    val |= (1 << i)
            self.state["reg"] = val

        # Rising-edge shift
        elif self.state["last_clk"] == 0 and clk == 1:
            if dir == 1:
                # Shift left
                new = ((self.state["reg"] << 1) & 0xFE) | (sl & 1)
                self.state["reg"] = new
            else:
                # Shift right
                new = (self.state["reg"] >> 1) | ((sr & 1) << 7)
                self.state["reg"] = new

        self.state["last_clk"] = clk

        # Drive outputs
        for i in range(8):
            if oe_n == 0:
                self.pins[f"Q{i}"].write((self.state["reg"] >> i) & 1)
            else:
                self.pins[f"Q{i}"].write(None)