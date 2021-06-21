import numpy as np
from astropy import units as un
from astropy import constants as const


class Array:
    """
    A short description.

    A bit longer description.

    Args:
        variable (type): description

    Returns:
        type: description

    Raises:
        Exception: description

    """

    def __init__(self, antpos, gains=None, redundant=True):
        """
        A short description.

        A bit longer description.

        Args:
            gains (type): description
        """
        self.antpos = antpos
        self.redundant = redundant
        self.gains = gains

        if redundant:
            pass
