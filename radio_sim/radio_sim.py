import numpy as np
import matplotlib.pyplot as plt
from scipy.special import j1
from astropy import units as un
from astropy import constants as const
from scipy.interpolate import interp1d
import aipy

from beams import beam_gaussian

from tqdm import tqdm
from hera_cal.redcal import get_pos_reds

from multiprocessing import Pool


class RadioSim:
    """
    Class for simulating radio visibilities
    """

    def __init__(self, antpos, beam, sky, theta, phi, nu):
        """ """
        self.antpos = antpos
        self.beam = beam
        self.sky = sky
        self.theta = theta
        self.phi = phi
        self.nu = nu

        self.uv = {}

        for i, vi in self.antpos.items():
            for j, vj in self.antpos.items():
                if i != j and self.uv.get((j, i)):
                    self.uv[(i, j)] = vj - vi

        self.delays = {k: self.tau(b, theta, phi) for k, v in self.uv.items()}

    def tau(self, b, theta, phi):
        """
        Solves for the delay

        b : np.ndarray, (3,)
            baseline vector

        theta : np.
        """
        bx, by, bz = b * un.m
        l, m, n = (
            np.cos(theta) * np.sin(phi),
            np.cos(theta) * np.cos(phi),
            np.sin(theta),
        )
        return (bx * l + by * m + bz * n) / const.c

    def simulate(self):
        """
        Simulate visibilities using the Radio Interferometry Measurement Equation (RIME)

        Parameters
        ----------
        sources : np.ndarray
            Array containing the flux density of sources

        theta : np.ndarray
            Beam position of sources

        delay : np.ndarray

        """
        sky = self.sky * self.beam
        visibilities = {}

        for k, delay in tqdm(self.delays.items()):
            visibilities[k] = np.sum(
                sky * np.exp(-2 * np.pi * 1j * self.nu[:, None] * delay).value, axis=1
            )

        return visibilities
