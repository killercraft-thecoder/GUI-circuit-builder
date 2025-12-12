# 74hc373.py
from core.component import Component
from core.pin import PinDirection


class HC373(Component):
    """
    74HC373 — 8-bit transparent latch.
    Inputs: D0–D7
    Outputs: Q0–Q7
    Control: LE (Latch Enable), OE (Output Enable)
    """

    def __init__(self):
        super().__init__("74HC373")

        # Inputs
        for i in range(8):
            self.add_pin(f"D{i}", PinDirection.INPUT)

        # Outputs (tri-state)
        for i in range(8):
            self.add_pin(f"Q{i}", PinDirection.TRISTATE)

        self.add_pin("LE", PinDirection.INPUT)
        self.add_pin("OE", PinDirection.INPUT)

        # Internal latch
        self.state["latch"] = [0] * 8

    def update(self, tick):
        le = self.pins["LE"].read()
        oe = self.pins["OE"].read()

        # Transparent when LE = HIGH
        if le == 1:
            for i in range(8):
                bit = self.pins[f"D{i}"].read()
                if bit in (0, 1):
                    self.state["latch"][i] = bit

        # Output enable
        if oe == 0:
            for i in range(8):
                self.pins[f"Q{i}"].write(self.state["latch"][i])
        else:
            for i in range(8):
                self.pins[f"Q{i}"].write(None)