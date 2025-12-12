# Contributing to GUI‑circuit‑builder

Thanks for your interest in contributing!  
This project is an open‑source digital logic simulator with a modular engine, GUI, and chip library.  
Contributions of all kinds are welcome — code, documentation, bug reports, and new chips.

---

## How to Contribute

1. Fork the repository  
2. Create a feature branch  
3. Make your changes  
4. Test the simulator (`python main.py`)  
5. Submit a pull request with a clear description

Small, focused PRs are easier to review.

---

## Project Structure
core/      → engine, pins, wires, components
chips/     → individual IC implementations
gui/       → renderer + input handler
main.py    → application entry point


---

## Coding Guidelines

- Use clear, readable Python  
- Follow existing patterns (Component → pins → update())  
- Keep chips self‑contained  
- Avoid global state  
- Use docstrings (shown in the GUI menu)  
- Use 4‑space indentation

---

## Adding a New Chip

1. Create a file in `chips/`  
2. Inherit from `Component`  
3. Add pins in `__init__()`  
4. Implement `update(self, tick)`  
5. Add the chip to the registry in `main.py`  
6. Include a short docstring describing the chip

Example:

```python
from core.component import Component
from core.pin import PinDirection

class HC245(Component):
    """74HC245 — 8‑bit bus transceiver."""
    def __init__(self):
        super().__init__("74HC245")
        # add pins here
```

Reporting Issues
When opening an issue, include:
• 	What you expected
• 	What happened
• 	Steps to reproduce
• 	OS + Python version
• 	Screenshots if GUI‑related

Feature Requests
Feature ideas are welcome.
Please describe:
• 	The use case
• 	How it should work
• 	Any relevant examples or diagrams

License
By contributing, you agree that your contributions are licensed under the MIT License.
Thanks for helping improve GUI‑circuit‑builder!
