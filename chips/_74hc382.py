# 74hc382.py
from core.component import Component
from core.pin import PinDirection


class HC382(Component):
    """74HC382 — 4-bit ALU (variant)."""

    def __init__(self):
        super().__init__("74HC382")

        # Operand inputs
        for i in range(4):
            self.add_pin(f"A{i}", PinDirection.INPUT)
            self.add_pin(f"B{i}", PinDirection.INPUT)

        # Function select
        for i in range(4):
            self.add_pin(f"S{i}", PinDirection.INPUT)

        self.add_pin("CIN", PinDirection.INPUT)

        # Outputs
        for i in range(4):
            self.add_pin(f"F{i}", PinDirection.OUTPUT)

        self.add_pin("COUT", PinDirection.OUTPUT)

    def update(self, tick):
        a = 0
        b = 0
        for i in range(4):
            if self.pins[f"A{i}"].read():
                a |= (1 << i)
            if self.pins[f"B{i}"].read():
                b |= (1 << i)

        s = 0
        for i in range(4):
            if self.pins[f"S{i}"].read():
                s |= (1 << i)

        cin = 1 if self.pins["CIN"].read() else 0

        # Simple mapping: use S to choose arithmetic/logical combos
        if s == 0x0:
            result = a + b + cin
        elif s == 0x1:
            result = a + (~b & 0xF) + cin
        elif s == 0x2:
            result = (a ^ b) + cin
        elif s == 0x3:
            result = (a & b) + cin
        elif s == 0x4:
            result = (a | b) + cin
        elif s == 0x5:
            result = a - b + cin
        elif s == 0x6:
            result = b - a + cin
        else:
            result = 0

        f = result & 0xF
        cout = 1 if result > 0xF or result < 0 else 0

        for i in range(4):
            self.pins[f"F{i}"].write((f >> i) & 1)
        self.pins["COUT"].write(cout)