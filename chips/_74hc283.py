# 74hc283.py
from core.component import Component
from core.pin import PinDirection


class HC283(Component):
    """74HC283 — 4-bit binary adder with carry in/out."""

    def __init__(self):
        super().__init__("74HC283")

        # Inputs A0..A3, B0..B3
        for i in range(4):
            self.add_pin(f"A{i}", PinDirection.INPUT)
            self.add_pin(f"B{i}", PinDirection.INPUT)

        self.add_pin("CIN", PinDirection.INPUT)
        self.add_pin("COUT", PinDirection.OUTPUT)

        # Outputs S0..S3
        for i in range(4):
            self.add_pin(f"S{i}", PinDirection.OUTPUT)

    def update(self, tick):
        a = 0
        b = 0

        for i in range(4):
            if self.pins[f"A{i}"].read():
                a |= (1 << i)
            if self.pins[f"B{i}"].read():
                b |= (1 << i)

        cin = 1 if self.pins["CIN"].read() else 0

        result = a + b + cin
        sum_bits = result & 0xF
        cout = 1 if result > 0xF else 0

        for i in range(4):
            self.pins[f"S{i}"].write((sum_bits >> i) & 1)

        self.pins["COUT"].write(cout)