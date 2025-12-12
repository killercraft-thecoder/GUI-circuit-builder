# input.py
import pygame
from core.wire import Wire


class InputHandler:
    """
    Handles all mouse/keyboard input for the GUI.
    Responsibilities:
      - Chip menu selection
      - Adding new components
      - Selecting pins
      - Creating wires
      - Dragging components
      - Toggling switches/buttons
      - Scrolling the menu
    """

    def __init__(self, engine, renderer):
        self.engine = engine
        self.renderer = renderer

        self.dragging_component = None
        self.drag_offset = (0, 0)

        self.selected_pin = None
        self.placing_component_class = None  # class selected from menu

    # ---------------------------------------------------------
    # MAIN EVENT HANDLER
    # ---------------------------------------------------------

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self._mouse_down(event.pos)
            elif event.button == 3:
                self._right_click(event.pos)
            elif event.button == 4:
                self.renderer.menu_scroll = max(0, self.renderer.menu_scroll - 30)
            elif event.button == 5:
                self.renderer.menu_scroll += 30

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self._mouse_up(event.pos)

        elif event.type == pygame.MOUSEMOTION:
            self._mouse_move(event.pos)

    # ---------------------------------------------------------
    # MOUSE DOWN
    # ---------------------------------------------------------

    def _mouse_down(self, pos):
        mx, my = pos

        # 1. Check if clicked inside the chip menu
        chip_class = self.renderer.pick_menu(pos)
        if chip_class:
            self.placing_component_class = chip_class
            return

        # 2. If a chip is selected from menu → place it
        if self.placing_component_class:
            comp = self.placing_component_class()
            comp.position = (mx, my)
            self.engine.add_component(comp)
            self.placing_component_class = None
            return

        # 3. Check if clicked a pin
        comp, pin = self.renderer.pick_at(pos)
        if pin:
            self._handle_pin_click(pin)
            return

        # 4. Check if clicked a component body
        if comp:
            self._start_drag(comp, pos)
            self._handle_component_click(comp)
            return
        
    def _right_click(self, pos):
        # Check for wire first
        wire = self.renderer.pick_wire_at(pos)
        if wire:
            self.engine.delete_wire(wire)
            return

        # Then check for component
        comp, pin = self.renderer.pick_at(pos)
        if comp:
            self.engine.delete_component(comp)
            return

        # Otherwise do nothing
        return

    # ---------------------------------------------------------
    # PIN CLICK → WIRE CREATION
    # ---------------------------------------------------------

    def _handle_pin_click(self, pin):
        if self.selected_pin is None:
            self.selected_pin = pin
        else:
            # Create wire between pins
            wire = Wire()
            wire.connect_pin(self.selected_pin)
            wire.connect_pin(pin)
            self.engine.add_wire(wire)
            self.selected_pin = None

    # ---------------------------------------------------------
    # COMPONENT CLICK → BUTTON/SWITCH LOGIC
    # ---------------------------------------------------------

    def _handle_component_click(self, comp):
        label = comp.label.upper()

        # Button → press
        if label == "BUTTON":
            comp.press()

        # Switch → toggle
        if label == "SWITCH":
            comp.toggle()

    # ---------------------------------------------------------
    # START DRAGGING
    # ---------------------------------------------------------

    def _start_drag(self, comp, pos):
        self.dragging_component = comp
        cx, cy = comp.position
        mx, my = pos
        self.drag_offset = (cx - mx, cy - my)

    # ---------------------------------------------------------
    # MOUSE UP
    # ---------------------------------------------------------

    def _mouse_up(self, pos):
        # Release button
        if self.dragging_component:
            label = self.dragging_component.label.upper()
            if label == "BUTTON":
                self.dragging_component.release()

        self.dragging_component = None

    # ---------------------------------------------------------
    # MOUSE MOVE
    # ---------------------------------------------------------

    def _mouse_move(self, pos):
        if self.dragging_component:
            mx, my = pos
            ox, oy = self.drag_offset
            self.dragging_component.position = (mx + ox, my + oy)