# _74hc73.py
from core.component import Component
from core.pin import PinDirection


class HC73(Component):
    """74HC73 — Dual JK flip-flop with asynchronous clear (active LOW)."""

    def __init__(self):
        super().__init__("74HC73")

        self.state["Q1"] = 0
        self.state["Q2"] = 0
        self.state["last_clk1"] = 0
        self.state["last_clk2"] = 0

        # FF1
        self.add_pin("1J", PinDirection.INPUT)
        self.add_pin("1K", PinDirection.INPUT)
        self.add_pin("1CLK", PinDirection.INPUT)
        self.add_pin("1CLR", PinDirection.INPUT)
        self.add_pin("1Q", PinDirection.OUTPUT)

        # FF2
        self.add_pin("2J", PinDirection.INPUT)
        self.add_pin("2K", PinDirection.INPUT)
        self.add_pin("2CLK", PinDirection.INPUT)
        self.add_pin("2CLR", PinDirection.INPUT)
        self.add_pin("2Q", PinDirection.OUTPUT)

    def _update_ff(self, n):
        j = self.pins[f"{n}J"].read() or 0
        k = self.pins[f"{n}K"].read() or 0
        clk = self.pins[f"{n}CLK"].read() or 0
        clr = self.pins[f"{n}CLR"].read() or 0

        # Async clear (active LOW)
        if clr == 0:
            self.state[f"Q{n}"] = 0

        # Rising edge
        elif self.state[f"last_clk{n}"] == 0 and clk == 1:
            q = self.state[f"Q{n}"]
            if j == 0 and k == 0:
                pass
            elif j == 1 and k == 0:
                q = 1
            elif j == 0 and k == 1:
                q = 0
            elif j == 1 and k == 1:
                q = 0 if q == 1 else 1
            self.state[f"Q{n}"] = q

        self.state[f"last_clk{n}"] = clk
        self.pins[f"{n}Q"].write(self.state[f"Q{n}"])

    def update(self, tick):
        self._update_ff("1")
        self._update_ff("2")