# 4017.py
from core.component import Component
from core.pin import PinDirection


class CD4017(Component):
    """
    CD4017 decade counter.
    10 outputs Q0–Q9, advances on rising clock.
    """

    def __init__(self):
        super().__init__("4017")

        self.add_pin("CLK", PinDirection.INPUT)
        self.add_pin("RESET", PinDirection.INPUT)

        for i in range(10):
            self.add_pin(f"Q{i}", PinDirection.OUTPUT)

        self.state["count"] = 0
        self.state["last_clk"] = 0

    def update(self, tick):
        clk = self.pins["CLK"].read() or 0
        rst = self.pins["RESET"].read() or 0

        # Reset
        if rst == 1:
            self.state["count"] = 0

        # Rising edge detect
        if self.state["last_clk"] == 0 and clk == 1:
            self.state["count"] = (self.state["count"] + 1) % 10

        self.state["last_clk"] = clk

        # Drive outputs
        for i in range(10):
            self.pins[f"Q{i}"].write(1 if i == self.state["count"] else 0)