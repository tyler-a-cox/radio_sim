import numpy as np
from astropy import units as un
from itertools import combinations
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

    def __init__(
        self,
        antpos,
        gains=None,
        redundant=True,
        nfreqs=1024,
        tsys=15,
        tint=10,
        noise=False,
    ):
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

        if noise:
            self.tsys = tsys
            self.tint = tint

            # TODO: implement the radiometer equation
            self.noise = ...

        else:
            self.noise = {
                k: np.zeros(nfreqs) for k in combinations(self.antpos.keys(), 2)
            }

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

    def __add__(self, array):
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

        keys = set(list(array.antpos.keys()) + list(self.antpos.keys()))
        antpos = {}
        for k in keys:
            a, b = self.antpos.get(k), array.antpos.get(k)
            if a and b:
                antpos["arr0_{}".format(k)] = a
                antpos["arr1_{}".format(k)] = b

            elif a:
                antpos[k] = a

            elif b:
                antpos[k] = b

        class_vars = {k: v for k, v in self.__dict__.items() if k is not "antpos"}
        return Array(antpos, **class_vars)

    def __repr__(self):
        """ """
        return str(self.antpos)
