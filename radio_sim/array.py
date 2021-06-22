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

    def __init__(self, antpos, gains=None, redundant=True, nfreqs=1024):
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

        if gains:
            self.gains = gains

        else:
            self.gains = {key: np.ones(nfreqs) for key in self.antpos.keys()}

    def __repr__(self):
        """
        A short description.

        A bit longer description.

        Args:
            variable (type): description

        Returns:
            type: description
        """
        return str(gains)
