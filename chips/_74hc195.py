# 74hc195.py
from core.component import Component
from core.pin import PinDirection


class HC195(Component):
    """74HC195 — Universal 4-bit shift register.

    Features:
    - Parallel load (active LOW)
    - Shift left or right
    - Serial inputs: SL (left), SR (right)
    - Hold mode
    - Asynchronous master reset (MR, active LOW)
    """

    def __init__(self):
        super().__init__("74HC195")

        # Control pins
        self.add_pin("CLK", PinDirection.INPUT)
        self.add_pin("MR", PinDirection.INPUT)   # active LOW
        self.add_pin("PL", PinDirection.INPUT)   # parallel load, active LOW
        self.add_pin("S0", PinDirection.INPUT)   # mode select
        self.add_pin("S1", PinDirection.INPUT)

        # Serial inputs
        self.add_pin("SL", PinDirection.INPUT)   # shift-left input
        self.add_pin("SR", PinDirection.INPUT)   # shift-right input

        # Parallel inputs and outputs
        for i in range(4):
            self.add_pin(f"D{i}", PinDirection.INPUT)
            self.add_pin(f"Q{i}", PinDirection.OUTPUT)

        self.state["reg"] = 0
        self.state["last_clk"] = 0

    def update(self, tick):
        clk = self.pins["CLK"].read() or 0
        mr_n = self.pins["MR"].read()
        pl_n = self.pins["PL"].read()
        s0 = self.pins["S0"].read() or 0
        s1 = self.pins["S1"].read() or 0
        sl = self.pins["SL"].read() or 0
        sr = self.pins["SR"].read() or 0

        # Asynchronous master reset
        if mr_n == 0:
            self.state["reg"] = 0

        else:
            # Parallel load (active LOW)
            if pl_n == 0:
                val = 0
                for i in range(4):
                    if self.pins[f"D{i}"].read():
                        val |= (1 << i)
                self.state["reg"] = val

            # Rising-edge clock
            elif self.state["last_clk"] == 0 and clk == 1:
                mode = (s1 << 1) | s0

                if mode == 0b00:
                    pass  # Hold
                elif mode == 0b01:
                    # Shift right
                    new = (self.state["reg"] >> 1) | ((sr & 1) << 3)
                    self.state["reg"] = new & 0xF
                elif mode == 0b10:
                    # Shift left
                    new = ((self.state["reg"] << 1) & 0xE) | (sl & 1)
                    self.state["reg"] = new & 0xF
                elif mode == 0b11:
                    # Parallel load (redundant)
                    val = 0
                    for i in range(4):
                        if self.pins[f"D{i}"].read():
                            val |= (1 << i)
                    self.state["reg"] = val

        self.state["last_clk"] = clk

        # Drive outputs
        for i in range(4):
            bit = (self.state["reg"] >> i) & 1
            self.pins[f"Q{i}"].write(bit)