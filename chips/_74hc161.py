# 74hc161.py
from core.component import Component
from core.pin import PinDirection


class HC161(Component):
    """
    74HC161 — 4-bit synchronous binary counter.
    Pins:
      CLK, CLR, LOAD, ENP, ENT
      D0–D3 inputs
      Q0–Q3 outputs
      RCO (ripple carry)
    """

    def __init__(self):
        super().__init__("74HC161")

        self.add_pin("CLK", PinDirection.INPUT)
        self.add_pin("CLR", PinDirection.INPUT)
        self.add_pin("LOAD", PinDirection.INPUT)
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
        clr = self.pins["CLR"].read() or 0
        load = self.pins["LOAD"].read() or 0
        enp = self.pins["ENP"].read() or 0
        ent = self.pins["ENT"].read() or 0

        # Asynchronous clear
        if clr == 0:
            self.state["count"] = 0

        # Rising edge
        if self.state["last_clk"] == 0 and clk == 1:
            if load == 0:
                # Load D inputs
                val = 0
                for i in range(4):
                    bit = self.pins[f"D{i}"].read() or 0
                    val |= (bit << i)
                self.state["count"] = val
            elif enp == 1 and ent == 1:
                self.state["count"] = (self.state["count"] + 1) & 0xF

        self.state["last_clk"] = clk

        # Outputs
        for i in range(4):
            self.pins[f"Q{i}"].write((self.state["count"] >> i) & 1)

        # Ripple carry
        self.pins["RCO"].write(1 if (self.state["count"] == 0xF and ent == 1) else 0)