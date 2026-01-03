# 74hc164.py
from core.component import Component
from core.pin import PinDirection


class HC164(Component):
    """74HC164 — 8-bit serial-in parallel-out shift register.

    - Serial inputs A and B are ANDed.
    - Asynchronous clear (CLR), active LOW.
    - Data is shifted on the rising edge of CLK.
    """

    def __init__(self):
        super().__init__("74HC164")

        # Control pins
        self.add_pin("CLK", PinDirection.INPUT)
        self.add_pin("CLR", PinDirection.INPUT)  # active LOW

        # Serial inputs
        self.add_pin("A", PinDirection.INPUT)
        self.add_pin("B", PinDirection.INPUT)

        # Parallel outputs Q0..Q7
        for i in range(8):
            self.add_pin(f"Q{i}", PinDirection.OUTPUT)

        self.state["reg"] = 0
        self.state["last_clk"] = 0

    def update(self, tick):
        clk = self.pins["CLK"].read() or 0
        clr_n = self.pins["CLR"].read()
        a = self.pins["A"].read() or 0
        b = self.pins["B"].read() or 0

        # Asynchronous clear (active LOW)
        if clr_n == 0:
            self.state["reg"] = 0
        else:
            # Rising-edge triggered shift
            if self.state["last_clk"] == 0 and clk == 1:
                new_bit = 1 if (a and b) else 0
                self.state["reg"] = ((self.state["reg"] << 1) | new_bit) & 0xFF

        self.state["last_clk"] = clk

        # Drive outputs
        for i in range(8):
            bit = (self.state["reg"] >> i) & 1
            self.pins[f"Q{i}"].write(bit)