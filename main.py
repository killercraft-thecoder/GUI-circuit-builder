# main.py
import pygame
import sys

from core.engine import Engine
from gui.render import Renderer
from gui.input import InputHandler

# Import chips
from chips.button import Button
from chips.switch import Switch
from chips.led import LED
from chips.clock import Clock
from chips.ne555 import NE555
from chips._28c16 import AT28C16  
from chips._6116 import SRAM6116  
from chips._4017 import CD4017    
from chips._74hc373 import HC373  
from chips._74ls181 import LS181
from chips._74hc165 import HC165
from chips._74hc595 import HC595
from chips._74hc00 import HC00
from chips._74hc08 import HC08
from chips._74hc32 import HC32
from chips._74hc161 import HC161
from chips._74hc193 import HC193


def build_chip_registry():
    """
    Returns a dict: label -> class
    Used by the renderer menu and input handler.
    """
    return {
        "Button": Button,
        "Switch": Switch,
        "LED": LED,
        "Clock": Clock,
        "NE555": NE555,
        "28C16 EEPROM": AT28C16,
        "6116 SRAM": SRAM6116,
        "4017 Decade Counter": CD4017,
        "74HC373 Latch": HC373,
        "74LS181 ALU": LS181,
        "74HC165 PISO": HC165,
        "74HC595 SIPO": HC595,
        "74HC00 NAND": HC00,
        "74HC08 AND": HC08,
        "74HC32 OR": HC32,
        "74HC161 Counter": HC161,
        "74HC193 Up/Down Counter": HC193,
    }


def main():
    pygame.init()
    pygame.display.set_caption("Logic Simulator")

    screen_width = 1280
    screen_height = 720
    screen = pygame.display.set_mode((screen_width, screen_height))

    clock = pygame.time.Clock()

    engine = Engine()
    chip_registry = build_chip_registry()
    renderer = Renderer(engine, screen, chip_registry)
    input_handler = InputHandler(engine, renderer)

    running = True

    # Simulation speed: number of engine ticks per second
    sim_fps = 60

    while running:
        # -----------------------------
        # EVENT HANDLING
        # -----------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

            input_handler.handle_event(event)

        # -----------------------------
        # SIMULATION TICK
        # -----------------------------
        engine.tick()

        # -----------------------------
        # RENDER
        # -----------------------------
        renderer.draw()

        # -----------------------------
        # FRAME LIMIT
        # -----------------------------
        clock.tick(sim_fps)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()