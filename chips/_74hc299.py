# 74hc299.py
from core.component import Component
from core.pin import PinDirection


class HC299(Component):
    """74HC299 — Universal 8-bit shift register."""

    def __init__(self):
        super().__init__("74HC299")

        # Control pins
        self.add_pin("CLK", PinDirection.INPUT)
        self.add_pin("PL", PinDirection.INPUT)   # active LOW
        self.add_pin("OE", PinDirection.INPUT)   # active LOW
        self.add_pin("S0", PinDirection.INPUT)
        self.add_pin("S1", PinDirection.INPUT)

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
        s0 = self.pins["S0"].read() or 0
        s1 = self.pins["S1"].read() or 0
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
            mode = (s1 << 1) | s0

            if mode == 0b00:
                pass  # Hold
            elif mode == 0b01:
                # Shift right
                new = (self.state["reg"] >> 1) | ((sr & 1) << 7)
                self.state["reg"] = new & 0xFF
            elif mode == 0b10:
                # Shift left
                new = ((self.state["reg"] << 1) & 0xFE) | (sl & 1)
                self.state["reg"] = new & 0xFF
            elif mode == 0b11:
                # Parallel load (redundant)
                val = 0
                for i in range(8):
                    if self.pins[f"D{i}"].read():
                        val |= (1 << i)
                self.state["reg"] = val

        self.state["last_clk"] = clk

        # Drive outputs
        for i in range(8):
            if oe_n == 0:
                self.pins[f"Q{i}"].write((self.state["reg"] >> i) & 1)
            else:
                self.pins[f"Q{i}"].write(None)