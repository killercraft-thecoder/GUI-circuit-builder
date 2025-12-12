# switch.py
from core.component import Component
from core.pin import PinDirection


class Switch(Component):
    """
    Toggle switch.
    Output stays HIGH or LOW until toggled.
    """

    def __init__(self):
        super().__init__("Switch")
        self.add_pin("OUT", PinDirection.OUTPUT)
        self.state["on"] = False

    def toggle(self):
        self.state["on"] = not self.state["on"]

    def update(self, tick):
        self.pins["OUT"].write(1 if self.state["on"] else 0)