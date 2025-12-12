# engine.py
from wire import Wire
from component import Component

class Engine:
    """
    The simulation engine.
    Manages components, wires, and tick updates.
    """

    def __init__(self):
        self.components: list[Component] = []   # list of Component objects
        self.wires: list[Wire] = []        # list of Wire objects
        self.tick_count = 0

    # ---------------------------------------------------------
    # REGISTRATION
    # ---------------------------------------------------------

    def add_component(self, component):
        self.components.append(component)

    def add_wire(self, wire):
        self.wires.append(wire)

    def delete_component(self, comp):
        # Remove wires connected to this component
        wires_to_remove = []
        for wire in self.wires:
            for pin in wire.pins:
                if pin.owner == comp:
                    wires_to_remove.append(wire)
                    break

        for w in wires_to_remove:
            self.wires.remove(w)

        # Remove the component itself
        if comp in self.components:
            self.components.remove(comp)

    # ---------------------------------------------------------
    # SIMULATION LOOP
    # ---------------------------------------------------------

    def tick(self):
        """
        One simulation step:
        1. Resolve all wires
        2. Update all components
        3. Resolve wires again
        """
        self.tick_count += 1

        # First pass: resolve wires
        for wire in self.wires:
            wire.resolve()

        # Update components
        for comp in self.components:
            comp.update(self.tick_count)

        # Second pass: resolve wires again
        for wire in self.wires:
            wire.resolve()

    

    # ---------------------------------------------------------
    # SERIALIZATION
    # ---------------------------------------------------------

    def serialize(self):
        return {
            "components": [c.serialize() for c in self.components],
            "wires": [w.serialize() for w in self.wires],
            "tick": self.tick_count,
        }