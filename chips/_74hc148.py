# _74hc148.py
from core.component import Component
from core.pin import PinDirection


class HC148(Component):
    """74HC148 — 8-to-3 priority encoder (active-LOW)."""

    def __init__(self):
        super().__init__("74HC148")

        for i in range(8):
            self.add_pin(f"I{i}", PinDirection.INPUT)

        self.add_pin("EI", PinDirection.INPUT)  # active LOW
        self.add_pin("EO", PinDirection.OUTPUT) # active LOW
        self.add_pin("GS", PinDirection.OUTPUT) # active LOW

        for i in range(3):
            self.add_pin(f"A{i}", PinDirection.OUTPUT)

    def update(self, tick):
        ei = self.pins["EI"].read() or 0

        if ei == 1:
            # Disabled → outputs HIGH
            for i in range(3):
                self.pins[f"A{i}"].write(1)
            self.pins["EO"].write(1)
            self.pins["GS"].write(1)
            return

        active = [i for i in range(8) if (self.pins[f"I{i}"].read() or 1) == 0]

        if not active:
            code = 7
            eo = 1
            gs = 1
        else:
            code = max(active)
            eo = 0
            gs = 0

        for i in range(3):
            bit = (code >> i) & 1
            self.pins[f"A{i}"].write(0 if bit == 1 else 1)

        self.pins["EO"].write(eo)
        self.pins["GS"].write(gs)