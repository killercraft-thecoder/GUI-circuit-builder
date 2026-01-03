# 74hc670.py
from core.component import Component
from core.pin import PinDirection


class HC670(Component):
    """74HC670 — 4x4 register file."""

    def __init__(self):
        super().__init__("74HC670")

        # Write address
        self.add_pin("WA0", PinDirection.INPUT)
        self.add_pin("WA1", PinDirection.INPUT)
        self.add_pin("WE", PinDirection.INPUT)   # active LOW

        # Read address
        self.add_pin("RA0", PinDirection.INPUT)
        self.add_pin("RA1", PinDirection.INPUT)

        # Data pins
        for i in range(4):
            self.add_pin(f"D{i}", PinDirection.INPUT)
            self.add_pin(f"Q{i}", PinDirection.OUTPUT)

        # Internal 4x4 storage
        self.state["regs"] = [0, 0, 0, 0]

    def update(self, tick):
        wa = ((self.pins["WA1"].read() or 0) << 1) | (self.pins["WA0"].read() or 0)
        ra = ((self.pins["RA1"].read() or 0) << 1) | (self.pins["RA0"].read() or 0)
        we_n = self.pins["WE"].read()

        # Write (active LOW)
        if we_n == 0:
            val = 0
            for i in range(4):
                if self.pins[f"D{i}"].read():
                    val |= (1 << i)
            self.state["regs"][wa] = val

        # Read
        val = self.state["regs"][ra]
        for i in range(4):
            self.pins[f"Q{i}"].write((val >> i) & 1)