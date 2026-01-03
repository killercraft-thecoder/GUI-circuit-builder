# _74hc148n.py
from core.component import Component
from core.pin import PinDirection


class HC148N(Component):
    """74HC148N — 8-to-3 binary encoder (non-priority)."""

    def __init__(self):
        super().__init__("74HC148N")

        for i in range(8):
            self.add_pin(f"I{i}", PinDirection.INPUT)

        for i in range(3):
            self.add_pin(f"A{i}", PinDirection.OUTPUT)

    def update(self, tick):
        active = [i for i in range(8) if (self.pins[f"I{i}"].read() or 0) == 1]

        if not active:
            code = 0
        else:
            code = max(active)  # non-priority → highest index wins

        for i in range(3):
            self.pins[f"A{i}"].write((code >> i) & 1)