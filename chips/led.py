# led.py
from core.component import Component
from core.pin import PinDirection


class LED(Component):
    """
    Simple LED indicator.
    Reads one input pin.
    """

    def __init__(self):
        super().__init__("LED")
        self.add_pin("IN", PinDirection.INPUT)
        self.state["value"] = 0

    def update(self, tick):
        # Just store the input value for the renderer
        val = self.pins["IN"].read()
        self.state["value"] = val