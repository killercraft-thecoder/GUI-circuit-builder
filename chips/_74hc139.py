# 74hc139.py
from core.component import Component
from core.pin import PinDirection

class HC139(Component):
    """74HC139 — Dual 2-to-4 decoder."""

    def __init__(self):
        super().__init__("74HC139")

        # Two sections: A and B
        for sec in ("A", "B"):
            self.add_pin(f"{sec}0", PinDirection.INPUT)
            self.add_pin(f"{sec}1", PinDirection.INPUT)
            self.add_pin(f"EN{sec}", PinDirection.INPUT)

            for i in range(4):
                self.add_pin(f"Y{sec}{i}", PinDirection.OUTPUT)

    def update(self, tick):
        for sec in ("A", "B"):
            en = self.pins[f"EN{sec}"].read() or 0

            if en == 1:
                # Disabled → all HIGH
                for i in range(4):
                    self.pins[f"Y{sec}{i}"].write(1)
                continue

            a0 = self.pins[f"{sec}0"].read() or 0
            a1 = self.pins[f"{sec}1"].read() or 0
            index = (a1 << 1) | a0

            for i in range(4):
                self.pins[f"Y{sec}{i}"].write(0 if i == index else 1)