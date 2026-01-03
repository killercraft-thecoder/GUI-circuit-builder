# 74hc4053.py
from core.component import Component
from core.pin import PinDirection


class HC4053(Component):
    """74HC4053 — Triple 2-channel analog switch."""

    def __init__(self):
        super().__init__("74HC4053")

        # Select lines
        self.add_pin("S0", PinDirection.INPUT)
        self.add_pin("S1", PinDirection.INPUT)
        self.add_pin("S2", PinDirection.INPUT)

        # Enable (active LOW)
        self.add_pin("EN", PinDirection.INPUT)

        # Three switches: A, B, C
        for sw in ["A", "B", "C"]:
            self.add_pin(f"{sw}0", PinDirection.INPUT)
            self.add_pin(f"{sw}1", PinDirection.INPUT)
            self.add_pin(f"{sw}OUT", PinDirection.OUTPUT)

    def update(self, tick):
        en = self.pins["EN"].read()

        if en == 1:
            for sw in ["A", "B", "C"]:
                self.pins[f"{sw}OUT"].write(None)
            return

        sels = [
            self.pins["S0"].read() or 0,
            self.pins["S1"].read() or 0,
            self.pins["S2"].read() or 0,
        ]

        for idx, sw in enumerate(["A", "B", "C"]):
            sel = sels[idx]
            val = self.pins[f"{sw}{sel}"].read()
            self.pins[f"{sw}OUT"].write(val)