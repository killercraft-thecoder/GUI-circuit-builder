# _74hc259.py
from core.component import Component
from core.pin import PinDirection


class HC259(Component):
    """74HC259 — 8-bit addressable latch."""

    def __init__(self):
        super().__init__("74HC259")

        # Address pins
        self.add_pin("A0", PinDirection.INPUT)
        self.add_pin("A1", PinDirection.INPUT)
        self.add_pin("A2", PinDirection.INPUT)

        # Data + control
        self.add_pin("D", PinDirection.INPUT)
        self.add_pin("WE", PinDirection.INPUT)   # active HIGH
        self.add_pin("CLR", PinDirection.INPUT)  # active LOW

        # Outputs Q0..Q7
        for i in range(8):
            self.add_pin(f"Q{i}", PinDirection.OUTPUT)

        # Internal storage
        self.state["bits"] = [0] * 8

    def update(self, tick):
        clr = self.pins["CLR"].read() or 0
        we  = self.pins["WE"].read() or 0

        if clr == 0:
            # Active-low clear
            self.state["bits"] = [0] * 8
        else:
            # Decode address
            a0 = self.pins["A0"].read() or 0
            a1 = self.pins["A1"].read() or 0
            a2 = self.pins["A2"].read() or 0
            addr = (a2 << 2) | (a1 << 1) | a0

            if we == 1:
                d = self.pins["D"].read() or 0
                self.state["bits"][addr] = 1 if d == 1 else 0

        # Drive outputs
        for i in range(8):
            self.pins[f"Q{i}"].write(self.state["bits"][i])