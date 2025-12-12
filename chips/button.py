# button.py
from core.component import Component
from core.pin import PinDirection


class Button(Component):
    """
    Momentary push button.
    Output is HIGH only while pressed.
    """

    def __init__(self):
        super().__init__("Button")
        self.add_pin("OUT", PinDirection.OUTPUT)
        self.state["pressed"] = False

    def press(self):
        self.state["pressed"] = True

    def release(self):
        self.state["pressed"] = False

    def update(self, tick):
        self.pins["OUT"].write(1 if self.state["pressed"] else 0)