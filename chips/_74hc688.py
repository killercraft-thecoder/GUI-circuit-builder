# 74hc688.py
from core.component import Component
from core.pin import PinDirection


class HC688(Component):
    """74HC688 — 8-bit equality comparator.

    - Outputs EQ = 0 when A == B
    - Outputs EQ = 1 when A != B
    """

    def __init__(self):
        super().__init__("74HC688")

        for i in range(8):
            self.add_pin(f"A{i}", PinDirection.INPUT)
            self.add_pin(f"B{i}", PinDirection.INPUT)

        self.add_pin("EQ", PinDirection.OUTPUT)

    def update(self, tick):
        equal = True

        for i in range(8):
            a = 1 if self.pins[f"A{i}"].read() else 0
            b = 1 if self.pins[f"B{i}"].read() else 0
            if a != b:
                equal = False
                break

        # Active LOW equality output
        self.pins["EQ"].write(0 if equal else 1)