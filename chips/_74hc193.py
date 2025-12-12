# 74hc193.py
from core.component import Component
from core.pin import PinDirection


class HC193(Component):
    """
    74HC193 — 4-bit up/down counter.
    Pins:
      UPCLK, DOWNCLK
      LOAD, CLR
      D0–D3
      Q0–Q3
      BORROW, CARRY
    """

    def __init__(self):
        super().__init__("74HC193")

        self.add_pin("UPCLK", PinDirection.INPUT)
        self.add_pin("DOWNCLK", PinDirection.INPUT)
        self.add_pin("LOAD", PinDirection.INPUT)
        self.add_pin("CLR", PinDirection.INPUT)

        for i in range(4):
            self.add_pin(f"D{i}", PinDirection.INPUT)
            self.add_pin(f"Q{i}", PinDirection.OUTPUT)

        self.add_pin("CARRY", PinDirection.OUTPUT)
        self.add_pin("BORROW", PinDirection.OUTPUT)

        self.state["count"] = 0
        self.state["last_up"] = 0
        self.state["last_down"] = 0

    def update(self, tick):
        up = self.pins["UPCLK"].read() or 0
        down = self.pins["DOWNCLK"].read() or 0
        load = self.pins["LOAD"].read() or 0
        clr = self.pins["CLR"].read() or 0

        # Async clear
        if clr == 0:
            self.state["count"] = 0

        # Load
        if load == 0:
            val = 0
            for i in range(4):
                bit = self.pins[f"D{i}"].read() or 0
                val |= (bit << i)
            self.state["count"] = val

        # Up count
        if self.state["last_up"] == 0 and up == 1:
            if self.state["count"] == 0xF:
                self.pins["CARRY"].write(1)
            self.state["count"] = (self.state["count"] + 1) & 0xF

        # Down count
        if self.state["last_down"] == 0 and down == 1:
            if self.state["count"] == 0:
                self.pins["BORROW"].write(1)
            self.state["count"] = (self.state["count"] - 1) & 0xF

        self.state["last_up"] = up
        self.state["last_down"] = down

        # Outputs
        for i in range(4):
            self.pins[f"Q{i}"].write((self.state["count"] >> i) & 1)