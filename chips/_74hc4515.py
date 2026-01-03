# _74hc4515.py
from core.component import Component
from core.pin import PinDirection


class HC4515(Component):
    """74HC4515 — 4-to-16 decoder with latch, active-LOW outputs."""

    def __init__(self):
        super().__init__("74HC4515")

        for i in range(4):
            self.add_pin(f"A{i}", PinDirection.INPUT)

        self.add_pin("ST", PinDirection.INPUT)
        self.add_pin("EN", PinDirection.INPUT)  # active HIGH

        for i in range(16):
            self.add_pin(f"Y{i}", PinDirection.OUTPUT)

        self.state["latched"] = 0
        self.state["last_st"] = 0

    def update(self, tick):
        st = self.pins["ST"].read() or 0
        en = self.pins["EN"].read() or 0

        # Latch on falling edge
        if self.state["last_st"] == 1 and st == 0:
            a0 = self.pins["A0"].read() or 0
            a1 = self.pins["A1"].read() or 0
            a2 = self.pins["A2"].read() or 0
            a3 = self.pins["A3"].read() or 0
            self.state["latched"] = (a3 << 3) | (a2 << 2) | (a1 << 1) | a0

        self.state["last_st"] = st

        if en == 0:
            # Disabled → all outputs HIGH
            for i in range(16):
                self.pins[f"Y{i}"].write(1)
            return

        # Active → one output LOW
        for i in range(16):
            self.pins[f"Y{i}"].write(0 if i == self.state["latched"] else 1)