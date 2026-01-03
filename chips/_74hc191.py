# 74hc191.py
from core.component import Component
from core.pin import PinDirection


class HC191(Component):
    """74HC191 — 4-bit synchronous up/down counter.

    - Up/Down controlled by U/D (1 = up, 0 = down)
    - Parallel load (PL, active LOW)
    - Ripple carry output (RC)
    """

    def __init__(self):
        super().__init__("74HC191")

        self.add_pin("CLK", PinDirection.INPUT)
        self.add_pin("PL", PinDirection.INPUT)   # active LOW
        self.add_pin("UD", PinDirection.INPUT)   # 1=up, 0=down

        # Parallel inputs
        for i in range(4):
            self.add_pin(f"D{i}", PinDirection.INPUT)

        # Outputs
        for i in range(4):
            self.add_pin(f"Q{i}", PinDirection.OUTPUT)

        self.add_pin("RC", PinDirection.OUTPUT)  # ripple carry

        self.state["count"] = 0
        self.state["last_clk"] = 0

    def update(self, tick):
        clk = self.pins["CLK"].read() or 0
        pl_n = self.pins["PL"].read()
        ud = self.pins["UD"].read() or 0

        # Parallel load
        if pl_n == 0:
            val = 0
            for i in range(4):
                if self.pins[f"D{i}"].read():
                    val |= (1 << i)
            self.state["count"] = val & 0xF

        # Rising-edge count
        elif self.state["last_clk"] == 0 and clk == 1:
            if ud == 1:
                self.state["count"] = (self.state["count"] + 1) & 0xF
            else:
                self.state["count"] = (self.state["count"] - 1) & 0xF

        self.state["last_clk"] = clk

        # Drive Q outputs
        for i in range(4):
            bit = (self.state["count"] >> i) & 1
            self.pins[f"Q{i}"].write(bit)

        # Ripple carry: HIGH when terminal count reached
        if ud == 1:
            rc = 1 if self.state["count"] == 0xF else 0
        else:
            rc = 1 if self.state["count"] == 0x0 else 0

        self.pins["RC"].write(rc)