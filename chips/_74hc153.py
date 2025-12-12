# 74hc153.py
from core.component import Component
from core.pin import PinDirection

class HC153(Component):
    """74HC153 — Dual 4-to-1 multiplexer."""

    def __init__(self):
        super().__init__("74HC153")

        # Shared select lines
        self.add_pin("S0", PinDirection.INPUT)
        self.add_pin("S1", PinDirection.INPUT)

        # Two sections: A and B
        for sec in ("A", "B"):
            for i in range(4):
                self.add_pin(f"D{sec}{i}", PinDirection.INPUT)
            self.add_pin(f"Y{sec}", PinDirection.OUTPUT)
            self.add_pin(f"EN{sec}", PinDirection.INPUT)  # active LOW

    def update(self, tick):
        s0 = self.pins["S0"].read() or 0
        s1 = self.pins["S1"].read() or 0
        index = (s1 << 1) | s0

        for sec in ("A", "B"):
            en = self.pins[f"EN{sec}"].read() or 0
            if en == 1:
                self.pins[f"Y{sec}"].write(1)
                continue

            val = self.pins[f"D{sec}{index}"].read()
            self.pins[f"Y{sec}"].write(val)