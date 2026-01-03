# 74hc163.py
from core.component import Component
from core.pin import PinDirection


class HC163(Component):
    """74HC163 — 4-bit synchronous binary counter."""

    def __init__(self):
        super().__init__("74HC163")

        self.add_pin("CLK", PinDirection.INPUT)
        self.add_pin("CLR", PinDirection.INPUT)  # active LOW
        self.add_pin("LOAD", PinDirection.INPUT) # active LOW
        self.add_pin("ENP", PinDirection.INPUT)
        self.add_pin("ENT", PinDirection.INPUT)

        for i in range(4):
            self.add_pin(f"D{i}", PinDirection.INPUT)
            self.add_pin(f"Q{i}", PinDirection.OUTPUT)

        self.add_pin("RCO", PinDirection.OUTPUT)

        self.state["count"] = 0
        self.state["last_clk"] = 0

    def update(self, tick):
        clk = self.pins["CLK"].read() or 0
        clr_n = self.pins["CLR"].read()
        load_n = self.pins["LOAD"].read()
        enp = self.pins["ENP"].read() or 0
        ent = self.pins["ENT"].read() or 0

        # Asynchronous clear
        if clr_n == 0:
            self.state["count"] = 0

        # Parallel load
        elif load_n == 0:
            val = 0
            for i in range(4):
                if self.pins[f"D{i}"].read():
                    val |= (1 << i)
            self.state["count"] = val

        # Rising-edge count
        elif self.state["last_clk"] == 0 and clk == 1:
            if enp and ent:
                self.state["count"] = (self.state["count"] + 1) & 0xF

        self.state["last_clk"] = clk

        # Drive outputs
        for i in range(4):
            self.pins[f"Q{i}"].write((self.state["count"] >> i) & 1)

        # Ripple carry out
        self.pins["RCO"].write(1 if (self.state["count"] == 0xF and ent) else 0)