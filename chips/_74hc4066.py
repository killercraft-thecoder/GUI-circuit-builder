# 74hc4066.py
from core.component import Component
from core.pin import PinDirection

class HC4066(Component):
    """74HC4066 — Quad analog switch (digital model)."""

    def __init__(self):
        super().__init__("74HC4066")

        for i in range(4):
            self.add_pin(f"A{i}", PinDirection.TRISTATE)
            self.add_pin(f"B{i}", PinDirection.TRISTATE)
            self.add_pin(f"EN{i}", PinDirection.INPUT)

    def update(self, tick):
        for i in range(4):
            en = self.pins[f"EN{i}"].read() or 0

            if en == 1:
                # Pass A → B and B → A
                a = self.pins[f"A{i}"].read()
                b = self.pins[f"B{i}"].read()

                # If one side is driven, drive the other
                if a in (0, 1):
                    self.pins[f"B{i}"].write(a)
                if b in (0, 1):
                    self.pins[f"A{i}"].write(b)
            else:
                # High-Z both sides
                self.pins[f"A{i}"].write(None)
                self.pins[f"B{i}"].write(None)