# _74hc155.py
from core.component import Component
from core.pin import PinDirection


class HC155(Component):
    """74HC155 — Dual 2-to-4 decoder, active-LOW outputs."""

    def __init__(self):
        super().__init__("74HC155")

        # Decoder 1
        self.add_pin("1A", PinDirection.INPUT)
        self.add_pin("1B", PinDirection.INPUT)
        self.add_pin("1G", PinDirection.INPUT)  # active LOW
        for i in range(4):
            self.add_pin(f"1Y{i}", PinDirection.OUTPUT)

        # Decoder 2
        self.add_pin("2A", PinDirection.INPUT)
        self.add_pin("2B", PinDirection.INPUT)
        self.add_pin("2G", PinDirection.INPUT)  # active LOW
        for i in range(4):
            self.add_pin(f"2Y{i}", PinDirection.OUTPUT)

    def _decode(self, n):
        g = self.pins[f"{n}G"].read() or 0
        a = self.pins[f"{n}A"].read() or 0
        b = self.pins[f"{n}B"].read() or 0

        if g == 1:
            # Disabled → all outputs HIGH
            for i in range(4):
                self.pins[f"{n}Y{i}"].write(1)
            return

        sel = (b << 1) | a

        for i in range(4):
            self.pins[f"{n}Y{i}"].write(0 if i == sel else 1)

    def update(self, tick):
        self._decode("1")
        self._decode("2")