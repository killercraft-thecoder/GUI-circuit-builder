# render.py
import pygame
import inspect
from core.component import Component # for type reasons

PIN_RADIUS = 6
FONT_SIZE = 16

MENU_WIDTH = 260
MENU_BG = (45, 45, 45)
MENU_TEXT = (230, 230, 230)
MENU_HIGHLIGHT = (70, 70, 70)

COMP_BG = (80, 80, 80)
COMP_BORDER = (200, 200, 200)

LED_ON = (255, 80, 80)
LED_OFF = (80, 20, 20)
LED_Z = (40, 40, 40)


class Renderer:
    """
    Draws components, wires, and the chip selection menu.
    """

    def __init__(self, engine, screen, chip_classes):
        self.engine = engine
        self.screen = screen
        self.font = pygame.font.SysFont("consolas", FONT_SIZE)

        # Chip menu
        self.chip_classes = chip_classes  # dict: name -> class
        self.menu_scroll = 0
        self.menu_item_height = 80

        # Cached menu rectangles for input handler
        self.menu_hitboxes = []

    # ---------------------------------------------------------
    # MAIN DRAW
    # ---------------------------------------------------------

    def draw(self):
        self.screen.fill((30, 30, 30))

        # Draw menu
        self._draw_menu()

        # Draw wires first (under components)
        for wire in self.engine.wires:
            self._draw_wire(wire)

        # Draw components
        for comp in self.engine.components:
            self._draw_component(comp)

        pygame.display.flip()

    # ---------------------------------------------------------
    # CHIP MENU
    # ---------------------------------------------------------

    def _draw_menu(self):
        pygame.draw.rect(self.screen, MENU_BG, (0, 0, MENU_WIDTH, self.screen.get_height()))

        self.menu_hitboxes = []
        y = -self.menu_scroll

        for name, cls in self.chip_classes.items():
            rect = pygame.Rect(0, y, MENU_WIDTH, self.menu_item_height)

            # Background
            pygame.draw.rect(self.screen, MENU_HIGHLIGHT if rect.collidepoint(pygame.mouse.get_pos()) else MENU_BG, rect)

            # Title
            label = self.font.render(name, True, MENU_TEXT)
            self.screen.blit(label, (10, y + 5))

            # Docstring preview
            doc = inspect.getdoc(cls) or ""
            doc_lines = doc.split("\n")[:3]  # first 3 lines only
            for i, line in enumerate(doc_lines):
                txt = self.font.render(line.strip(), True, (180, 180, 180))
                self.screen.blit(txt, (10, y + 25 + i * 18))

            # Save hitbox
            self.menu_hitboxes.append((rect, cls))

            y += self.menu_item_height

    # ---------------------------------------------------------
    # COMPONENTS
    # ---------------------------------------------------------

    def _draw_component(self, comp:Component):
        x, y = comp.position

        # Auto-size based on pin count
        pin_count = len(comp.pins)
        width = max(200, pin_count * 22)
        height = 70

        rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, COMP_BG, rect, border_radius=6)
        pygame.draw.rect(self.screen, COMP_BORDER, rect, 2, border_radius=6)

        # Label
        label = self.font.render(comp.label, True, (255, 255, 255))
        self.screen.blit(label, (x + 10, y + 10))

        # LED special rendering
        if comp.label == "LED":
            self._draw_led(comp, x, y)
            return

        # Draw pins
        for i, (name, pin) in enumerate(comp.pins.items()):
            px = x + 20 + (i * 22)
            py = y + height - 12

            color = (0,0,0)

            if pin.is_shorted():
                color = (255, 255, 0)
            elif pin.value == 0:
                color = (0, 128, 255)
            elif pin.value == 1:
                color = (255, 0, 0)

            pygame.draw.circle(self.screen, color, (px, py), PIN_RADIUS)

            # Store for picking
            pin.screen_pos = (px, py)

            font = pygame.font.SysFont(None, 12)   # very small font
            text_surf = font.render(name, True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=(px, py - 8))
            self.screen.blit(text_surf, text_rect)


    # ---------------------------------------------------------
    # LED RENDERING
    # ---------------------------------------------------------

    def _draw_led(self, comp, x, y):
        val = comp.state.get("value", None)

        if val == 1:
            color = LED_ON
        elif val == 0:
            color = LED_OFF
        else:
            color = LED_Z

        pygame.draw.circle(self.screen, color, (x + 35, y + 35), 20)

        # Label
        label = self.font.render("LED", True, (255, 255, 255))
        self.screen.blit(label, (x + 65, y + 25))

        # Pin position
        pin = comp.pins["IN"]
        pin.screen_pos = (x + 35, y + 65)

        pygame.draw.circle(self.screen, (255, 255, 255), pin.screen_pos, PIN_RADIUS)

    # ---------------------------------------------------------
    # WIRES
    # ---------------------------------------------------------

    def _draw_wire(self, wire):
        if wire.short:
            color = (255, 255, 0)
        elif wire.value == 1:
            color = (255, 0, 0)
        elif wire.value == 0:
            color = (0, 128, 255)
        else:
            color = (0, 0, 0)

        points = [pin.screen_pos for pin in wire.pins if hasattr(pin, "screen_pos")]
        if len(points) >= 2:
            pygame.draw.lines(self.screen, color, False, points, 3)

    # ---------------------------------------------------------
    # PICKING (for input.py)
    # ---------------------------------------------------------

    def pick_at(self, pos):
        mx, my = pos

        # Check pins first
        for comp in self.engine.components:
            for pin in comp.pins.values():
                if hasattr(pin, "screen_pos"):
                    px, py = pin.screen_pos
                    if (mx - px)**2 + (my - py)**2 <= PIN_RADIUS**2:
                        return comp, pin

        # Check components
        for comp in self.engine.components:
            x, y = comp.position
            width = max(120, len(comp.pins) * 12)
            height = 70
            rect = pygame.Rect(x, y, width, height)
            if rect.collidepoint(pos):
                return comp, None

        return None, None

    def pick_wire_at(self, pos):
        mx, my = pos

        # Simple distance-to-line check
        for wire in self.engine.wires:
            (x1, y1) = wire.pins[0].get_screen_pos()
            (x2, y2) = wire.pins[1].get_screen_pos()

            # Distance from point to line segment
            # Using bounding box first for speed
            if not (min(x1, x2) - 4 <= mx <= max(x1, x2) + 4 and
                    min(y1, y2) - 4 <= my <= max(y1, y2) + 4):
                continue

            # Now do precise distance check
            # Line parametric projection
            dx = x2 - x1
            dy = y2 - y1
            if dx == 0 and dy == 0:
                continue

            t = ((mx - x1) * dx + (my - y1) * dy) / (dx*dx + dy*dy)
            t = max(0, min(1, t))

            px = x1 + t * dx
            py = y1 + t * dy

            dist2 = (mx - px)**2 + (my - py)**2
            if dist2 <= 16:  # within 4px
                return wire

        return None

    # ---------------------------------------------------------
    # MENU PICKING
    # ---------------------------------------------------------

    def pick_menu(self, pos):
        mx, my = pos
        if mx > MENU_WIDTH:
            return None

        for rect, cls in self.menu_hitboxes:
            if rect.collidepoint((mx, my)):
                return cls

        return None