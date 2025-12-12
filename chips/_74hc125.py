# 74hc125.py
from core.component import Component
from core.pin import PinDirection

class HC125(Component):
    """74HC125 — Quad tri-state buffer (active-low OE)."""

    def __init__(self):
        super().__init__("74HC125")

        for i in range(4):
            self.add_pin(f"A{i}", PinDirection.INPUT)
            self.add_pin(f"Y{i}", PinDirection.TRISTATE)
            self.add_pin(f"OE{i}", PinDirection.INPUT)  # active LOW

    def update(self, tick):
        for i in range(4):
            oe = self.pins[f"OE{i}"].read() or 0
            if oe == 1:
                self.pins[f"Y{i}"].write(None)
            else:
                val = self.pins[f"A{i}"].read()
                self.pins[f"Y{i}"].write(val)