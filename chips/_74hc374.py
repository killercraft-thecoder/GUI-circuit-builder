# _74hc374.py
from core.component import Component
from core.pin import PinDirection


class HC374(Component):
    """74HC374 — Octal D flip-flop with tri-state outputs."""

    def __init__(self):
        super().__init__("74HC374")

        self.state["Q"] = [0] * 8
        self.state["last_clk"] = 0

        self.add_pin("CLK", PinDirection.INPUT)
        self.add_pin("OE", PinDirection.INPUT)  # active LOW

        for i in range(8):
            self.add_pin(f"D{i}", PinDirection.INPUT)
            self.add_pin(f"Q{i}", PinDirection.OUTPUT)

    def update(self, tick):
        clk = self.pins["CLK"].read() or 0
        oe = self.pins["OE"].read() or 0

        # Rising edge
        if self.state["last_clk"] == 0 and clk == 1:
            for i in range(8):
                self.state["Q"][i] = 1 if (self.pins[f"D{i}"].read() or 0) == 1 else 0

        self.state["last_clk"] = clk

        # Drive or tri-state
        for i in range(8):
            if oe == 1:
                self.pins[f"Q{i}"].write(None)
            else:
                self.pins[f"Q{i}"].write(self.state["Q"][i])