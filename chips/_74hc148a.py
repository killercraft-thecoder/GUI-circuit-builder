# _74hc148a.py
from core.component import Component
from core.pin import PinDirection


class HC148A(Component):
    """74HC148A — 8-to-3 priority encoder (active-HIGH enable variant)."""

    def __init__(self):
        super().__init__("74HC148A")

        for i in range(8):
            self.add_pin(f"I{i}", PinDirection.INPUT)

        self.add_pin("EI", PinDirection.INPUT)  # active HIGH
        self.add_pin("EO", PinDirection.OUTPUT) # active HIGH
        self.add_pin("GS", PinDirection.OUTPUT) # active HIGH

        for i in range(3):
            self.add_pin(f"A{i}", PinDirection.OUTPUT)

    def update(self, tick):
        ei = self.pins["EI"].read() or 0

        if ei == 0:
            # Disabled → outputs LOW
            for i in range(3):
                self.pins[f"A{i}"].write(0)
            self.pins["EO"].write(0)
            self.pins["GS"].write(0)
            return

        active = [i for i in range(8) if (self.pins[f"I{i}"].read() or 0) == 1]

        if not active:
            code = 7
            eo = 0
            gs = 0
        else:
            code = max(active)
            eo = 1
            gs = 1

        for i in range(3):
            bit = (code >> i) & 1
            self.pins[f"A{i}"].write(bit)

        self.pins["EO"].write(eo)
        self.pins["GS"].write(gs)