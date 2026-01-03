# _74hc132.py
from core.component import Component
from core.pin import PinDirection


class HC132(Component):
    """74HC132 — Quad 2-input NAND with Schmitt-trigger inputs."""

    def __init__(self):
        super().__init__("74HC132")

        for n in range(1, 5):
            self.add_pin(f"{n}A", PinDirection.INPUT)
            self.add_pin(f"{n}B", PinDirection.INPUT)
            self.add_pin(f"{n}Y", PinDirection.OUTPUT)

    def update(self, tick):
        for n in range(1, 5):
            a = self.pins[f"{n}A"].read() or 0
            b = self.pins[f"{n}B"].read() or 0
            y = 0 if (a == 1 and b == 1) else 1
            self.pins[f"{n}Y"].write(y)