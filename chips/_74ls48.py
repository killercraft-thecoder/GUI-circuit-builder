# 74ls48.py
from core.component import Component
from core.pin import PinDirection


class LS48(Component):
    """74LS48 — BCD to 7-segment decoder (active HIGH)."""

    def __init__(self):
        super().__init__("74LS48")

        for i in range(4):
            self.add_pin(f"A{i}", PinDirection.INPUT)

        for seg in "abcdefg":
            self.add_pin(seg.upper(), PinDirection.OUTPUT)

        self.seg_table = {
            0: 0b1111110,
            1: 0b0110000,
            2: 0b1101101,
            3: 0b1111001,
            4: 0b0110011,
            5: 0b1011011,
            6: 0b1011111,
            7: 0b1110000,
            8: 0b1111111,
            9: 0b1111011,
        }

    def update(self, tick):
        val = 0
        for i in range(4):
            if self.pins[f"A{i}"].read():
                val |= (1 << i)

        pattern = self.seg_table.get(val, 0)

        for idx, seg in enumerate("abcdefg"):
            bit = (pattern >> idx) & 1
            self.pins[seg.upper()].write(bit)