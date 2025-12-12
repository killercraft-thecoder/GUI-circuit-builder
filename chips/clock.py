# clock.py
from core.component import Component
from core.pin import PinDirection


class Clock(Component):
    """
    Adjustable virtual clock.
    Frequency is in ticks per toggle.
    """

    def __init__(self, frequency=30):
        super().__init__("Clock")
        self.add_pin("OUT", PinDirection.OUTPUT)

        self.state["frequency"] = frequency  # ticks per toggle
        self.state["counter"] = 0
        self.state["level"] = 0  # current output

    def set_frequency(self, freq):
        self.state["frequency"] = max(1, int(freq))

    def update(self, tick):
        self.state["counter"] += 1

        if self.state["counter"] >= self.state["frequency"]:
            self.state["counter"] = 0
            self.state["level"] ^= 1  # toggle

        self.pins["OUT"].write(self.state["level"])