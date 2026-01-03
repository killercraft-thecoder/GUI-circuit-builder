# _74hc30.py
from core.component import Component
from core.pin import PinDirection


class HC30(Component):
    """74HC30 — 8-input NAND gate."""

    def __init__(self):
        super().__init__("74HC30")

        for pin in ["A","B","C","D","E","F","G","H"]:
            self.add_pin(pin, PinDirection.INPUT)

        self.add_pin("Y", PinDirection.OUTPUT)

    def update(self, tick):
        # Treat None as 0 (floating = low)
        inputs = [(self.pins[p].read() or 0) for p in ["A","B","C","D","E","F","G","H"]]

        # NAND: output = 0 only if ALL inputs are 1
        y = 0 if all(v == 1 for v in inputs) else 1

        self.pins["Y"].write(y)