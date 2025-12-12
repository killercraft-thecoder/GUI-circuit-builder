# 74hc165.py
from core.component import Component
from core.pin import PinDirection


class HC165(Component):
    """
    74HC165 — Parallel-in, Serial-out shift register.
    Pins:
      D0–D7 (inputs)
      CLK, SH_LD (inputs)
      QH (output)
    """

    def __init__(self):
        super().__init__("74HC165")

        for i in range(8):
            self.add_pin(f"D{i}", PinDirection.INPUT)

        self.add_pin("CLK", PinDirection.INPUT)
        self.add_pin("SH_LD", PinDirection.INPUT)
        self.add_pin("QH", PinDirection.OUTPUT)

        self.state["shift"] = [0] * 8
        self.state["last_clk"] = 0

    def update(self, tick):
        clk = self.pins["CLK"].read() or 0
        shld = self.pins["SH_LD"].read() or 0

        # Load parallel data when SH_LD = 0
        if shld == 0:
            for i in range(8):
                bit = self.pins[f"D{i}"].read()
                if bit in (0, 1):
                    self.state["shift"][7 - i] = bit

        # Shift on rising edge
        if self.state["last_clk"] == 0 and clk == 1 and shld == 1:
            self.state["shift"] = [0] + self.state["shift"][:-1]

        self.state["last_clk"] = clk

        self.pins["QH"].write(self.state["shift"][0])