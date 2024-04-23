#daemon/printer/__init__.py

from . import printer_controller
from . import printer_commands


def test(printer):
    if printer is not None:
        return True
    return False
