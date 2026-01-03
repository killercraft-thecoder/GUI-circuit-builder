# 74hc573.py
from core.component import Component
from core.pin import PinDirection


class HC573(Component):
    """74HC573 — Octal transparent latch with tri-state outputs."""

    def __init__(self):
        super().__init__("74HC573")

        self.add_pin("LE", PinDirection.INPUT)   # Latch enable (active HIGH)
        self.add_pin("OE", PinDirection.INPUT)   # Output enable (active LOW)

        for i in range(8):
            self.add_pin(f"D{i}", PinDirection.INPUT)
            self.add_pin(f"Q{i}", PinDirection.OUTPUT)

        self.state["latched"] = 0

    def update(self, tick):
        le = self.pins["LE"].read() or 0
        oe_n = self.pins["OE"].read()

        # Transparent when LE = 1
        if le == 1:
            val = 0
            for i in range(8):
                if self.pins[f"D{i}"].read():
                    val |= (1 << i)
            self.state["latched"] = val

        # Drive outputs
        for i in range(8):
            if oe_n == 0:
                bit = (self.state["latched"] >> i) & 1
                self.pins[f"Q{i}"].write(bit)
            else:
                self.pins[f"Q{i}"].write(None)