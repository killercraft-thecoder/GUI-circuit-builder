# 74ls47.py
from core.component import Component
from core.pin import PinDirection


class LS47(Component):
    """74LS47 — BCD to 7-segment decoder/driver (active LOW outputs)."""

    def __init__(self):
        super().__init__("74LS47")

        for i in range(4):
            self.add_pin(f"A{i}", PinDirection.INPUT)

        # Outputs: a..g (active LOW)
        for seg in "abcdefg":
            self.add_pin(seg.upper(), PinDirection.OUTPUT)

        self.seg_table = {
            0: 0b0000001,
            1: 0b1001111,
            2: 0b0010010,
            3: 0b0000110,
            4: 0b1001100,
            5: 0b0100100,
            6: 0b0100000,
            7: 0b0001111,
            8: 0b0000000,
            9: 0b0000100,
        }

    def update(self, tick):
        val = 0
        for i in range(4):
            if self.pins[f"A{i}"].read():
                val |= (1 << i)

        pattern = self.seg_table.get(val, 0b1111111)

        for idx, seg in enumerate("abcdefg"):
            bit = (pattern >> idx) & 1
            self.pins[seg.upper()].write(bit)