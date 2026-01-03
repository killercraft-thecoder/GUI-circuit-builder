# _cd4532.py
from core.component import Component
from core.pin import PinDirection


class CD4532(Component):
    """CD4532 — 8-to-3 priority encoder (active-HIGH inputs)."""

    def __init__(self):
        super().__init__("CD4532")

        for i in range(8):
            self.add_pin(f"I{i}", PinDirection.INPUT)

        self.add_pin("EO", PinDirection.OUTPUT) # active HIGH
        self.add_pin("GS", PinDirection.OUTPUT) # active HIGH

        for i in range(3):
            self.add_pin(f"A{i}", PinDirection.OUTPUT)

    def update(self, tick):
        active = [i for i in range(8) if (self.pins[f"I{i}"].read() or 0) == 1]

        if not active:
            code = 0
            eo = 0
            gs = 0
        else:
            code = max(active)
            eo = 1
            gs = 1

        for i in range(3):
            self.pins[f"A{i}"].write((code >> i) & 1)

        self.pins["EO"].write(eo)
        self.pins["GS"].write(gs)