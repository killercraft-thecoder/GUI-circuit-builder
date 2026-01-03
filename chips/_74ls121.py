# 74ls121.py
from core.component import Component
from core.pin import PinDirection


class LS121(Component):
    """74LS121 — Monostable one-shot (digital pulse generator)."""

    def __init__(self):
        super().__init__("74LS121")

        self.add_pin("TRIG", PinDirection.INPUT)
        self.add_pin("CLR", PinDirection.INPUT)   # active LOW
        self.add_pin("Q", PinDirection.OUTPUT)

        self.state["last_trig"] = 0
        self.state["pulse"] = 0
        self.state["remaining"] = 0

        self.PULSE_WIDTH = 5  # digital ticks

    def update(self, tick):
        trig = self.pins["TRIG"].read() or 0
        clr = self.pins["CLR"].read() or 1

        if clr == 0:
            self.state["pulse"] = 0
            self.state["remaining"] = 0
        else:
            if self.state["last_trig"] == 0 and trig == 1:
                self.state["pulse"] = 1
                self.state["remaining"] = self.PULSE_WIDTH

            if self.state["remaining"] > 0:
                self.state["remaining"] -= 1
                if self.state["remaining"] == 0:
                    self.state["pulse"] = 0

        self.state["last_trig"] = trig
        self.pins["Q"].write(self.state["pulse"])