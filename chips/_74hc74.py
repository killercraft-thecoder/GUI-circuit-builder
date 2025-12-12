# 74hc74.py
from core.component import Component
from core.pin import PinDirection

class HC74(Component):
    """74HC74 — Dual D flip-flop with set/reset."""

    def __init__(self):
        super().__init__("74HC74")

        for sec in ("A", "B"):
            self.add_pin(f"D{sec}", PinDirection.INPUT)
            self.add_pin(f"CLK{sec}", PinDirection.INPUT)
            self.add_pin(f"SET{sec}", PinDirection.INPUT)   # active LOW
            self.add_pin(f"CLR{sec}", PinDirection.INPUT)   # active LOW
            self.add_pin(f"Q{sec}", PinDirection.OUTPUT)
            self.add_pin(f"nQ{sec}", PinDirection.OUTPUT)

            self.state[f"Q{sec}"] = 0
            self.state[f"last_clk{sec}"] = 0

    def update(self, tick):
        for sec in ("A", "B"):
            clk = self.pins[f"CLK{sec}"].read() or 0
            d = self.pins[f"D{sec}"].read() or 0
            setn = self.pins[f"SET{sec}"].read() or 1
            clrn = self.pins[f"CLR{sec}"].read() or 1

            # Async clear
            if clrn == 0:
                self.state[f"Q{sec}"] = 0
            # Async set
            elif setn == 0:
                self.state[f"Q{sec}"] = 1
            # Rising edge
            elif self.state[f"last_clk{sec}"] == 0 and clk == 1:
                self.state[f"Q{sec}"] = d

            self.state[f"last_clk{sec}"] = clk

            q = self.state[f"Q{sec}"]
            self.pins[f"Q{sec}"].write(q)
            self.pins[f"nQ{sec}"].write(1 - q)