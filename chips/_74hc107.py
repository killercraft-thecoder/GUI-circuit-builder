# 74hc107.py
from core.component import Component
from core.pin import PinDirection


class HC107(Component):
    """74HC107 — Dual JK flip-flop with clear."""

    def __init__(self):
        super().__init__("74HC107")

        for n in [0, 1]:
            self.add_pin(f"J{n}", PinDirection.INPUT)
            self.add_pin(f"K{n}", PinDirection.INPUT)
            self.add_pin(f"CLK{n}", PinDirection.INPUT)
            self.add_pin(f"CLR{n}", PinDirection.INPUT)  # active LOW
            self.add_pin(f"Q{n}", PinDirection.OUTPUT)

        self.state["q"] = [0, 0]
        self.state["last_clk"] = [0, 0]

    def update(self, tick):
        for n in [0, 1]:
            clk = self.pins[f"CLK{n}"].read() or 0
            clr_n = self.pins[f"CLR{n}"].read()
            j = self.pins[f"J{n}"].read() or 0
            k = self.pins[f"K{n}"].read() or 0

            # Asynchronous clear
            if clr_n == 0:
                self.state["q"][n] = 0

            # Rising-edge triggered JK
            elif self.state["last_clk"][n] == 0 and clk == 1:
                if j == 0 and k == 0:
                    pass
                elif j == 0 and k == 1:
                    self.state["q"][n] = 0
                elif j == 1 and k == 0:
                    self.state["q"][n] = 1
                elif j == 1 and k == 1:
                    self.state["q"][n] ^= 1

            self.state["last_clk"][n] = clk
            self.pins[f"Q{n}"].write(self.state["q"][n])